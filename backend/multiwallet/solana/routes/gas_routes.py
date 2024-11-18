from flask import Blueprint, jsonify
from solana.services.gas_service import GasService
from ethereum.middleware.jwt_middleware import jwt_required  # Reuse JWT middleware
import os

rpc_url = os.getenv("SOLANA_RPC_URL")
gas_service = GasService(rpc_url)

gas_routes = Blueprint("solana_gas_routes", __name__)

@gas_routes.route("/fees", methods=["GET"])
@jwt_required
def get_fees():
    """
    Get the current transaction fees for Solana.
    """
    try:
        fees = gas_service.get_fees()
        return jsonify({"status": "success", "fees": fees})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
