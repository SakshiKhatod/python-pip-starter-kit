from src.constants.plan_mapping import PLAN_DETAILS
from src.enums.plan_type import PlanType
from src.enums.subscription_category import SubscriptionCategory
from src.constants.error_codes import ErrorCodes


# class to add and get details of plan
class Plan:
    def __init__(self):
        self._plans = {}

    # Function to check whether given subscription plan is valid or not
    def is_valid_plan(self, plan_type: str) -> PlanType:
        try:
            return PlanType[plan_type]
        except KeyError:
            return None

    # Function to add subscription plan with subscription category and plan type
    def add_plan(
        self, subscription_category: SubscriptionCategory, plan_type: PlanType
    ):
        self._plans[subscription_category] = plan_type

    # Function to get all plans
    def get_plans(self) -> dict:
        return self._plans

    # Function to get plan details
    def get_plan_details(
        self, category: SubscriptionCategory, plan_type: PlanType
    ) -> dict:
        try:
            plan_details = PLAN_DETAILS[category][plan_type]
        except KeyError:
            raise ValueError(ErrorCodes.INVALID_PLAN_DETAILS_MAPPING)

        return {
            "category": category.value,
            "plan_type": plan_type.value,
            "cost": plan_details["cost"],
            "duration_in_months": plan_details["duration"],
        }
