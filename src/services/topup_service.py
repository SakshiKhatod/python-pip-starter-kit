from src.constants.error_codes import ErrorCodes
from src.models.topup import Topup


class TopupService:
    def __init__(self):
        self.topup = None
        self.stop_execution = False

    def add_topup(self, topup_type: str, no_of_months: int):
        if self.topup:
            self.stop_execution = True
            return f"{ErrorCodes.ADD_TOPUP_FAILED} {ErrorCodes.DUPLICATE_TOPUP}"
        new_topup = Topup()
        if not new_topup.is_valid_topup(topup_type, no_of_months):
            self.stop_execution = True
            return f"{ErrorCodes.ADD_TOPUP_FAILED} {ErrorCodes.INVALID_TOPUP_TYPE}"
        self.topup = new_topup
        self.topup.calculate_cost()
        return None

    def calculate_topup_cost(self):
        if not self.topup:
            return 0
        return self.topup.cost
