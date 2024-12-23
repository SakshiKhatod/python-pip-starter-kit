from src.constants.plan_mapping import PLAN_DETAILS
from src.enums.plan_type import PlanType
from src.enums.subscription_category import SubscriptionCategory
from src.constants.error_codes import ErrorCodes


# Plan class where plans can be added and retrieved
class Plan:
    def __init__(self):
        self.category = None
        self.plan_type = None
        self.cost = None
        self.duration = None
        self.plans = {}

    def is_valid_plan(self, plan_type: str) -> PlanType:
        try:
            return PlanType[plan_type]
        except KeyError:
            return None

    def add_plan(
        self, subscription_category: SubscriptionCategory, plan_type: PlanType
    ):
        self.plans[subscription_category] = plan_type

    def get_plans(self) -> dict:
        return self.plans

    def get_plan_details(self, category: SubscriptionCategory, plan_type: PlanType):
        try:
            plan_details = PLAN_DETAILS[category][plan_type]
        except KeyError:
            raise ValueError(ErrorCodes.INVALID_PLAN_DETAILS_MAPPING)

        self.category = category
        self.plan_type = plan_type
        self.cost = plan_details["cost"]
        self.duration = plan_details["duration"]

        return {
            "category": self.category.value,
            "plan_type": self.plan_type.value,
            "cost": self.cost,
            "duration_in_months": self.duration,
        }
