from flask import jsonify

def handle_custom_error(error):
    """
    Handle custom application-specific errors.
    """
    response = {
        "status": "error",
        "message": str(error)
    }
    return jsonify(response), 400


def handle_generic_error(error):
    """
    Handle all other uncaught exceptions.
    """
    response = {
        "status": "error",
        "message": "An unexpected error occurred."
    }
    return jsonify(response), 500
