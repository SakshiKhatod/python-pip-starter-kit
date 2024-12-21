from src.constants.error_codes import ErrorCodes
from src.models.subscription import Subscription
from src.enums.subscription_category import SubscriptionCategory
from src.enums.plan_type import PlanType
from dateutil.relativedelta import relativedelta
from datetime import datetime
from src.models.plan import Plan
from src.constants.constant import DATE_FORMAT, NO_OF_DAYS_BEFORE_TO_NOTIFY, ZERO


class SubscriptionService:

    def __init__(self):
        self.subscription = Subscription()
        self.plan = Plan()
        self.plans = {}
        self.start_date = None
        self.stop_execution = False

    def start_subscription(self, start_date):
        if not self.subscription.is_valid_date(start_date):
            return ErrorCodes.INVALID_DATE
        self.start_date = datetime.strptime(start_date, DATE_FORMAT)
        return None

    def add_plan(
        self, subscription_category: SubscriptionCategory, plan_type: PlanType
    ):
        self.plans[subscription_category] = plan_type

    def add_subscription(self, subscription_category: str, plan_type: str) -> str:
        if not self.start_date:
            self.stop_execution = True
            return ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.INVALID_DATE
        category_enum = self.subscription.is_valid_category(subscription_category)
        if not category_enum:
            self.stop_execution = True
            return f"{ErrorCodes.ADD_SUBSCRIPTION_FAILED} {ErrorCodes.INVALID_CATEGORY}"
        if category_enum in self.plans:
            self.stop_execution = True
            return (
                ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.DUPLICATE_CATEGORY
            )

        plan_type_enum = self.plan.is_valid_plan(plan_type)
        if not plan_type_enum:
            self.stop_execution = True
            return (
                f"{ErrorCodes.ADD_SUBSCRIPTION_FAILED} {ErrorCodes.INVALID_PLAN_TYPE}"
            )
        self.add_plan(category_enum, plan_type_enum)
        return None

    def calculate_renewal_dates(self) -> dict:
        renewal_dates = {}
        for category, plan_type in self.plans.items():
            if category in SubscriptionCategory and plan_type in PlanType:
                plan_details = self.plan.get_details(category, plan_type)
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

    def calculate_subscription_cost(self):
        total_subscription_cost = 0
        for category, plan_type in self.plans.items():
            if category in SubscriptionCategory and plan_type in PlanType:
                plan_details = self.plan.get_details(category, plan_type)
                total_subscription_cost += plan_details["cost"]
            else:
                print(ErrorCodes.INVALID_PLAN_DETAILS_MAPPING)
        return total_subscription_cost

    def get_subscriptions(self):
        return True if len(self.plans) > ZERO else False
