from web3 import Web3

class EthereumWallet:
    """
    EthereumWallet handles wallet generation for the Ethereum blockchain.
    """

    def __init__(self):
        self.web3 = Web3()

    def generate_wallet(self):
        """
        Generate a new Ethereum wallet.
        Returns:
            dict: Wallet details containing private_key and address.
        """
        try:
            account = self.web3.eth.account.create()
            return {
                "private_key": account.key.hex(),
                "address": account.address
            }
        except Exception as e:
            raise Exception(f"Failed to generate Ethereum wallet: {str(e)}")
