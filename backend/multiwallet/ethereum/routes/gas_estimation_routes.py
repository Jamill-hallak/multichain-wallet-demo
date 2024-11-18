from flask import Blueprint, jsonify, request
from web3 import Web3
from ethereum.services.gas_estimation_service import GasEstimationService
from ethereum.middleware.jwt_middleware import jwt_required
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

gas_estimation_routes = Blueprint("gas_estimation_routes", __name__)

# Initialize Web3 and Gas Estimation Service
rpc_url = os.getenv("SEPOLIA_RPC_URL")
web3 = Web3(Web3.HTTPProvider(rpc_url))
gas_estimation_service = GasEstimationService(web3)


@gas_estimation_routes.route('/estimate-gas', methods=['POST'], endpoint='estimate_gas')
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

        result = gas_estimation_service.estimate_gas(from_address, to_address, amount)
        return jsonify({"status": "success", "data": result}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}), 500
