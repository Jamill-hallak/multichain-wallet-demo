from flask import Blueprint, jsonify, request
from solana.services.transaction_service import TransactionService
from ethereum.middleware.jwt_middleware import jwt_required  # Reuse Ethereum JWT middleware
from solana.keypair import Keypair
import os

# Initialize the Solana transaction service
rpc_url = os.getenv("SOLANA_RPC_URL")
transaction_service = TransactionService(rpc_url)

transaction_routes = Blueprint("solana_transaction_routes", __name__)

@transaction_routes.route("/send", methods=["POST"])
@jwt_required  # Enforce JWT authentication
def send_transaction():
    """
    Create, sign, and send a Solana transaction.
    Expects JSON with 'from_address', 'to_address', 'amount', and 'private_key'.
    """
    try:
        # Parse the request body
        data = request.get_json()
        from_address = data["from_address"]
        to_address = data["to_address"]
        amount = float(data["amount"])
        private_key = bytes.fromhex(data["private_key"])  # Convert private key to bytes

        # Create the transaction
        transaction = transaction_service.create_transfer_transaction(from_address, to_address, amount)

        # Load the sender's keypair
        signer_keypair = Keypair.from_secret_key(private_key)

        # Send the transaction
        tx_signature = transaction_service.send_transaction(transaction, signer_keypair)

        return jsonify({"status": "success", "tx_signature": tx_signature})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
