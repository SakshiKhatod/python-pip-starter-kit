class TopupError(Exception):
    """Base class for all topup-related exceptions."""

    pass


class DuplicateTopupError(TopupError):
    """Raised when a duplicate topup is added."""

    pass


class InvalidTopupTypeError(TopupError):
    """Raised when an invalid topup type is provided."""

    pass


class InvalidTopupDurationError(TopupError):
    """Raised when an invalid topup duration is provided."""

    pass
