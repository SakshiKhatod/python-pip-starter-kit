from src.enums.topup_type import TopupType
from src.constants.error_codes import ErrorCodes
from src.exceptions.topup_exceptions import (
    InvalidTopupTypeError,
    DuplicateTopupError,
    InvalidTopupDurationError,
)
from src.constants.constant import TOPUP_COST_ZERO, TOPUP_DURATION_ZERO


class Topup:
    """Class to manage topup and calculate total topup cost"""

    def __init__(self):
        self._topup_type = None  # Private attribute for topup type
        self._duration = 0  # Private attribute for duration
        self._cost = 0  # Private attribute for cost

    def _validate_topup_type(self, topup_type: str):
        """Validate topup type."""
        if topup_type not in TopupType.__members__:
            raise InvalidTopupTypeError(
                f"{ErrorCodes.INVALID_TOPUP_TYPE_ERROR_MESSAGE}"
            )

    def _validate_duration(self, no_of_months: int):
        """Validate duration."""
        if no_of_months < 0:
            raise InvalidTopupDurationError(
                f"{ErrorCodes.INVALID_TOPUP_DURATION_ERROR_MESSAGE}"
            )

    def _validate_existing_topup(self):
        """Method to check no duplicate topups are added."""
        if self._topup_type:
            raise DuplicateTopupError(f"{ErrorCodes.DUPLICATE_TOPUP_ERROR_MESSAGE}")

    def _calculate_cost(self):
        """Calculate the total cost of topup"""
        if self._topup_type and self._duration > TOPUP_DURATION_ZERO:
            topup_details = self._topup_type.get_details()
            self._cost = topup_details["cost"] * self._duration

    def add_topup(self, topup_type: str, no_of_months: int):
        """Add topup by validating and calculating cost."""
        self._validate_existing_topup()
        self._validate_topup_type(topup_type)
        self._validate_duration(no_of_months)

        self._topup_type = TopupType[topup_type]
        self._duration = no_of_months
        self._calculate_cost()

    def get_topup_cost(self) -> int:
        """Return total topup cost, default to ZERO if no topup."""
        return self._cost if self._topup_type else TOPUP_COST_ZERO
