from flask import Blueprint, jsonify, request
from web3 import Web3
from services.transaction_service import TransactionService
from middleware.jwt_middleware import jwt_required

transaction_routes = Blueprint("transaction_routes", __name__)

# Initialize Web3 and Transaction Service
web3 = Web3(Web3.HTTPProvider("YOUR_ETHEREUM_RPC_URL"))
transaction_service = TransactionService(web3)

@transaction_routes.route('/send-eth', methods=['POST'])
@jwt_required
def send_eth():
    """
    Send ETH from one address to another.
    Requires JWT authentication and OTP validation.
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

        response = transaction_service.send_eth(from_address, to_address, amount, encrypted_private_key, otp)
        return jsonify({"status": "success", "data": response}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@transaction_routes.route('/send-trc20', methods=['POST'])
@jwt_required
def send_trc20():
    """
    Send TRC-20 tokens from one address to another.
    Requires JWT authentication and OTP validation.
    """
    data = request.json
    try:
        from_address = data.get('from_address')
        to_address = data.get('to_address')
        amount = data.get('amount')
        token_contract_address = data.get('token_contract_address')
        encrypted_private_key = data.get('encrypted_private_key')
        otp = data.get('otp')

        if not all([from_address, to_address, amount, token_contract_address, encrypted_private_key, otp]):
            return jsonify({"status": "error", "message": "All fields are required"}), 400

        response = transaction_service.send_trc20(from_address, to_address, amount, token_contract_address, encrypted_private_key, otp)
        return jsonify({"status": "success", "data": response}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
