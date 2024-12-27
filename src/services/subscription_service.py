from src.models.subscription import Subscription
from src.exceptions.subscription_exceptions import (
    InvalidDateException,
    InvalidCategoryException,
    DuplicateCategoryException,
    InvalidPlanTypeException,
    InvalidOnlyDateException,
)


# service for calling subscription related functions
class SubscriptionService:
    def __init__(self):
        self.subscription = Subscription()  # instantiating object of Subscription model

    def _handle_service_method(self, service_method, *args, **kwargs):
        """Helper method to execute service methods and handle exceptions."""
        try:
            result = service_method(*args, **kwargs)
            return result  # Assuming result check is handled by the caller
        except (
            InvalidOnlyDateException,
            InvalidDateException,
            InvalidCategoryException,
            InvalidPlanTypeException,
            DuplicateCategoryException,
        ) as e:
            return str(e)  # Return the error message from exception
        except Exception as e:
            return str(e)  # Generic exception handling

    def is_subscription_date_valid(self) -> bool:
        """Check if the subscription's start date is valid."""
        return self._handle_service_method(self.subscription.is_start_date_valid)

    def start_subscription(self, start_date: str):
        """Starts a subscription from the given date."""
        return self._handle_service_method(
            self.subscription.start_subscription, start_date
        )

    def add_subscription(self, subscription_category: str, plan_type: str):
        """Adds a subscription with the given category and plan type."""
        return self._handle_service_method(
            self.subscription.add_subscription, subscription_category, plan_type
        )

    def calculate_renewal_dates(self):
        """Calculates renewal dates for all subscriptions."""
        return self._handle_service_method(self.subscription.calculate_renewal_dates)

    def calculate_subscription_cost(self):
        """Calculates the total cost of all subscriptions."""
        return self._handle_service_method(
            self.subscription.calculate_subscription_cost
        )

    def get_subscriptions(self):
        """Retrieves all subscriptions."""
        return self._handle_service_method(self.subscription.get_subscriptions)
