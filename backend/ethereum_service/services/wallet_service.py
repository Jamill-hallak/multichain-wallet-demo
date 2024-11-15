from web3 import Web3
from services.errors import WalletGenerationError, BalanceQueryError


class EthereumWallet:
    """
    Handles Ethereum wallet operations, such as wallet generation and balance queries.
    """

    def __init__(self):
        try:
            self.web3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID"))
        except Exception as e:
            raise ConnectionError("Failed to connect to the Ethereum network.") from e

    def generate_wallet(self):
        """
        Generate a new Ethereum wallet.
        Returns:
            dict: A dictionary containing the private key and address of the wallet.
        Raises:
            WalletGenerationError: If wallet generation fails.
        """
        try:
            account = self.web3.eth.account.create()
            return {"private_key": account.key.hex(), "address": account.address}
        except Exception as e:
            raise WalletGenerationError("Failed to generate wallet.") from e

    def get_balance(self, address):
        """
        Fetch the Ether balance of a given Ethereum address.
        Args:
            address (str): The Ethereum address.
        Returns:
            float: The balance in Ether.
        Raises:
            BalanceQueryError: If balance fetching fails.
        """
        if not self.web3.isAddress(address):
            raise BalanceQueryError(f"Invalid Ethereum address: {address}")
        try:
            balance_wei = self.web3.eth.get_balance(address)
            return self.web3.fromWei(balance_wei, "ether")
        except Exception as e:
            raise BalanceQueryError(f"Failed to fetch balance for address {address}.") from e
