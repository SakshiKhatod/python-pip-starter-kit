import unittest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.models.subscription import Subscription
from src.enums.subscription_category import SubscriptionCategory
from src.enums.plan_type import PlanType
from src.exceptions.subscription_exceptions import (
    InvalidDateException,
    InvalidCategoryException,
    DuplicateCategoryException,
    InvalidPlanTypeException,
)
from src.models.plan import Plan
from dateutil.relativedelta import relativedelta
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


# Test for Subscription model
class TestSubscription(unittest.TestCase):

    def setUp(self):
        """Set up a fresh Subscription and Plan instance before each test."""
        self.subscription = Subscription()
        self.plan = Plan()
        self.plan.add_plan(SubscriptionCategory.MUSIC, PlanType.PERSONAL)
        self.subscription.plan = self.plan

    # Test to check whether subscription date is valid
    def test_start_subscription_valid_date(self):
        start_date = "20-02-2022"
        result = self.subscription.start_subscription(start_date)
        self.assertIsNone(result)
        self.assertEqual(
            self.subscription.start_date, datetime.strptime(start_date, "%d-%m-%Y")
        )

    # Test to check if proper invalid date exception is occured
    def test_start_subscription_invalid_date(self):
        start_date = "2022-02-20"
        with self.assertRaises(InvalidDateException):
            self.subscription.start_subscription(start_date)

    # Test adding a subscription when the start date is not set
    def test_add_subscription_invalid_date(self):
        with self.assertRaises(InvalidDateException):
            self.subscription.add_subscription(
                SubscriptionCategory.MUSIC.value, PlanType.PERSONAL.value
            )

    # Test adding a subscription with an invalid category
    def test_add_subscription_invalid_category(self):
        start_date = "20-02-2022"
        self.subscription.start_subscription(start_date)
        with self.assertRaises(InvalidCategoryException):
            self.subscription.add_subscription("STREAM", PlanType.PERSONAL.value)

    # Test adding a subscription with a duplicate category
    def test_add_subscription_duplicate_category(self):
        start_date = "20-02-2022"
        self.subscription.start_subscription(start_date)
        self.plan.get_plans = lambda: {SubscriptionCategory.MUSIC: PlanType.PERSONAL}
        with self.assertRaises(DuplicateCategoryException):
            self.subscription.add_subscription(
                SubscriptionCategory.MUSIC.value, PlanType.PERSONAL
            )

    # Test adding a subscription with an invalid plan type
    def test_add_subscription_invalid_plan_type(self):
        start_date = "20-02-2022"
        self.subscription.start_subscription(start_date)
        self.plan.get_plans = lambda: {}  # No plans added yet
        with self.assertRaises(InvalidPlanTypeException):
            self.subscription.add_subscription(SubscriptionCategory.MUSIC.value, "VIP")

    # Test calculating renewal dates
    def test_calculate_renewal_dates(self):
        start_date = "20-02-2022"
        self.subscription.start_subscription(start_date)
        self.plan.get_plans = lambda: {SubscriptionCategory.MUSIC: PlanType.PERSONAL}
        self.subscription.plan.get_details = lambda category, plan_type: {
            "cost": 100,
            "duration_in_months": 1,
        }
        renewal_dates = self.subscription.calculate_renewal_dates()
        self.assertEqual(
            renewal_dates[SubscriptionCategory.MUSIC.value],
            (
                datetime.strptime(start_date, "%d-%m-%Y")
                + relativedelta(months=1)
                - relativedelta(days=10)
            ).strftime("%d-%m-%Y"),
        )

    # Test calculating the total cost of subscriptions
    def test_calculate_subscription_cost(self):
        start_date = "20-02-2022"
        self.subscription.start_subscription(start_date)
        self.plan.get_plans = lambda: {SubscriptionCategory.MUSIC: PlanType.PERSONAL}
        self.subscription.plan.get_details = lambda category, plan_type: {
            "cost": 100,
            "duration_in_months": 1,
        }
        total_cost = self.subscription.calculate_subscription_cost()
        self.assertEqual(total_cost, 100)

    # Test if subscriptions exist
    def test_get_subscriptions(self):
        start_date = "20-02-2022"
        self.subscription.start_subscription(start_date)
        self.plan.get_plans = lambda: {SubscriptionCategory.MUSIC: PlanType.PERSONAL}
        self.assertTrue(self.subscription.get_subscriptions())
        # Test when no subscriptions exist
        self.plan.get_plans = lambda: {}
        self.assertFalse(self.subscription.get_subscriptions())


if __name__ == "__main__":
    unittest.main()
