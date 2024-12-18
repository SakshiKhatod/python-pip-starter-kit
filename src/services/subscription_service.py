from src.constants.error_codes import ErrorCodes
from src.models.plan import Plan
from src.models.subscription import Subscription
from src.enums.subscription_category import SubscriptionCategory
from src.enums.plan_type import PlanType


class SubscriptionService:
    def __init__(self, subscription: Subscription):
        self.subscription = subscription

    def add_subscription(
        self, subscription_category: SubscriptionCategory, plan_type: PlanType
    ):
        if subscription_category not in SubscriptionCategory:
            return (
                ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.INVALID_CATEGORY
            )
        if subscription_category in self.subscription.plans:
            return (
                ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.DUPLICATE_CATEGORY
            )

        plan = Plan(plan_type, subscription_category)
        self.subscription.plans[subscription_category] = plan
        return None

    def get_subscriptions(self):
        return self.subscriptions
