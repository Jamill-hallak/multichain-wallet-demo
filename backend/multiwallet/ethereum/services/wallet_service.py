
from web3 import Web3
from ethereum.services.error_service import WalletGenerationError, WalletRecoveryError
from ethereum.services.security_service import SecurityService

class WalletService:
    """
    Handles Ethereum wallet generation and recovery with encrypted private keys.
    """

    def __init__(self, web3: Web3):
        self.web3 = web3
        self.security_service = SecurityService()

    def generate_wallet(self):
        """
        Generate a new Ethereum wallet.
        Returns:
            dict: Contains wallet address and encrypted private key.
        Raises:
            WalletGenerationError: If wallet generation fails.
        """
        try:
            account = self.web3.eth.account.create()
            encrypted_key = self.security_service.encrypt_data(account.key.hex())
            return {"address": account.address, "encrypted_private_key": encrypted_key}
        except Exception as e:
            raise WalletGenerationError("Failed to generate wallet.") from e

    def recover_wallet(self, mnemonic, otp):
        """
        Recover an Ethereum wallet using a mnemonic and OTP.
        Args:
            mnemonic (str): Wallet mnemonic.
            otp (str): OTP for validation.
        Returns:
            dict: Wallet address and encrypted private key.
        Raises:
            WalletRecoveryError: If recovery fails or OTP is invalid.
        """
        if not self.security_service.validate_otp(otp):
            raise WalletRecoveryError("Invalid OTP for wallet recovery.")
        try:
            account = self.web3.eth.account.from_mnemonic(mnemonic)
            encrypted_key = self.security_service.encrypt_data(account.key.hex())
            return {"address": account.address, "encrypted_private_key": encrypted_key}
        except Exception as e:
            raise WalletRecoveryError("Failed to recover wallet.") from e