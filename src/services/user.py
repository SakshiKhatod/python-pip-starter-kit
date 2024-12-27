from src.constants.error_codes import ErrorCodes
from src.services.subscription_service import SubscriptionService
from src.services.topup_service import TopupService
from src.constants.constant import RENEWAL_REMINDER_MESSAGE, RENEWAL_AMOUNT_MESSAGE

#User class can add, start subscription and topup and get renewal date with reminder message
class User:
    def __init__(self):
        """Initialize User with services for subscriptions and top-ups."""
        self._subscription_service = SubscriptionService()
        self._topup_service = TopupService()

    def handle_exception(self, func, *args, **kwargs):
        """Generalized method to handle exceptions for subscription operations."""
        try:
            result = func(*args, **kwargs)
            if result:
                print(result)
            return result
        except Exception as e:
            return str(e)

    def process_start_subscription(self, start_date):
        """Starts a subscription with the given start date."""
        return self.handle_exception(
            self._subscription_service.start_subscription, start_date
        )

    def process_add_subscription(self, category, plan_type):
        """Adds a subscription for the given category and plan type."""
        return self.handle_exception(
            self._subscription_service.add_subscription, category, plan_type
        )
    
    def _validate_topup_conditions(self):
        """Validates conditions before adding a top-up."""
        if not self._subscription_service.is_subscription_date_valid():
            raise TypeError(ErrorCodes.INVALID_TOPUP_DATE_MESSAGE)
        if not self._subscription_service.get_subscriptions():
            raise TypeError(ErrorCodes.ADD_TOPUP_FAILED_SUBSCRIPTIONS_NOT_FOUND_MESSAGE)
        
    def process_add_topup(self, topup_type, months):
        """Adds a top-up after validating subscription date and existence."""
        try:
            # Validate subscription date and existence
            self._validate_topup_conditions()

            # Proceed with the top-up operation
            result = self._topup_service.add_topup(topup_type, months)
            if result:
                print(result)
            return result

        except TypeError as e:
            print(str(e))
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return None


    def process_print_renewal_details(self):
        """Prints renewal details for subscriptions and top-ups."""
        try:
            if not self._subscription_service.get_subscriptions():
                raise ValueError(
                    ErrorCodes.PRINT_RENEWAL_DETAILS_SUBSCRIPTIONS_NOT_FOUND_MESSAGE
                )

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
            return print(str(e))
