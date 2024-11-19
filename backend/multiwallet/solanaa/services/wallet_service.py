from solders.keypair import Keypair
from solanaa.services.error_service import WalletGenerationError
from solanaa.services.security_service import SecurityService
import os

class WalletService:
    def __init__(self):
        self.security_service = SecurityService()

    def generate_wallet(self):
        """
        Generate a new Solana wallet.
        Returns:
            dict: Contains wallet address (public key), encrypted private key, and encrypted seed.
        Raises:
            WalletGenerationError: If wallet generation fails.
        """
        try:
            # Generate a random 32-byte seed
            seed = os.urandom(32)

            # Generate a new keypair using the seed
            keypair = Keypair.from_seed(seed)

            # Access public key and secret key
            public_key = keypair.pubkey()  # Public key
            secret_key = keypair.secret()  # Private key (64 bytes)

            # Encrypt the private key and seed
            encrypted_key = self.security_service.encrypt_data(secret_key.hex())
            encrypted_seed = self.security_service.encrypt_data(seed.hex())

            # Return wallet details
            return {
                "address": str(public_key),  # Public key as a string
                "encrypted_private_key": encrypted_key,  # Encrypted private key
                "encrypted_seed": encrypted_seed,  # Encrypted seed
            }
        except Exception as e:
            print(f"Error in generate_wallet: {e}")
            raise WalletGenerationError("Failed to generate wallet.") from e
