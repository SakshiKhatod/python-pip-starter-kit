from src.constants.error_codes import ErrorCodes
from src.services.subscription_service import SubscriptionService
from src.services.topup_service import TopupService
from src.constants.constant import RENEWAL_REMINDER_MESSAGE, RENEWAL_AMOUNT_MESSAGE


class User:
    def __init__(self):
        self._subscription_service = SubscriptionService()
        self._topup_service = TopupService()

    def process_start_subscription(self, start_date):
        try:
            result = self._subscription_service.start_subscription(start_date)
            if result:
                print(result)
        except Exception as e:
            return f"Error: {str(e)}"

    def process_add_subscription(self, category, plan_type):
        try:
            result = self._subscription_service.add_subscription(category, plan_type)
            if result:
                print(result)
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def process_add_topup(self, topup_type, months):
        try:
            if self._subscription_service.get_subscriptions():
                result = self._topup_service.add_topup(topup_type, months)
                if result:
                    print(result)
                return result
            else:
                print(
                    ErrorCodes.ADD_TOPUP_FAILED
                    + " "
                    + ErrorCodes.SUBSCRIPTIONS_NOT_FOUND
                )
                return ErrorCodes.ADD_TOPUP_FAILED
        except Exception as e:
            return f"Error: {str(e)}"

    def process_print_renewal_details(self):
        try:
            if not self._subscription_service.get_subscriptions():
                print(ErrorCodes.SUBSCRIPTIONS_NOT_FOUND)
                return ErrorCodes.SUBSCRIPTIONS_NOT_FOUND
            total_cost = (
                self._subscription_service.calculate_subscription_cost()
                + self._topup_service.calculate_topup_cost()
            )
            renewal_dates = self._subscription_service.calculate_renewal_dates()
            renewal_details = []
            for category, date in renewal_dates.items():
                renewal_details.append(f"{RENEWAL_REMINDER_MESSAGE} {category} {date}")
            renewal_details.append(f"{RENEWAL_AMOUNT_MESSAGE} {total_cost}")
            for detail in renewal_details:
                print(detail)
        except Exception as e:
            return f"Error: {str(e)}"
