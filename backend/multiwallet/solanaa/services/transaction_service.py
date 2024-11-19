from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.transaction import Transaction
from solders.message import Message
from solders.hash import Hash
from solders.keypair import Keypair
from solana.rpc.api import Client


class TransactionService:
    def __init__(self, rpc_url):
        """
        Initialize the TransactionService with the Solana RPC URL.
        Args:
            rpc_url (str): Solana RPC URL.
        """
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
            print(f"Creating transfer transaction: from={from_address}, to={to_address}, amount={amount}")

            lamports = int(amount * 1e9)  # Convert SOL to lamports
            print(f"Lamports: {lamports}")

            from_pubkey = Pubkey.from_string(from_address)
            to_pubkey = Pubkey.from_string(to_address)
            print(f"From Pubkey: {from_pubkey}, To Pubkey: {to_pubkey}")

            # Create the transfer instruction
            transfer_instruction = transfer(
                TransferParams(
                    from_pubkey=from_pubkey,
                    to_pubkey=to_pubkey,
                    lamports=lamports
                )
            )
            print(f"Transfer Instruction: {transfer_instruction}")

            # Fetch recent blockhash
            blockhash_response = self.client.get_latest_blockhash()
            print(f"Blockhash Response: {blockhash_response}")

            # Convert the blockhash to a Hash object
            recent_blockhash = Hash.from_string(blockhash_response['result']['value']['blockhash'])
            print(f"Recent Blockhash: {recent_blockhash}")

            # Build the message with the instruction
            message = Message([transfer_instruction])
            print(f"Message: {message}")

            # Create the transaction with the message and blockhash
            transaction = Transaction(message, recent_blockhash)
            print(f"Transaction: {transaction}")

            return transaction
        except Exception as e:
            raise Exception(f"Failed to create transaction. Error: {str(e)}")

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
            print(f"Signing transaction with signer: {signer_keypair.pubkey()}")

            # Sign the transaction with the signer's keypair
            signed_transaction = transaction.sign([signer_keypair])
            print(f"Signed Transaction: {signed_transaction}")

            # Send the transaction to the Solana network
            response = self.client.send_transaction(signed_transaction, signer_keypair)
            print(f"Transaction Response: {response}")

            # Check the response for the result
            if "result" in response:
                return response["result"]
            else:
                raise Exception(f"Failed to send transaction: {response}")
        except Exception as e:
            raise Exception(f"Failed to send transaction. Error: {str(e)}")
