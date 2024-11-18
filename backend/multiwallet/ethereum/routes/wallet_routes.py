from flask import Blueprint, jsonify, request
from web3 import Web3
from ethereum.services.wallet_service import WalletService
from ethereum.middleware.jwt_middleware import jwt_required
import os

# Blueprint with a unique name
wallet_routes = Blueprint("ethereum_wallet_routes", __name__)

# Initialize Web3 and Wallet Service
web3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))
wallet_service = WalletService(web3)

if not web3.is_connected():
    raise Exception("Failed to connect to Ethereum node. Check SEPOLIA_RPC_URL.")

@wallet_routes.route('/generate', methods=['GET'], endpoint='ethereum_generate_wallet')
@jwt_required
def generate_wallet():
    """
    Generate a new Ethereum wallet.
    Requires JWT authentication.
    """
    try:
        wallet = wallet_service.generate_wallet()
        return jsonify({"status": "success", "data": wallet}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@wallet_routes.route('/recover', methods=['POST'], endpoint='ethereum_recover_wallet')
@jwt_required
def recover_wallet():
    """
    Recover a wallet using mnemonic and OTP.
    Requires JWT authentication and OTP validation.
    """
    data = request.json
    try:
        mnemonic = data.get('mnemonic')
        otp = data.get('otp')
        if not mnemonic or not otp:
            return jsonify({"status": "error", "message": "Mnemonic and OTP are required"}), 400

        wallet = wallet_service.recover_wallet(mnemonic, otp)
        return jsonify({"status": "success", "data": wallet}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
