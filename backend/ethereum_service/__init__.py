from flask import Flask
from app.routes.wallet_routes import wallet_routes
from app.routes.balance_routes import balance_routes
from app.routes.fa_routes import twofa_routes
from app.middleware.error_handler import handle_custom_error, handle_generic_error
from services.error_service import CustomError

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)

    # Register blueprints for routes
    app.register_blueprint(wallet_routes, url_prefix="/wallet")
    app.register_blueprint(balance_routes, url_prefix="/balance")
    app.register_blueprint(twofa_routes, url_prefix="/2fa")

    # Register error handlers
    app.register_error_handler(CustomError, handle_custom_error)
    app.register_error_handler(Exception, handle_generic_error)

    return app
