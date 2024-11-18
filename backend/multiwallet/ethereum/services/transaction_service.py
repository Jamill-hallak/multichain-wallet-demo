from ethereum.services.security_service import SecurityService
from ethereum.services.error_service import TransactionError


class TransactionService:
    def __init__(self, web3):
        self.web3 = web3
        self.security_service = SecurityService()

    def send_eth(self, from_address, to_address, amount, encrypted_private_key, otp):
        """
        Send ETH from one address to another.
        Fails gracefully if balance is insufficient.
        """
        if not self.security_service.validate_otp(otp):
            raise TransactionError("Invalid OTP for ETH transaction.")

        try:
            # Get balance and gas details
            balance_wei = self.web3.eth.get_balance(from_address)
            amount_wei = self.web3.to_wei(amount, 'ether')
            gas_price = self.web3.eth.gas_price
            gas_limit = 21000

            # Check if the balance is sufficient
            total_cost = amount_wei + gas_price * gas_limit
            if balance_wei < total_cost:
                raise TransactionError("Not enough balance to complete the transaction.")

            # Decrypt private key and prepare the transaction
            private_key = self.security_service.decrypt_data(encrypted_private_key)
            nonce = self.web3.eth.get_transaction_count(from_address)

            tx = {
                'nonce': nonce,
                'to': to_address,
                'value': amount_wei,
                'gas': gas_limit,
                'gasPrice': gas_price
            }

            # Sign and send the transaction
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)

            return {"tx_hash": tx_hash.hex(), "gas_price": gas_price}
        except TransactionError as e:
            # Specific transaction errors (e.g., insufficient balance)
            raise e
        except Exception as e:
            # General transaction errors
            raise TransactionError(f"Failed to send ETH. Error: {str(e)}")
