from flask import Blueprint, jsonify, request
from web3 import Web3
from ethereum.services.transaction_service import TransactionService
from ethereum.middleware.jwt_middleware import jwt_required
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

transaction_routes = Blueprint("transaction_routes", __name__)

# Initialize Web3 and Transaction Service
rpc_url = os.getenv("SEPOLIA_RPC_URL")
web3 = Web3(Web3.HTTPProvider(rpc_url))
transaction_service = TransactionService(web3)

@transaction_routes.route('/estimate-gas', methods=['POST'], endpoint='estimate_gas')
@jwt_required
def estimate_gas():
    """
    Estimate gas for an ETH transaction.
    """
    data = request.json
    try:
        from_address = data.get('from_address')
        to_address = data.get('to_address')
        amount = data.get('amount')

        if not all([from_address, to_address, amount]):
            return jsonify({"status": "error", "message": "All fields are required"}), 400

        result = transaction_service.estimate_gas(from_address, to_address, amount)
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@transaction_routes.route('/send-eth', methods=['POST'], endpoint='send_eth')
@jwt_required
def send_eth():
    """
    Send ETH from one address to another.
    """
    data = request.json
    try:
        from_address = data.get('from_address')
        to_address = data.get('to_address')
        amount = data.get('amount')
        encrypted_private_key = data.get('encrypted_private_key')
        otp = data.get('otp')

        if not all([from_address, to_address, amount, encrypted_private_key, otp]):
            return jsonify({"status": "error", "message": "All fields are required"}), 400

        result = transaction_service.send_eth(from_address, to_address, amount, encrypted_private_key, otp)
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
