from src.constants.plan_mapping import PLAN_DETAILS
from src.enums.plan_type import PlanType
from src.enums.subscription_category import SubscriptionCategory
from src.constants.error_codes import ErrorCodes


"""class to add and get details of plan"""


class Plan:
    def __init__(self):
        self._plans = {}

    def _get_plan_data(self, category: SubscriptionCategory, plan_type: PlanType):
        """Function to fetch plan data with error handling."""
        try:
            return PLAN_DETAILS[category][plan_type]
        except KeyError:
            raise ValueError(ErrorCodes.INVALID_PLAN_DETAILS_MAPPING)

    def is_valid_plan(self, plan_type: str) -> PlanType:
        """Function to check whether given subscription plan is valid or not"""
        try:
            return PlanType[plan_type]
        except KeyError:
            return None

    def add_plan(
        self, subscription_category: SubscriptionCategory, plan_type: PlanType
    ):
        """Function to add subscription plan with subscription category and plan type"""
        self._plans[subscription_category] = plan_type

    def get_plans(self) -> dict:
        """Function to get all plans"""
        return self._plans

    def get_plan_details(
        self, category: SubscriptionCategory, plan_type: PlanType
    ) -> dict:
        """Function to get plan details"""
        plan_details = self._get_plan_data(category, plan_type)
        return {
            "category": category.value,
            "plan_type": plan_type.value,
            "cost": plan_details["cost"],
            "duration_in_months": plan_details["duration"],
        }
