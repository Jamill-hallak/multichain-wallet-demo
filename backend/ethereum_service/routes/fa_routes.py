from flask import Blueprint, jsonify, request
from services.security_service import SecurityService
from services.error_service import CustomError

twofa_routes = Blueprint("twofa_routes", __name__)
security_service = SecurityService()

@twofa_routes.route("/generate-otp", methods=["POST"])
def generate_otp():
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            raise CustomError("User ID is required.", 400)
        otp = security_service.generate_otp(user_id)
        return jsonify({"status": "success", "otp": otp}), 200
    except Exception as e:
        raise CustomError(f"Failed to generate OTP: {str(e)}", 500)

@twofa_routes.route("/verify-otp", methods=["POST"])
def verify_otp():
    try:
        data = request.json
        user_id = data.get("user_id")
        otp = data.get("otp")
        print(f"Received OTP: {otp} for user: {user_id}")  # Debugging line
        if not user_id or not otp:
            raise CustomError("User ID and OTP are required.", 400)
        is_valid = security_service.verify_otp(user_id, otp)
        return jsonify({"status": "success", "valid": is_valid}), 200
    except Exception as e:
        raise CustomError(f"Failed to verify OTP: {str(e)}", 500)

