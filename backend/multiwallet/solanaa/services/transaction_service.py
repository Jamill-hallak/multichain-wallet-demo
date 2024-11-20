from solathon import Client, Keypair, PublicKey, Transaction
from solathon.core.instructions import transfer

class TransactionService:
    def __init__(self, rpc_url):
        self.client = Client(rpc_url, local=True)

    def create_transfer_transaction(self, from_keypair, to_address, amount):
        try:
            lamports = int(amount * 1e9)
            to_pubkey = PublicKey(to_address)
            transfer_instruction = transfer(
                from_public_key=from_keypair.public_key,
                to_public_key=to_pubkey,
                lamports=lamports
            )
            transaction = Transaction(instructions=[transfer_instruction], signers=[from_keypair])
            return transaction
        except Exception as e:
            raise Exception(f"Failed to create transaction. Error: {str(e)}")

    def send_transaction(self, transaction):
        try:
            result = self.client.send_transaction(transaction)
            if "result" in result:
                return result["result"]
            else:
                raise Exception(f"Failed to send transaction: {result}")
        except Exception as e:
            raise Exception(f"Failed to send transaction. Error: {str(e)}")
