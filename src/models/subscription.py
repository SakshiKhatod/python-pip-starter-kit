from src.constants.error_codes import ErrorCodes
from src.enums.subscription_category import SubscriptionCategory
from src.enums.plan_type import PlanType
from dateutil.relativedelta import relativedelta
from datetime import datetime
from src.models.plan import Plan
from src.constants.constant import (
    DATE_FORMAT,
    NO_OF_DAYS_BEFORE_TO_NOTIFY,
    DEFAULT_PLAN_LENGTH,
)
from src.exceptions.subscription_exceptions import (
    InvalidDateException,
    InvalidCategoryException,
    DuplicateCategoryException,
    InvalidPlanTypeException,
    InvalidOnlyDateException,
)


class Subscription:
    """Class to start, add subscription with their renewal date and total subscription cost"""

    def __init__(self):
        self._plan = Plan()  # Private attribute for Plan instance
        self._start_date = None

    def _is_valid_date(self, given_date: str) -> bool:
        """Private method to validate a given date."""
        try:
            datetime.strptime(given_date, DATE_FORMAT)
            return True
        except ValueError:
            return False

    def _validate_start_date(self):
        """Method to check the start date is valid. and throw exception"""
        if not self.is_start_date_valid():
            raise InvalidDateException(f"{ErrorCodes.INVALID_DATE_EXCEPTION_MESSAGE}")

    def is_valid_plan_type(self, plan_type: str):
        """Private method to validate a subscription plan type."""
        return self._validate_enum(PlanType, plan_type, InvalidPlanTypeException)

    def _is_valid_category(self, category: str) -> SubscriptionCategory:
        """Private method to validate a subscription category."""
        return self._validate_enum(
            SubscriptionCategory, category, InvalidCategoryException
        )

    def _validate_enum(self, enum_class, value: str, exception_class):
        """Method to convert str to enums to avoid repetition."""
        try:
            return enum_class[value]
        except KeyError:
            raise exception_class(f"{ErrorCodes.INVALID_CATEGORY_EXCEPTION_MESSAGE}")

    def is_start_date_valid(self) -> bool:
        """Public method to check if the subscription start date is set and valid."""
        return self._start_date is not None

    def _iterate_plans(self):
        """Private method to iterate through and return plan details."""
        plans = self._plan.get_plans()
        return [
            (category, plan_type, self._get_plan_details(category, plan_type))
            for category, plan_type in plans.items()
            if self._is_valid_plan(category, plan_type)
        ]

    def _get_plan_details(self, category, plan_type):
        """Method to fetch plan details."""
        return self._plan.get_plan_details(category, plan_type)

    def _is_valid_plan(self, category, plan_type):
        """Method to validate both category and plan type existence."""
        if category not in SubscriptionCategory or plan_type not in PlanType:
            print(ErrorCodes.INVALID_PLAN_DETAILS_MAPPING)
            return False
        return True

    def start_subscription(self, start_date: str):
        """Start subscription from a given date."""
        if not self._is_valid_date(start_date):
            raise InvalidOnlyDateException(ErrorCodes.INVALID_DATE)
        self._start_date = datetime.strptime(start_date, DATE_FORMAT)

    def _validate_and_add_subscription(
        self, subscription_category: str, plan_type: str
    ):
        """Method to validate category and add plan to prevent code duplication."""
        category_enum = self._is_valid_category(subscription_category)
        if category_enum in self._plan.get_plans():
            raise DuplicateCategoryException(
                f"{ErrorCodes.DUPLICATE_CATEGORY_EXCEPTION_MESSAGE}"
            )
        plan_type_enum = self.is_valid_plan_type(plan_type)
        self._plan.add_plan(category_enum, plan_type_enum)

    def add_subscription(self, subscription_category: str, plan_type: str):
        """Add a subscription with a given category and plan type."""
        self._validate_start_date()
        self._validate_and_add_subscription(subscription_category, plan_type)

    def calculate_renewal_dates(self) -> dict:
        """Calculate renewal dates for all subscriptions."""
        renewal_dates = {}
        for category, _, plan_details in self._iterate_plans():
            renewal_date = self._start_date + relativedelta(
                months=plan_details["duration_in_months"]
            )
            reminder_date = renewal_date - relativedelta(
                days=NO_OF_DAYS_BEFORE_TO_NOTIFY
            )
            renewal_dates[category.value] = reminder_date.strftime(DATE_FORMAT)
        return renewal_dates

    def calculate_subscription_cost(self) -> int:
        """Calculate the total cost of all subscriptions."""
        return sum(plan_details["cost"] for _, _, plan_details in self._iterate_plans())

    def get_subscriptions(self) -> bool:
        """Check if there are any active subscriptions."""
        return len(self._plan.get_plans()) > DEFAULT_PLAN_LENGTH
