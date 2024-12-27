from src.enums.topup_type import TopupType
from src.constants.error_codes import ErrorCodes
from src.exceptions.topup_exceptions import (
    InvalidTopupTypeError,
    DuplicateTopupError,
    InvalidTopupDurationError,
)
from src.constants.constant import TOPUP_COST_ZERO, TOPUP_DURATION_ZERO


class Topup:
    """Class to add topup and get total topup cost"""

    def __init__(self):
        self._topup_type = None  # Private attribute for topup type
        self._duration = 0  # Private attribute for duration
        self._cost = 0  # Private attribute for cost

    def _is_valid_topup_type(self, topup_type: str) -> bool:
        """Private method to validate a topup type."""
        return topup_type in TopupType.__members__

    def add_topup(self, topup_type: str, no_of_months: int):
        """Add a topup with the given type and duration."""
        if self._topup_type:
            raise DuplicateTopupError(f"{ErrorCodes.DUPLICATE_TOPUP_ERROR_MESSAGE}")

        if not self._is_valid_topup_type(topup_type):
            raise InvalidTopupTypeError(
                f"{ErrorCodes.INVALID_TOPUP_TYPE_ERROR_MESSAGE}"
            )

        if no_of_months < 0:
            raise InvalidTopupDurationError(
                f"{ErrorCodes.INVALID_TOPUP_DURATION_ERROR_MESSAGE}"
            )

        self._topup_type = TopupType[topup_type]
        self._duration = no_of_months
        self._calculate_cost()

    def _calculate_cost(self):
        """Private method to calculate the topup cost."""
        if self._topup_type and self._duration > TOPUP_DURATION_ZERO:
            topup_details = self._topup_type.get_details()
            self._cost = topup_details["cost"] * self._duration

    def get_topup_cost(self) -> int:
        """Get the total cost of the topup."""
        return self._cost if self._topup_type else TOPUP_COST_ZERO
