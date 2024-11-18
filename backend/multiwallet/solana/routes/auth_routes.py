from flask import Blueprint, jsonify, request
from ethereum.services.security_service import SecurityService

auth_routes = Blueprint("auth_routes", __name__)
security_service = SecurityService()

@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Login endpoint to authenticate users and return a JWT token.
    """
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')

    # Example: Replace with actual authentication logic
    if user_id == "user123" and password == "password123":
        token = security_service.generate_jwt(user_id)
        return jsonify({"status": "success", "token": token}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401
