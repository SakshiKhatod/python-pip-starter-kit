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
        self.subscription = Subscription()

    def start_subscription(self, start_date: str):
        try:
            result = self.subscription.start_subscription(start_date)
            if result:
                return result
        except InvalidDateException as e:
            return str(e)

    def add_subscription(self, subscription_category: str, plan_type: str):
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

    def calculate_renewal_dates(self):
        try:
            renewal_dates = self.subscription.calculate_renewal_dates()
            if renewal_dates:
                return renewal_dates
        except Exception as e:
            return str(e)

    def calculate_subscription_cost(self):
        try:
            total_cost = self.subscription.calculate_subscription_cost()
            return total_cost
        except Exception as e:
            return str(e)

    def get_subscriptions(self):
        try:
            return self.subscription.get_subscriptions()
        except Exception as e:
            return str(e)
