import jwt
import pyotp
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from cryptography.fernet import Fernet

# Load environment variables
load_dotenv()

class SecurityService:
    """
    Handles JWT authentication, OTP-based security, and encryption of sensitive data.
    """

    def __init__(self):
        self.jwt_secret = os.getenv("JWT_SECRET", "default_jwt_secret")
        self.jwt_expiration = int(os.getenv("JWT_EXPIRATION", 3600))  # Default: 1 hour
        self.otp_secret = os.getenv("OTP_SECRET", pyotp.random_base32())  # OTP secret
        self.encryption_key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())  # Encryption key
        self.cipher = Fernet(self.encryption_key.encode())

    # JWT Operations
    def generate_jwt(self, user_id):
        """
        Generate a JWT for a user.
        Args:
            user_id (str): Unique identifier for the user.
        Returns:
            str: The JWT token.
        """
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=self.jwt_expiration)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    def validate_jwt(self, token):
        """
        Validate a JWT token.
        Args:
            token (str): JWT token.
        Returns:
            dict: Decoded payload if valid.
        Raises:
            InvalidTokenError: If the token is invalid or expired.
        """
        try:
            return jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise InvalidTokenError("Token has expired.")
        except InvalidTokenError:
            raise InvalidTokenError("Invalid token.")

    # OTP Operations
    def generate_otp(self):
        """
        Generate a TOTP-based OTP for 2FA.
        Returns:
            str: Generated OTP.
        """
        totp = pyotp.TOTP(self.otp_secret)
        return totp.now()

    def validate_otp(self, otp):
        """
        Validate a TOTP-based OTP.
        Args:
            otp (str): OTP to validate.
        Returns:
            bool: True if OTP is valid, False otherwise.
        """
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(otp)

    # Encryption/Decryption Operations
    def encrypt_data(self, data):
        """
        Encrypt sensitive data such as private keys.
        Args:
            data (str): Data to encrypt.
        Returns:
            str: Encrypted data.
        """
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        """
        Decrypt sensitive data such as private keys.
        Args:
            encrypted_data (str): Encrypted data to decrypt.
        Returns:
            str: Decrypted data.
        """
        return self.cipher.decrypt(encrypted_data.encode()).decode()
