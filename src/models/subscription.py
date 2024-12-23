from src.constants.error_codes import ErrorCodes
from src.enums.subscription_category import SubscriptionCategory
from src.enums.plan_type import PlanType
from dateutil.relativedelta import relativedelta
from datetime import datetime
from src.models.plan import Plan
from src.constants.constant import DATE_FORMAT, NO_OF_DAYS_BEFORE_TO_NOTIFY, ZERO
from src.exceptions.subscription_exceptions import (
    InvalidDateException,
    InvalidCategoryException,
    DuplicateCategoryException,
    InvalidPlanTypeException,
)


# Subscription class where subscriptions can be added,cost calulated and retrieved
class Subscription:

    def __init__(self):
        self.plan = Plan()
        self.start_date = None

    def is_valid_date(self, given_date: str) -> bool:
        try:
            datetime.strptime(given_date, DATE_FORMAT)
            return True
        except ValueError:
            return False

    def start_subscription(self, start_date: str):
        if not self.is_valid_date(start_date):
            raise InvalidDateException(ErrorCodes.INVALID_DATE)
        self.start_date = datetime.strptime(start_date, DATE_FORMAT)
        return None

    def is_valid_category(self, category: str) -> SubscriptionCategory:
        try:
            return SubscriptionCategory[category]
        except KeyError:
            return None

    def add_subscription(self, subscription_category: str, plan_type: str) -> str:
        if not self.start_date:
            raise InvalidDateException(
                ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.INVALID_DATE
            )

        category_enum = self.is_valid_category(subscription_category)
        if not category_enum:
            raise InvalidCategoryException(
                f"{ErrorCodes.ADD_SUBSCRIPTION_FAILED} {ErrorCodes.INVALID_CATEGORY}"
            )

        if category_enum in self.plan.get_plans():
            raise DuplicateCategoryException(
                ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.DUPLICATE_CATEGORY
            )

        plan_type_enum = self.plan.is_valid_plan(plan_type)
        if not plan_type_enum:
            raise InvalidPlanTypeException(
                f"{ErrorCodes.ADD_SUBSCRIPTION_FAILED} {ErrorCodes.INVALID_PLAN_TYPE}"
            )

        self.plan.add_plan(category_enum, plan_type_enum)
        return None

    def calculate_renewal_dates(self) -> dict:
        renewal_dates = {}
        plans = self.plan.get_plans()
        for category, plan_type in plans.items():
            if category in SubscriptionCategory and plan_type in PlanType:
                plan_details = self.plan.get_plan_details(category, plan_type)
                renewal_date = self.start_date + relativedelta(
                    months=plan_details["duration_in_months"]
                )
                reminder_date = renewal_date - relativedelta(
                    days=NO_OF_DAYS_BEFORE_TO_NOTIFY
                )
                renewal_dates[category.value] = reminder_date.strftime(DATE_FORMAT)
            else:
                print(ErrorCodes.INVALID_PLAN_DETAILS_MAPPING)
        return renewal_dates

    def calculate_subscription_cost(self) -> int:
        total_subscription_cost = 0
        plans = self.plan.get_plans()
        for category, plan_type in plans.items():
            if category in SubscriptionCategory and plan_type in PlanType:
                plan_details = self.plan.get_plan_details(category, plan_type)
                total_subscription_cost += plan_details["cost"]
            else:
                print(ErrorCodes.INVALID_PLAN_DETAILS_MAPPING)
        return total_subscription_cost

    def get_subscriptions(self) -> bool:
        return True if len(self.plan.get_plans()) > ZERO else False
