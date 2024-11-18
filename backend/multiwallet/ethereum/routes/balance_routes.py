from flask import Blueprint, jsonify
from web3 import Web3
from ethereum.services.balance_service import BalanceService
from ethereum.middleware.jwt_middleware import jwt_required
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

balance_routes = Blueprint("balance_routes", __name__)

# Initialize Web3 and Balance Service
rpc_url = os.getenv("SEPOLIA_RPC_URL")
web3 = Web3(Web3.HTTPProvider(rpc_url))
balance_service = BalanceService(web3)

@balance_routes.route('/eth/<address>', methods=['GET'], endpoint='get_eth_balance')
@jwt_required
def get_eth_balance(address):
    """
    Fetch ETH balance for a given address.
    Requires JWT authentication.
    """
    try:
        # Lazy import BalanceService to avoid circular import
        from ethereum.services.balance_service import BalanceService
        from web3 import Web3

        # Load RPC URL and initialize Web3
        rpc_url = os.getenv("SEPOLIA_RPC_URL")
        web3 = Web3(Web3.HTTPProvider(rpc_url))

        if not web3.is_connected():
            raise Exception("Failed to connect to Ethereum node.")

        # Initialize BalanceService with Web3
        balance_service = BalanceService(web3)

        # Validate Ethereum address
        if not web3.is_address(address):
            return jsonify({"status": "error", "message": "Invalid Ethereum address"}), 400

        # Fetch the balance
        balance = balance_service.get_eth_balance(address)
        return jsonify({"status": "success", "balance": str(balance)}), 200
    except Exception as e:
        # Log the error for debugging
        print(f"Error in get_eth_balance: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400



# @balance_routes.route('/trc20', methods=['POST'], endpoint='get_trc20_balance')
# @jwt_required
# def get_trc20_balance():
#     """
#     Fetch TRC-20 token balance for a given address and token contract.
#     Requires JWT authentication.
#     """
#     data = request.json
#     try:
#         wallet_address = data.get('wallet_address')
#         token_contract_address = data.get('token_contract_address')

#         if not wallet_address or not token_contract_address:
#             return jsonify({"status": "error", "message": "Wallet address and token contract address are required"}), 400

#         balance = balance_service.get_trc20_balance(wallet_address, token_contract_address)
#         return jsonify({"status": "success", "balance": balance}), 200
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 400
