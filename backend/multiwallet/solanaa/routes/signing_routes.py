from flask import Blueprint, jsonify, request
from solanaa.services.signing_service import SigningService
from solanaa.middleware.jwt_middleware import jwt_required

# Initialize the Blueprint
signing_routes = Blueprint("Solana_signing_routes", __name__)

# Initialize Signing Service
signing_service = SigningService()

@signing_routes.route('/sign-message', methods=['POST'], endpoint='sign_message')
@jwt_required
def sign_message():
    """
    Sign a message with the user's Solana private key.
    """
    data = request.json
    try:
        # Extract message and private key from the request
        message = data.get("message")
        private_key = data.get("private_key")

        if not message or not private_key:
            return jsonify({"status": "error", "message": "Message and private key are required"}), 400

        # Use the signing service to sign the message
        result = signing_service.sign_message(message, private_key)
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}), 500
