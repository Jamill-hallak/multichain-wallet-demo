from flask import Blueprint, jsonify
from services.balance_service import BalanceService
from services.error_service import BalanceQueryError

balance_routes = Blueprint("balance_routes", __name__)

# Initialize the BalanceService with the Ethereum RPC URL
balance_service = BalanceService("https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID")


@balance_routes.route("/get-balance/<address>", methods=["GET"])
def get_balance(address):
    """
    Fetch the Ether balance of a given Ethereum address.
    """
    try:
        balance = balance_service.get_balance(address)
        return jsonify({"status": "success", "data": {"address": address, "balance": f"{balance} ETH"}}), 200
    except BalanceQueryError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500
