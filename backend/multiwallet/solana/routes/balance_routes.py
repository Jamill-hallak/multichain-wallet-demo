from flask import Blueprint, jsonify
from solana.services.balance_service import BalanceService
from ethereum.middleware.jwt_middleware import jwt_required  # Reuse Ethereum JWT middleware
import os

# Initialize the Solana balance service
rpc_url = os.getenv("SOLANA_RPC_URL")
balance_service = BalanceService(rpc_url)

balance_routes = Blueprint("solana_balance_routes", __name__)

@balance_routes.route("/<address>", methods=["GET"])
@jwt_required  # Enforce JWT authentication
def get_balance(address):
    """
    Get the balance of a Solana wallet.
    """
    try:
        balance = balance_service.get_balance(address)
        return jsonify({"status": "success", "balance": balance})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
