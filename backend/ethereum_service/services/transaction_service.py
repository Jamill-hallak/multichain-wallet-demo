from services.security_service import SecurityService
from services.error_service import TransactionError

class TransactionService:
    def __init__(self, web3, tron_web=None):
        self.web3 = web3
        self.tron_web = tron_web
        self.security_service = SecurityService()

    def estimate_gas_eth(self, from_address, to_address, amount):
        try:
            tx = {'from': from_address, 'to': to_address, 'value': self.web3.toWei(amount, 'ether')}
            return self.web3.eth.estimate_gas(tx)
        except Exception as e:
            raise TransactionError("Failed to estimate gas for ETH transaction.") from e

    def send_eth(self, from_address, to_address, amount, encrypted_private_key, otp):
        if not self.security_service.validate_otp(otp):
            raise TransactionError("Invalid OTP for ETH transaction.")
        try:
            private_key = self.security_service.decrypt_data(encrypted_private_key)
            nonce = self.web3.eth.get_transaction_count(from_address)
            gas_price = self.web3.eth.gas_price
            tx = {'nonce': nonce, 'to': to_address, 'value': self.web3.toWei(amount, 'ether'), 'gas': 21000, 'gasPrice': gas_price}
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return {"tx_hash": tx_hash.hex(), "gas_price": gas_price}
        except Exception as e:
            raise TransactionError("Failed to send ETH.") from e

    def send_trc20(self, from_address, to_address, amount, token_contract_address, encrypted_private_key, otp):
        if not self.security_service.validate_otp(otp):
            raise TransactionError("Invalid OTP for TRC-20 transaction.")
        try:
            private_key = self.security_service.decrypt_data(encrypted_private_key)
            contract = self.tron_web.contract(address=token_contract_address)
            tx = contract.functions.transfer(to_address, int(amount)).buildTransaction({'from': from_address})
            signed_tx = self.tron_web.sign_transaction(tx, private_key)
            tx_hash = self.tron_web.send_raw_transaction(signed_tx)
            return {"tx_hash": tx_hash, "status": "Transaction sent"}
        except Exception as e:
            raise TransactionError("Failed to send TRC-20 tokens.") from e
