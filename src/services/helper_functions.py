from src.enums.subscription_category import SubscriptionCategory
from src.enums.plan_type import PlanType
from src.enums.topup_type import TopupType
from src.constants.error_codes import ErrorCodes
from datetime import datetime


def validate_date(given_date: str) -> bool:
    """Validates if the date is in the correct format."""
    try:
        datetime.strptime(given_date, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def validate_category(category: str) -> SubscriptionCategory:
    """Validates if the given category exists in SubscriptionCategory."""
    try:
        return SubscriptionCategory[category]
    except KeyError:
        print(ErrorCodes.INVALID_CATEGORY)
        return None


def validate_plan_type(plan_type: str) -> PlanType:
    """Validates if the given plan type exists in PlanType."""
    try:
        return PlanType[plan_type]
    except KeyError:
        print(ErrorCodes.INVALID_PLAN_TYPE)
        return None


def validate_topup_type(topup_type: str) -> TopupType:
    """Validates if the given topup type exists in TopupType."""
    try:
        return TopupType[topup_type]
    except KeyError:
        print(ErrorCodes.INVALID_TOPUP_TYPE)
        return None
