from ethereum.services.error_service import TransactionError

class GasEstimationService:
    def __init__(self, web3):
        self.web3 = web3

    def estimate_gas(self, from_address, to_address, amount):
        """
        Estimate gas and gas price for an ETH transaction.
        """
        try:
            # Prepare the transaction for estimation
            tx = {
                'from': from_address,
                'to': to_address,
                'value': self.web3.to_wei(amount, 'ether'),
            }
            # Estimate gas usage and get the current gas price
            gas_estimate = self.web3.eth.estimate_gas(tx)
            gas_price = self.web3.eth.gas_price

            return {"gas_estimate": gas_estimate, "gas_price": gas_price}
        except Exception as e:
            error_message = str(e)
            if "insufficient funds" in error_message:
                raise TransactionError("Insufficient funds for gas estimation.")
            raise TransactionError(f"Failed to estimate gas. Error: {error_message}")
