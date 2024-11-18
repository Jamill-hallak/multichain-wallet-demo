from web3 import Web3
from ethereum.services.error_service import BalanceError

class BalanceService:
    def __init__(self, web3: Web3):
        self.web3 = web3

    def get_eth_balance(self, address: str) -> float:
        """
        Fetch the ETH balance for a given Ethereum address.
        """
        try:
            if not Web3.is_address(address):
                raise ValueError(f"Invalid Ethereum address: {address}")

            print(f"Fetching balance for address: {address}")
            
            # Fetch balance in Wei
            balance_wei = self.web3.eth.get_balance(address)
            print(f"Balance in Wei: {balance_wei}")
            
            # Convert balance to Ether
            balance_eth = self.web3.from_wei(balance_wei, "ether")
            print(f"Balance in ETH: {balance_eth}")
            
            return balance_eth
        except Exception as e:
            # Log the RPC error message
            print(f"RPC Error: {e}")
            raise BalanceError(f"Failed to fetch ETH balance for {address}: {e}")
