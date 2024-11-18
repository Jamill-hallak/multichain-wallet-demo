import os
import sys
from flask import Flask
from dotenv import load_dotenv
from web3 import Web3

# Add the multiwallet directory to the Python module search path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import Ethereum routes
from ethereum.routes.wallet_routes import wallet_routes as ethereum_wallet_routes
from ethereum.routes.balance_routes import balance_routes as ethereum_balance_routes
from ethereum.routes.transaction_routes import transaction_routes as ethereum_transaction_routes
from ethereum.routes.auth_routes import auth_routes as ethereum_auth_routes
from ethereum.routes.gas_estimation_routes import gas_estimation_routes as ethereum_gas_estimation_routes
from ethereum.routes.signing_routes import signing_routes as ethereum_signing_routes


from solana.routes.wallet_routes import  solana_wallet_routes
# from solana.routes.balance_routes import balance_routes as solana_balance_routes
# from solana.routes.transaction_routes import transaction_routes as solana_transaction_routes
# from solana.routes.gas_routes import gas_routes as solana_gas_routes
# from solana.routes.signing_routes import signing_routes as solana_signing_routes

# Import middleware and services
from ethereum.middleware.error_handler import handle_custom_error, handle_generic_error
from ethereum.services.error_service import CustomError





# Load environment variables
load_dotenv()

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))
if not web3.is_connected():
    print("Failed to connect to Ethereum node. Check your SEPOLIA_RPC_URL.")
else:
    print("Connected to Ethereum node.")


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Register Ethereum blueprints
    app.register_blueprint(ethereum_wallet_routes, url_prefix="/ethereum/wallet")
    app.register_blueprint(ethereum_balance_routes, url_prefix="/ethereum/balance")
    app.register_blueprint(ethereum_transaction_routes, url_prefix="/ethereum/transaction")
    app.register_blueprint(ethereum_auth_routes, url_prefix="/ethereum/auth")
    app.register_blueprint(ethereum_gas_estimation_routes, url_prefix="/ethereum/gas-estimation")
    app.register_blueprint(ethereum_signing_routes, url_prefix="/ethereum/signing")
    
    
    
    # #ٌRegister Solana blueprints 
    app.register_blueprint(solana_wallet_routes, url_prefix="/solana/")
    # app.register_blueprint(solana_balance_routes, url_prefix="/solana/balance")
    # app.register_blueprint(solana_gas_routes, url_prefix="/solana/gas")
    # app.register_blueprint(solana_signing_routes, url_prefix="/solana/signing")
    # app.register_blueprint(solana_transaction_routes, url_prefix="/solana/transaction")


    # Register error handlers
    app.register_error_handler(CustomError, handle_custom_error)
    app.register_error_handler(Exception, handle_generic_error)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
