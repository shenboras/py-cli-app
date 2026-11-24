class ExpenseTrackerError(Exception):
    """Base exception for all expense tracker errors."""


class ValidationError(ExpenseTrackerError):
    """Raised when user input fails validation rules."""


class StorageError(ExpenseTrackerError):
    """Raised when reading or writing expense storage fails."""