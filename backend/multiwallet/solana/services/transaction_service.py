from solana.transaction import Transaction, TransactionInstruction
from solana.rpc.api import Client
from solana.services.error_service import TransactionError

class TransactionService:
    def __init__(self, rpc_url):
        self.client = Client(rpc_url)

    def create_transfer_transaction(self, from_address, to_address, amount):
        """
        Create a Solana transfer transaction.
        Args:
            from_address (str): Sender's public address.
            to_address (str): Recipient's public address.
            amount (float): Amount to transfer in SOL.
        Returns:
            Transaction: A Solana transaction object.
        """
        try:
            lamports = int(amount * 1e9)  # Convert SOL to lamports
            transfer_instruction = TransactionInstruction(
                keys=[
                    {"pubkey": from_address, "is_signer": True, "is_writable": True},
                    {"pubkey": to_address, "is_signer": False, "is_writable": True},
                ],
                program_id="11111111111111111111111111111111",  # Solana system program ID
                data=lamports.to_bytes(8, "little"),  # Amount in lamports
            )
            transaction = Transaction()
            transaction.add(transfer_instruction)
            return transaction
        except Exception as e:
            raise TransactionError(f"Failed to create transaction. Error: {str(e)}")

    def send_transaction(self, transaction, signer_keypair):
        """
        Sign and send a Solana transaction.
        Args:
            transaction (Transaction): The Solana transaction object.
            signer_keypair (Keypair): The signer's keypair for signing the transaction.
        Returns:
            str: Transaction signature.
        """
        try:
            transaction.sign(signer_keypair)
            response = self.client.send_transaction(transaction, signer_keypair)
            if "result" in response:
                return response["result"]
            else:
                raise TransactionError(f"Failed to send transaction: {response}")
        except Exception as e:
            raise TransactionError(f"Failed to send transaction. Error: {str(e)}")
