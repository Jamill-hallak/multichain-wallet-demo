from cryptography.fernet import Fernet
import pyotp

class SecurityUtils:
    """
    Handles encryption, decryption, and 2FA verification.
    """

    def __init__(self):
        # Generate or load encryption key
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)

    def encrypt(self, data):
        """
        Encrypts a string.
        Args:
            data (str): The string to encrypt.
        Returns:
            str: The encrypted data.
        """
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        """
        Decrypts a string.
        Args:
            encrypted_data (str): The encrypted string.
        Returns:
            str: The decrypted data.
        """
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def generate_2fa_secret(self):
        """
        Generates a 2FA secret for a user.
        Returns:
            str: The 2FA secret key.
        """
        return pyotp.random_base32()

    def verify_2fa(self, secret, token):
        """
        Verifies a TOTP token.
        Args:
            secret (str): The user's 2FA secret.
            token (str): The TOTP token to verify.
        Returns:
            bool: True if the token is valid, False otherwise.
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
