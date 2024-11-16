from flask import Blueprint, jsonify, request
from web3 import Web3
from services.wallet_service import WalletService
from middleware.jwt_middleware import jwt_required

wallet_routes = Blueprint("wallet_routes", __name__)

# Initialize Web3 and Wallet Service
web3 = Web3(Web3.HTTPProvider("YOUR_ETHEREUM_RPC_URL"))
wallet_service = WalletService(web3)

@wallet_routes.route('/generate', methods=['GET'])
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

@wallet_routes.route('/recover', methods=['POST'])
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
