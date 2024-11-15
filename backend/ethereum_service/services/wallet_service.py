from web3 import Web3
from services.error_service import WalletGenerationError


class WalletService:
    """
    Handles wallet generation and related operations for Ethereum.
    """

    def __init__(self, rpc_url):
        try:
            self.web3 = Web3(Web3.HTTPProvider(rpc_url))
            if not self.web3.isConnected():
                raise ConnectionError("Failed to connect to Ethereum network.")
        except Exception as e:
            raise ConnectionError("Ethereum RPC connection error.") from e

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
