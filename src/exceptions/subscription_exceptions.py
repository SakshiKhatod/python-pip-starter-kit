class SubscriptionException(Exception):
    """Base exception for subscription-related errors."""

    pass


class InvalidDateException(SubscriptionException):
    """Raised when the provided date is invalid."""

    pass


class InvalidCategoryException(SubscriptionException):
    """Raised when the subscription category is invalid."""

    pass


class DuplicateCategoryException(SubscriptionException):
    """Raised when a duplicate category is added."""

    pass


class InvalidPlanTypeException(SubscriptionException):
    """Raised when the plan type is invalid."""

    pass


class InvalidOnlyDateException(SubscriptionException):
    """Raised when the only date  is invalid."""

    pass
