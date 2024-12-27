from src.models.topup import Topup
from src.exceptions.topup_exceptions import (
    InvalidTopupTypeError,
    DuplicateTopupError,
    InvalidTopupDurationError,
)
from src.constants.constant import TOPUP_COST_ZERO


""" Service for calling topup related functions"""


class TopupService:
    def __init__(self):
        self.topup = Topup()  # instatiating Topup model

    """ Function call for to add topup with given topup type and duration"""

    def add_topup(self, topup_type: str, no_of_months: int):
        try:
            result = self.topup.add_topup(topup_type, no_of_months)
            if result:
                return result
        except (
            DuplicateTopupError,
            InvalidTopupTypeError,
            InvalidTopupDurationError,
        ) as e:
            return str(e)

    """ function to get total topup cost"""

    def calculate_topup_cost(self):
        cost = self.topup.get_topup_cost()
        if cost is None:
            return TOPUP_COST_ZERO
        return cost
