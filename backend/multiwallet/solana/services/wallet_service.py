from solders.keypair import Keypair
from solana.services.error_service import WalletGenerationError
from solana.services.security_service import SecurityService

class WalletService:
    def __init__(self):
        self.security_service = SecurityService()

    def generate_wallet(self):
        """
        Generate a new Solana wallet.
        Returns:
            dict: Contains wallet address (public key) and encrypted private key.
        Raises:
            WalletGenerationError: If wallet generation fails.
        """
        try:
            # Generate a new keypair
            keypair = Keypair()

            # Access public key and secret key
            public_key = keypair.pubkey()  # `pubkey()` method for public key
            secret_key = keypair.secret()  # `secret()` method for private key
                
            # Encrypt the private key
            encrypted_key = self.security_service.encrypt_data(secret_key.hex())
            
            # Return wallet details
            return {
                "address": str(public_key),  # Convert to string if necessary
                "encrypted_private_key": encrypted_key,
            }
        except Exception as e:
            print(f"Error in generate_wallet: {e}")
            raise WalletGenerationError("Failed to generate wallet.") from e
