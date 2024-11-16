from flask import jsonify
from services.error_service import CustomError


def handle_custom_error(error):
    """
    Custom error handler for defined application errors.
    """
    response = jsonify({"status": "error", "message": str(error)})
    response.status_code = 400
    return response


def handle_generic_error(error):
    """
    Generic error handler for unexpected exceptions.
    """
    response = jsonify({"status": "error", "message": "An unexpected error occurred."})
    response.status_code = 500
    return response
