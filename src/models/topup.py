from src.enums.topup_type import TopupType
from src.constants.error_codes import ErrorCodes
from src.exceptions.topup_exceptions import InvalidTopupTypeError, DuplicateTopupError
from src.constants.constant import TOPUP_COST_ZERO


# Topup class for adding topups and calculting it's cost
class Topup:
    def __init__(self):
        self.topup_type = None
        self.duration = 0
        self.cost = 0
        self.stop_execution = False

    # function to check valid topup type
    def is_valid_topup_type(self, topup_type: str) -> bool:
        return topup_type in TopupType.__members__

    # function to add topup with given topup type and duration
    def add_topup(self, topup_type: str, no_of_months: int):
        if self.topup_type:
            self.stop_execution = True
            raise DuplicateTopupError(
                f"{ErrorCodes.ADD_TOPUP_FAILED} {ErrorCodes.DUPLICATE_TOPUP}"
            )

        if not self.is_valid_topup_type(topup_type):
            self.stop_execution = True
            raise InvalidTopupTypeError(
                f"{ErrorCodes.ADD_TOPUP_FAILED} {ErrorCodes.INVALID_TOPUP_TYPE}"
            )

        if no_of_months < 0:
            raise InvalidTopupTypeError(
                f"{ErrorCodes.ADD_TOPUP_FAILED} {ErrorCodes.INVALID_TOPUP_DURATION}"
            )

        self.topup_type = TopupType[topup_type]
        self.duration = no_of_months
        self.calculate_cost()

    # function to calculate topup cost
    def calculate_cost(self):
        if self.topup_type and self.duration > TOPUP_COST_ZERO:
            topup_details = self.topup_type.get_details()
            self.cost = topup_details["cost"] * self.duration

    # function to get topup cost
    def get_topup_cost(self) -> int:
        return self.cost if self.topup_type else TOPUP_COST_ZERO
