from src.models.subscription import Subscription
from src.models.plan import Plan
from src.exceptions.subscription_exceptions import (
    InvalidDateException,
    InvalidCategoryException,
    DuplicateCategoryException,
    InvalidPlanTypeException,
)


# service for calling subscription related functions
class SubscriptionService:
    def __init__(self):
        self.subscription = Subscription()  # instantiating object of Subscription model

    # function to start subscription from given date
    def start_subscription(self, start_date: str) -> str:
        try:
            result = self.subscription.start_subscription(start_date)
            if result:
                return result
        except InvalidDateException as e:
            return str(e)

    # function to add subscription with subscription category and plan given from user
    def add_subscription(self, subscription_category: str, plan_type: str) -> str:
        try:
            result = self.subscription.add_subscription(
                subscription_category, plan_type
            )
            if result:
                return result
        except InvalidDateException as e:
            return str(e)
        except InvalidCategoryException as e:
            return str(e)
        except DuplicateCategoryException as e:
            return str(e)
        except InvalidPlanTypeException as e:
            return str(e)

    # function to calculate renewal dates
    def calculate_renewal_dates(self) -> dict | str:
        try:
            renewal_dates = self.subscription.calculate_renewal_dates()
            if renewal_dates:
                return renewal_dates
        except Exception as e:
            return str(e)

    # function to calculate subscription cost
    def calculate_subscription_cost(self) -> int | str:
        try:
            total_cost = self.subscription.calculate_subscription_cost()
            return total_cost
        except Exception as e:
            return str(e)

    # function to retreive all subscriptions
    def get_subscriptions(self) -> bool | str:
        try:
            return self.subscription.get_subscriptions()
        except Exception as e:
            return str(e)
