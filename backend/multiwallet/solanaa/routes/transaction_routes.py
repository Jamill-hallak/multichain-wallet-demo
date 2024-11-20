from flask import Blueprint, jsonify, request
from solathon import Keypair, PublicKey
from solanaa.services.transaction_service import TransactionService
from ethereum.middleware.jwt_middleware import jwt_required
import os

rpc_url = os.getenv("SOLANA_RPC_URL")
if not rpc_url:
    raise ValueError("SOLANA_RPC_URL environment variable is not set.")
transaction_service = TransactionService(rpc_url)

transaction_routes = Blueprint("solana_transaction_routes", __name__)

@transaction_routes.route("/send", methods=["POST"])
@jwt_required
def send_transaction():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON body"}), 400

        from_address = data.get("from_address")
        to_address = data.get("to_address")
        amount = data.get("amount")
        seed = data.get("seed")

        if not from_address or not to_address or not amount or not seed:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        try:
            amount = float(amount)
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid amount format"}), 400

        try:
            seed_bytes = bytes.fromhex(seed)
            if len(seed_bytes) != 32:
                raise ValueError("Seed must be 32 bytes long.")
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        try:
            private_key = seed_bytes
            signer_keypair = Keypair.from_private_key(private_key)
        except Exception as e:
            return jsonify({"status": "error", "message": "Failed to derive Keypair from seed. " + str(e)}), 400

        derived_from_address = str(signer_keypair.public_key)
        if derived_from_address != from_address:
            return jsonify({"status": "error", "message": "Seed does not match from_address"}), 400

        transaction = transaction_service.create_transfer_transaction(signer_keypair, to_address, amount)
        tx_signature = transaction_service.send_transaction(transaction)

        return jsonify({"status": "success", "tx_signature": tx_signature}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
