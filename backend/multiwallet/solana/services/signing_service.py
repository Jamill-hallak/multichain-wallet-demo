from solana.transaction import Transaction
from solders.keypair import Keypair
class SigningService:
    def sign_message(self, message, private_key):
        """
        Sign a message with the given private key.
        Args:
            message (str): The message to sign.
            private_key (str): The private key in hex format.
        Returns:
            dict: Signed message and signature.
        """
        try:
            keypair = Keypair.from_secret_key(bytes.fromhex(private_key))
            signature = keypair.sign(message.encode())
            return {
                "message": message,
                "signature": signature.hex(),
            }
        except Exception as e:
            raise ValueError(f"Failed to sign message. Error: {str(e)}")

    def sign_transaction(self, transaction, private_key):
        """
        Sign a Solana transaction with the given private key.
        Args:
            transaction (Transaction): The transaction to sign.
            private_key (str): The private key in hex format.
        Returns:
            Transaction: Signed transaction object.
        """
        try:
            keypair = Keypair.from_secret_key(bytes.fromhex(private_key))
            transaction.sign(keypair)
            return transaction
        except Exception as e:
            raise ValueError(f"Failed to sign transaction. Error: {str(e)}")
