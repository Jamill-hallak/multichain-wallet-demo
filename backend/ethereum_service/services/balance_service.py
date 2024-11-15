from web3 import Web3
from services.error_service import BalanceQueryError


class BalanceService:
    """
    Handles balance-related operations for Ethereum wallets.
    """

    def __init__(self, rpc_url):
        try:
            self.web3 = Web3(Web3.HTTPProvider(rpc_url))
            if not self.web3.isConnected():
                raise ConnectionError("Failed to connect to Ethereum network.")
        except Exception as e:
            raise ConnectionError("Ethereum RPC connection error.") from e

    def get_balance(self, address):
        """
        Fetch the Ether balance of a given Ethereum address.
        Args:
            address (str): Ethereum wallet address.
        Returns:
            float: Balance in Ether.
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
