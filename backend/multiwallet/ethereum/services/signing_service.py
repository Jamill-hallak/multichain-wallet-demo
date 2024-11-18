from eth_account.messages import encode_defunct
from eth_utils import keccak
from ethereum.services.error_service import TransactionError

class SigningService:
    def __init__(self, web3):
        self.web3 = web3

    def sign_message(self, message, private_key):
        """
        Sign a message with the provided private key.
        Args:
            message (str): The message to be signed.
            private_key (str): The private key used for signing the message.
        Returns:
            dict: The signed message, including signature components.
        Raises:
            TransactionError: If signing fails.
        """
        try:
            # Validate private key format
            if not private_key.startswith("0x"):
                private_key = "0x" + private_key

            # Encode the message for signing
            encoded_message = encode_defunct(text=message)

            # Sign the message
            signed_message = self.web3.eth.account.sign_message(encoded_message, private_key)

            # Calculate message hash manually if not provided
            try:
                message_hash = signed_message.messageHash
            except AttributeError:
                message_hash = keccak(encoded_message.body)

            return {
                "message": message,
                "message_hash": message_hash.hex(),
                "signature": signed_message.signature.hex(),
                "r": hex(signed_message.r),
                "s": hex(signed_message.s),
                "v": signed_message.v,
            }
        except Exception as e:
            raise TransactionError(f"Failed to sign message. Error: {str(e)}")

    def sign_transaction(self, transaction, private_key):
        """
        Sign an Ethereum transaction with the provided private key.
        Args:
            transaction (dict): The transaction to be signed.
            private_key (str): The private key used for signing the transaction.
        Returns:
            dict: The signed transaction and its hash.
        Raises:
            TransactionError: If signing fails.
        """
        try:
            # Sign the transaction
            signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key)

            return {
                "raw_transaction": signed_txn.rawTransaction.hex(),
                "hash": signed_txn.hash.hex(),
                "r": hex(signed_txn.r),
                "s": hex(signed_txn.s),
                "v": signed_txn.v,
            }
        except Exception as e:
            raise TransactionError(f"Failed to sign transaction. Error: {str(e)}")
