from flask import Blueprint, jsonify, request
from solanaa.services.transaction_service import TransactionService
from ethereum.middleware.jwt_middleware import jwt_required  # Reuse Ethereum JWT middleware
from solders.keypair import Keypair  # Use Keypair for signing
from solders.pubkey import Pubkey  # Use Pubkey for address validation
import os

# Initialize the Solana transaction service
rpc_url = os.getenv("SOLANA_RPC_URL")
if not rpc_url:
    raise ValueError("SOLANA_RPC_URL environment variable is not set.")
transaction_service = TransactionService(rpc_url)

# Define the Blueprint
transaction_routes = Blueprint("solana_transaction_routes", __name__)

@transaction_routes.route("/send", methods=["POST"])
@jwt_required  # Enforce JWT authentication
def send_transaction():
    """
    Create, sign, and send a Solana transaction.
    Expects JSON with 'from_address', 'to_address', 'amount', and 'seed'.
    """
    print("Debug message", flush=True)

    try:
        # Parse the request body
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON body"}), 400

        from_address = data.get("from_address")
        to_address = data.get("to_address")
        amount = data.get("amount")
        seed = data.get("seed")

        # Validate input
        if not from_address or not to_address or not amount or not seed:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        try:
            amount = float(amount)
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid amount format"}), 400

        # Convert seed to bytes
        try:
            seed_bytes = bytes.fromhex(seed)
            if len(seed_bytes) != 32:
                raise ValueError("Seed must be 32 bytes long.")
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        # Derive Keypair from the seed
        signer_keypair = Keypair.from_seed(seed_bytes)
        # Validate that the derived public key matches the from_address
        derived_from_address = str(signer_keypair.pubkey())
        if derived_from_address != from_address:
            return jsonify({"status": "error", "message": "Seed does not match from_address"}), 400

        # Create the transaction
        transaction = transaction_service.create_transfer_transaction(from_address, to_address, amount)
        
        # Send the transaction
        tx_signature = transaction_service.send_transaction(transaction, signer_keypair)

        return jsonify({"status": "success", "tx_signature": tx_signature}), 200
    except Exception as e:
        # Log the error for debugging
        return jsonify({"status": "error", "message": str(e)}), 500
