import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import unittest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.models.subscription import Subscription
from src.enums.subscription_category import SubscriptionCategory
from src.enums.plan_type import PlanType
from src.exceptions.subscription_exceptions import (
    InvalidCategoryException,
    DuplicateCategoryException,
    InvalidPlanTypeException,
    InvalidOnlyDateException,
)
from src.constants.constant import DATE_FORMAT


# Test for subscription model
class TestSubscription(unittest.TestCase):
    """Unit tests for the Subscription model."""

    def setUp(self):
        """Set up fresh Subscription instances before each test."""
        self.subscription = Subscription()
        self.start_date = "20-02-2022"

    def test_start_subscription_valid_date(self):
        """Test to start a subscription with a valid date."""
        self.subscription.start_subscription(self.start_date)
        expected_date = datetime.strptime(self.start_date, DATE_FORMAT)
        self.assertEqual(self.subscription._start_date, expected_date)

    def test_start_subscription_invalid_date(self):
        """Test to start a subscription with an invalid date format."""
        invalid_start_date = "2022-20-02"
        with self.assertRaises(InvalidOnlyDateException):
            self.subscription.start_subscription(invalid_start_date)

    def test_add_subscription_valid(self):
        """Test to add a valid subscription."""
        self.subscription.start_subscription(self.start_date)
        self.subscription.add_subscription(
            SubscriptionCategory.MUSIC.value, PlanType.PERSONAL.value
        )
        plans = self.subscription._plan.get_plans()
        self.assertIn(SubscriptionCategory.MUSIC, plans)
        self.assertEqual(plans[SubscriptionCategory.MUSIC], PlanType.PERSONAL)

    def test_add_subscription_invalid_category(self):
        """Test to check an invalid category while adding a subscription"""
        self.subscription.start_subscription(self.start_date)
        with self.assertRaises(InvalidCategoryException):
            self.subscription.add_subscription(
                "INVALID_CATEGORY", PlanType.PERSONAL.value
            )

    def test_add_subscription_invalid_plan_type(self):
        """Test to check invalid plan type while adding a subscription"""
        self.subscription.start_subscription(self.start_date)
        with self.assertRaises(InvalidPlanTypeException):
            self.subscription.add_subscription(SubscriptionCategory.MUSIC.value, "VIP")

    def test_add_subscription_duplicate_category(self):
        """Test to check duplicate category while adding a subscription"""
        self.subscription.start_subscription(self.start_date)
        self.subscription.add_subscription(
            SubscriptionCategory.MUSIC.value, PlanType.PERSONAL.value
        )
        with self.assertRaises(DuplicateCategoryException):
            self.subscription.add_subscription(
                SubscriptionCategory.MUSIC.value, PlanType.PERSONAL.value
            )

    def test_calculate_renewal_dates(self):
        """Test to calculate renewal dates for subscriptions."""
        self.subscription.start_subscription(self.start_date)
        self.subscription.add_subscription(
            SubscriptionCategory.MUSIC.value, PlanType.PERSONAL.value
        )
        renewal_dates = self.subscription.calculate_renewal_dates()
        expected_date = (
            datetime.strptime(self.start_date, DATE_FORMAT)
            + relativedelta(months=1)
            - relativedelta(days=10)
        ).strftime(DATE_FORMAT)
        self.assertEqual(renewal_dates[SubscriptionCategory.MUSIC.value], expected_date)

    def test_calculate_subscription_cost(self):
        """Test to calculate the total cost of subscriptions."""
        self.subscription.start_subscription(self.start_date)
        self.subscription.add_subscription(
            SubscriptionCategory.MUSIC.value, PlanType.PERSONAL.value
        )
        total_cost = self.subscription.calculate_subscription_cost()
        self.assertEqual(total_cost, 100)

    def test_get_subscriptions(self):
        """Test to retrieve subscriptions."""
        self.subscription.start_subscription(self.start_date)
        self.subscription.add_subscription(
            SubscriptionCategory.MUSIC.value, PlanType.PERSONAL.value
        )
        self.assertTrue(self.subscription.get_subscriptions())

    def test_get_subscriptions_empty(self):
        """Test to get subscriptions when there are none."""
        self.assertFalse(self.subscription.get_subscriptions())


if __name__ == "__main__":
    unittest.main()
