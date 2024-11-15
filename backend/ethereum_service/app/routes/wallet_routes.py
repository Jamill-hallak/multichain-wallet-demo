from flask import Blueprint, request
from services.wallet_service import WalletService
from services.security_service import SecurityService
from services.error_service import WalletGenerationError, TwoFactorAuthenticationError

wallet_routes = Blueprint("wallet_routes", __name__)

# Initialize services
wallet_service = WalletService("https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID")
security_service = SecurityService()

@wallet_routes.route("/generate-wallet", methods=["POST"])
def generate_wallet():
    """
    Generate a new Ethereum wallet. Requires 2FA for security.
    """
    try:
        data = request.json
        secret = data.get("2fa_secret")
        token = data.get("2fa_token")

        if not secret or not token or not security_service.verify_2fa(secret, token):
            raise TwoFactorAuthenticationError("Invalid 2FA token.")

        wallet = wallet_service.generate_wallet()
        wallet["private_key"] = security_service.encrypt(wallet["private_key"])
        return {"status": "success", "data": wallet}, 200
    except TwoFactorAuthenticationError as e:
        return {"status": "error", "message": str(e)}, 403
    except WalletGenerationError as e:
        return {"status": "error", "message": str(e)}, 500
    except Exception as e:
        return {"status": "error", "message": "An unexpected error occurred."}, 500
