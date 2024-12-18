from src.constants.plan_mapping import PLAN_DETAILS
from src.enums.plan_type import PlanType
from src.enums.subscription_category import SubscriptionCategory
from src.constants.error_codes import ErrorCodes


class Plan:
    def __init__(self, plan_type: PlanType, category: SubscriptionCategory):
        if plan_type.name not in PlanType.__members__:
            raise ValueError(ErrorCodes.INVALID_PLAN_TYPE)
        if category.name not in SubscriptionCategory.__members__:
            raise ValueError(ErrorCodes.INVALID_CATEGORY)

        try:
            plan_details = PLAN_DETAILS[category][plan_type]
        except KeyError:
            raise ValueError(ErrorCodes.INVALID_PLAN_DETAILS_MAPPING)

        self.category = category
        self.plan_type = plan_type
        self.cost = plan_details["cost"]
        self.duration = plan_details["duration"]

    def get_details(self):
        """Return plan details in a dictionary format."""
        return {
            "category": self.category.name,
            "plan_type": self.plan_type.name,
            "cost": self.cost,
            "duration_in_months": self.duration,
        }
