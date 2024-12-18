from src.constants.error_codes import ErrorCodes
from src.models.topup import Topup
from src.models.subscription import Subscription
from src.enums.topup_type import TopupType


class TopupService:
    def __init__(self, subscription: Subscription):
        self.subscription = subscription

    def add_topup(self, topup_type: TopupType, no_of_months: int):
        if not self.subscription.plans:
            return (
                ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.SUBSCRIPTIONS_NOT_FOUND
            )
        if self.subscription.topup:
            return ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.DUPLICATE_TOPUP

        self.subscription.topup = Topup(topup_type, no_of_months)
        return None
