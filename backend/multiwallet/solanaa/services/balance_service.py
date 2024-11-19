from solana.rpc.api import Client
from solders.pubkey import Pubkey  # Use Pubkey from the solders library

class BalanceError(Exception):
    """Custom error class for balance-related exceptions."""
    pass

class BalanceService:
    def __init__(self, rpc_url):
        self.client = Client(rpc_url)

    def get_balance(self, address):
        """
        Get the balance of a Solana wallet.
        Args:
            address (str): Wallet public address.
        Returns:
            float: Balance in SOL.
        Raises:
            BalanceError: If fetching the balance fails.
        """
        try:
            # Convert the address to a Pubkey object
            pubkey = Pubkey.from_string(address)

            # Call the Solana API to get the balance
            response = self.client.get_balance(pubkey)

            # Extract lamports from the structured response
            lamports = response.value  # Extract the `value` field directly
            return lamports / 1e9  # Convert lamports to SOL
        except Exception as e:
            raise BalanceError(f"Failed to fetch balance. Error: {str(e)}")
