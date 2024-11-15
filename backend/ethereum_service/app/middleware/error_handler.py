class CustomError(Exception):
    """Base class for all custom errors."""
    pass


class WalletGenerationError(CustomError):
    """Raised when wallet generation fails."""
    pass


class BalanceQueryError(CustomError):
    """Raised when fetching balance fails."""
    pass
