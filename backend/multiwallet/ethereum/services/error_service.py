class WalletGenerationError(Exception):
    """Raised when wallet generation fails."""
    pass

class WalletRecoveryError(Exception):
    """Raised when wallet recovery fails."""
    pass

class TransactionError(Exception):
    """Raised when a transaction fails."""
    pass

class BalanceError(Exception):
    """Raised when fetching the balance fails."""
    pass
class CustomError(Exception):
    pass