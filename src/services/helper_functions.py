from src.enums.subscription_category import SubscriptionCategory
from src.enums.plan_type import PlanType
from src.enums.topup_type import TopupType
from src.constants.error_codes import ErrorCodes
from datetime import datetime
from src.constants.constant import date_format


def is_valid_date(given_date: str) -> bool:
    """Validates if the date is in the correct format."""
    try:
        datetime.strptime(given_date, date_format)
        return True
    except ValueError:
        return False


def is_valid_category(category: str) -> SubscriptionCategory:
    """Validates if the given category exists in SubscriptionCategory."""
    try:
        return SubscriptionCategory[category]
    except KeyError:
        print(ErrorCodes.INVALID_CATEGORY)
        return None


def is_valid_plan_type(plan_type: str) -> PlanType:
    """Validates if the given plan type exists in PlanType."""
    try:
        return PlanType[plan_type]
    except KeyError:
        print(ErrorCodes.INVALID_PLAN_TYPE)
        return None


def is_valid_topup_type(topup_type: str) -> TopupType:
    """Validates if the given topup type exists in TopupType."""
    try:
        return TopupType[topup_type]
    except KeyError:
        print(ErrorCodes.INVALID_TOPUP_TYPE)
        return None


def is_valid_start_subscription(parts):
    if len(parts) < 2 or not is_valid_date(parts[1]):
        print(ErrorCodes.INVALID_DATE)
        return
    return parts[1]


def is_valid_add_topup(parts, subscription):
    if not subscription:
        print(ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.SUBSCRIPTION_NOT_FOUND)
        return None, None
    if len(parts) < 3 or not parts[2].isdigit():
        print(ErrorCodes.ADD_TOPUP_FAILED)
        return None, None
    topup_name_input, months = parts[1], int(parts[2])
    topup_name = is_valid_topup_type(topup_name_input)
    if not topup_name:
        print(ErrorCodes.ADD_TOPUP_FAILED)
        return None, None
    return topup_name, months


def is_valid_add_subscription(
    subscription, start_date, category_input, plan_type_input
):
    if not subscription:
        print(
            ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.SUBSCRIPTION_NOT_FOUND
        )
        return None, None
    if not start_date:
        print(ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.INVALID_DATE)
        return None, None
    category = is_valid_category(category_input)
    plan_type = is_valid_plan_type(plan_type_input)
    if not category or not plan_type:
        print(ErrorCodes.ADD_SUBSCRIPTION_FAILED + " INVALID_CATEGORY_OR_PLAN")
        return None, None
    return category, plan_type
