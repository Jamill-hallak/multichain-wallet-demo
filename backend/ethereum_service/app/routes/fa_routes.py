from flask import Blueprint
from services.security_service import SecurityService

twofa_routes = Blueprint("twofa_routes", __name__)

# Initialize security service
security_service = SecurityService()

@twofa_routes.route("/generate-2fa", methods=["GET"])
def generate_2fa():
    """
    Generate a 2FA secret.
    """
    try:
        secret = security_service.generate_2fa_secret()
        return {"status": "success", "data": {"2fa_secret": secret}}, 200
    except Exception as e:
        return {"status": "error", "message": "Failed to generate 2FA secret."}, 500
