from flask import Blueprint, jsonify, request
from web3 import Web3
from ethereum.services.signing_service import SigningService
from ethereum.middleware.jwt_middleware import jwt_required
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

signing_routes = Blueprint("signing_routes", __name__)

# Initialize Web3 and Signing Service
rpc_url = os.getenv("ETHEREUM_RPC_URL")
web3 = Web3(Web3.HTTPProvider(rpc_url))
signing_service = SigningService(web3)


@signing_routes.route('/sign-message', methods=['POST'], endpoint='sign_message')
@jwt_required
def sign_message():
    """
    Sign a message with the user's private key.
    """
    data = request.json
    try:
        message = data.get("message")
        private_key = data.get("private_key")

        if not message or not private_key:
            return jsonify({"status": "error", "message": "Message and private key are required"}), 400

        result = signing_service.sign_message(message, private_key)
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}), 500
