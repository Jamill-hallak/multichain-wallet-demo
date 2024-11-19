from flask import Blueprint, jsonify, request
from solanaa.services.wallet_service import WalletService
from ethereum.middleware.jwt_middleware import jwt_required  # Reuse Ethereum JWT middleware

solana_wallet_routes = Blueprint("solana_wallet_routes", __name__)
wallet_service = WalletService()

@solana_wallet_routes.route("/wallet", methods=["GET"])
@jwt_required
def generate_wallet():
    """
    Generate a new Solana wallet.
    """
    try:
        wallet = wallet_service.generate_wallet()
        return jsonify({"status": "success", "data": wallet})
    except Exception as e:
        print(f"Error in generate_wallet endpoint: {e}")  # Log the error
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500


# @wallet_routes.route("/recover", methods=["POST"])
# @jwt_required
# def recover_wallet():
#     """
#     Recover a Solana wallet using private key and OTP.
#     Expects JSON with 'private_key' and 'otp'.
#     """
#     try:
#         data = request.get_json()
#         private_key = data.get("private_key")
#         otp = data.get("otp")

#         if not private_key or not otp:
#             return jsonify({"status": "error", "message": "Missing required fields: private_key, otp"}), 400

#         wallet = wallet_service.recover_wallet(private_key, otp)
#         return jsonify({"status": "success", "data": wallet})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})
