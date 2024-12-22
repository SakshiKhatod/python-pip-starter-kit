from datetime import datetime
from src.constants.constant import DATE_FORMAT
from src.constants.error_codes import ErrorCodes
from src.enums.subscription_category import SubscriptionCategory


class Subscription:
    def is_valid_date(self, given_date: str) -> bool:
        try:
            datetime.strptime(given_date, DATE_FORMAT)
            return True
        except ValueError:
            return False

    def is_valid_category(self, category: str) -> SubscriptionCategory:
        try:
            return SubscriptionCategory[category]
        except KeyError:
            return None
