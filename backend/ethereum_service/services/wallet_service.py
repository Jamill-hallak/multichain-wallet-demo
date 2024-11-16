import os
from dotenv import load_dotenv
from web3 import Web3
from services.error_service import WalletGenerationError

# Load environment variables
load_dotenv()

class WalletService:
    """
    Handles wallet generation and related operations for Ethereum.
    """

    def __init__(self, rpc_url=None):
        # Use the provided RPC URL or fetch it from environment variables
        if rpc_url:
            self.rpc_url = rpc_url
        else:
            self.rpc_url = os.getenv("SEPOLIA_RPC_URL")
            if not self.rpc_url:
                raise EnvironmentError("SEPOLIA_RPC_URL not set in environment variables.")
        
        # Connect to Ethereum node
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to the Sepolia Ethereum testnet.")

    def generate_wallet(self):
        """
        Generate a new Ethereum wallet.
        Returns:
            dict: A dictionary containing the private key and wallet address.
        Raises:
            WalletGenerationError: If wallet generation fails.
        """
        try:
            account = self.web3.eth.account.create()
            return {"private_key": account.key.hex(), "address": account.address}
        except Exception as e:
            raise WalletGenerationError("Failed to generate Ethereum wallet.") from e

    def get_balance(self, address):
        """
        Get the balance of an Ethereum address.
        Args:
            address (str): Ethereum address.
        Returns:
            float: Balance in Ether.
        Raises:
            ValueError: If the address is invalid.
        """
        try:
            if not self.web3.is_address(address):
                raise ValueError(f"Invalid Ethereum address: {address}")
            balance_wei = self.web3.eth.get_balance(address)
            return self.web3.fromWei(balance_wei, "ether")
        except Exception as e:
            raise WalletGenerationError("Failed to fetch balance.") from e
