from web3 import Web3
from services.error_service import BalanceError

class BalanceService:
    def __init__(self, web3: Web3):
        self.web3 = web3

    def get_eth_balance(self, address):
        try:
            if not self.web3.is_address(address):
                raise ValueError(f"Invalid Ethereum address: {address}")
            balance = self.web3.eth.get_balance(address)
            return self.web3.fromWei(balance, "ether")
        except Exception as e:
            raise BalanceError("Failed to fetch ETH balance.") from e

    def get_trc20_balance(self, wallet_address, token_contract_address, tron_web):
        try:
            contract = tron_web.trx.contract(address=token_contract_address)
            balance = contract.functions.balanceOf(wallet_address).call()
            return balance
        except Exception as e:
            raise BalanceError("Failed to fetch TRC-20 token balance.") from e
