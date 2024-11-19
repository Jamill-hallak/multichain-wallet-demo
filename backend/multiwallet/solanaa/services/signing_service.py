from solders.keypair import Keypair

class SigningService:
    @staticmethod
    def sign_message(message: str, secret_key: str):
        """
        Sign a message using the given Solana private key.
        Args:
            message (str): The message to sign.
            secret_key (str): The 32-byte private key in hex format.
        Returns:
            dict: Signed message and signature.
        """
        try:
            # Convert the private key from hex to bytes (32 bytes)
            secret_key_bytes = bytes.fromhex(secret_key)

            # Derive the keypair
            keypair = Keypair.from_seed(secret_key_bytes)  # Derive public key automatically

            # Sign the message
            signature = keypair.sign_message(message.encode())

            # Convert the signature to a hex string directly
            signature_hex = str(signature)  # Most likely, the Signature object supports `__str__`

            return {
                "message": message,
                "signature": signature_hex,
            }
        except Exception as e:
            raise ValueError(f"Failed to sign message. Error: {str(e)}")
