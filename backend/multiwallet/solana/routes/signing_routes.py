from flask import Blueprint, jsonify, request
from solana.transaction import Transaction
from solana.services.signing_service import SigningService
from ethereum.middleware.jwt_middleware import jwt_required  # Reuse JWT middleware

signing_service = SigningService()
signing_routes = Blueprint("solana_signing_routes", __name__)

@signing_routes.route("/sign-message", methods=["POST"])
@jwt_required
def sign_message():
    """
    Sign a message with the given private key.
    """
    try:
        data = request.get_json()
        message = data["message"]
        private_key = data["private_key"]
        result = signing_service.sign_message(message, private_key)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@signing_routes.route("/sign-transaction", methods=["POST"])
@jwt_required
def sign_transaction():
    """
    Sign a Solana transaction.
    Expects 'transaction' (serialized) and 'private_key'.
    """
    try:
        data = request.get_json()
        transaction_data = data["transaction"]
        private_key = data["private_key"]

        # Deserialize transaction
        transaction = Transaction.deserialize(bytes.fromhex(transaction_data))

        # Sign transaction
        signed_transaction = signing_service.sign_transaction(transaction, private_key)
        return jsonify({"status": "success", "signed_transaction": signed_transaction.serialize().hex()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
