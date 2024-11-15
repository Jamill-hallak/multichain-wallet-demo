class CustomError(Exception):
    """Base class for custom errors."""
    pass


class WalletGenerationError(CustomError):
    """Raised when wallet generation fails."""
    pass


class TwoFactorAuthenticationError(CustomError):
    """Raised when 2FA verification fails."""
    pass


class BalanceQueryError(CustomError):
    """Raised when querying wallet balance fails."""
    pass
