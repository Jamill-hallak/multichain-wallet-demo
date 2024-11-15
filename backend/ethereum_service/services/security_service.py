import pyotp
from cryptography.fernet import Fernet


class SecurityService:
    """
    Provides encryption, decryption, and 2FA utilities.
    """

    def __init__(self):
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)

    def encrypt(self, data):
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def generate_2fa_secret(self):
        return pyotp.random_base32()

    def verify_2fa(self, secret, token):
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
