from flask import request, jsonify
from ethereum.services.security_service import SecurityService

security_service = SecurityService()

def jwt_required(func):
    """
    Middleware to enforce JWT authentication for secure routes.
    """
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"status": "error", "message": "Authorization token is missing"}), 401

        token = auth_header.split(" ")[1]
        try:
            security_service.validate_jwt(token)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 401

        return func(*args, **kwargs)
    return wrapper
