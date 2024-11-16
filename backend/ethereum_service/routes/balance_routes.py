from flask import Blueprint, jsonify
from services.balance_service import BalanceService
from services.error_service import BalanceQueryError

balance_routes = Blueprint("balance_routes", __name__)

# Initialize BalanceService (will use RPC URL from .env)
balance_service = BalanceService()


@balance_routes.route("/get-balance/<address>", methods=["GET"])
def get_balance(address):
    """
    Fetch the Ether balance of a given Ethereum address.
    """
    try:
        balance = balance_service.get_balance(address)
        return jsonify({"status": "success", "data": {"address": address, "balance": f"{balance} ETH"}}), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except BalanceQueryError as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500
