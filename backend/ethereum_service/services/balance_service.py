from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

class BalanceService:
    def __init__(self):
        rpc_url = os.getenv("SEPOLIA_RPC_URL")
        if not rpc_url:
            raise EnvironmentError("SEPOLIA_RPC_URL not set in environment variables.")
        
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to the Ethereum testnet.")
    

    def get_balance(self, address):
        """
        Fetch the balance of an Ethereum address.
        Args:
            address (str): Ethereum wallet address.
        Returns:
            float: Balance in Ether.
        Raises:
            ValueError: If the Ethereum address is invalid.
            Exception: If fetching the balance fails.
        """
        try:
            if not self.web3.is_address(address):
                raise ValueError(f"Invalid Ethereum address: {address}")
            balance_wei = self.web3.eth.get_balance(address)
            balance_eth = self.web3.from_wei(balance_wei, "ether")
            return balance_eth
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to fetch balance for address {address}. Error: {str(e)}")
