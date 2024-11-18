from solana.rpc.api import Client
from solana.services.error_service import BalanceError

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
            response = self.client.get_balance(address)
            if "result" in response:
                lamports = response["result"]["value"]
                return lamports / 1e9  # Convert lamports to SOL
            else:
                raise BalanceError(f"Error fetching balance: {response}")
        except Exception as e:
            raise BalanceError(f"Failed to fetch balance. Error: {str(e)}")
