from src.enums.subscription_category import SubscriptionCategory
from src.enums.plan_type import PlanType
from src.enums.topup_type import TopupType
from src.constants.error_codes import ErrorCodes
from datetime import datetime
from src.constants.constant import DATE_FORMAT, INPUT_ONE, TWO, INPUT_TWO, THREE


def is_valid_date(given_date: str) -> bool:
    """Validates if the date is in the correct format."""
    try:
        datetime.strptime(given_date, DATE_FORMAT)
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
    if len(parts) < TWO or not is_valid_date(parts[INPUT_ONE]):
        print(ErrorCodes.INVALID_DATE)
        return
    return parts[INPUT_ONE]


def is_valid_add_topup(parts, subscription):
    if not subscription:
        print(ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.SUBSCRIPTIONS_NOT_FOUND)
        return None, None
    if len(parts) < THREE or not parts[INPUT_TWO].isdigit():
        print(ErrorCodes.ADD_TOPUP_FAILED)
        return None, None
    topup_name_input, months = parts[INPUT_ONE], int(parts[INPUT_TWO])
    topup_name = is_valid_topup_type(topup_name_input)
    if not topup_name:
        print(ErrorCodes.ADD_TOPUP_FAILED)
        return None, None
    return topup_name, months
