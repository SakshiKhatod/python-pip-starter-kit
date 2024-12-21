from src.enums.topup_type import TopupType
from src.constants.error_codes import ErrorCodes


class Topup:
    def __init__(self):
        self.type = None
        self.duration = 0
        self.cost = 0

    def is_valid_topup(self, topup_type: str, no_of_months: int) -> bool:
        try:
            # Validate that the top-up type is part of the enum
            topup_enum = TopupType[topup_type]
            self.no_of_months = no_of_months
            self.cost = topup_enum.get_details()["cost"] * no_of_months
            return True
        except KeyError:
            return False

    def calculate_cost(self):
        if self.type and self.duration > 0:
            topup_details = self.type.get_details()
            self.cost = topup_details["cost"] * self.duration
