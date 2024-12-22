import unittest
from src.constants.constant import DATE_FORMAT, NO_OF_DAYS_BEFORE_TO_NOTIFY
from src.services.subscription_service import SubscriptionService
from src.enums.subscription_category import SubscriptionCategory
from src.enums.plan_type import PlanType
from src.constants.error_codes import ErrorCodes
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import unittest
from datetime import datetime
from unittest.mock import MagicMock
from dateutil.relativedelta import relativedelta


class TestSubscriptionService(unittest.TestCase):

    def setUp(self):
        self.service = SubscriptionService()
        self.service.subscription.is_valid_date = MagicMock()
        self.service.subscription.is_valid_category = MagicMock()
        self.service.plan.is_valid_plan = MagicMock()
        self.service.plan.get_details = MagicMock()

    def test_start_subscription_invalid_date(self):
        self.service.subscription.is_valid_date.return_value = False
        result = self.service.start_subscription("2024-12-32")
        self.assertEqual(result, ErrorCodes.INVALID_DATE)

    def test_start_subscription_valid_date(self):
        self.service.subscription.is_valid_date.return_value = True
        result = self.service.start_subscription("22-12-2024")
        self.assertIsNone(result)
        self.assertEqual(
            self.service.start_date, datetime.strptime("22-12-2024", DATE_FORMAT)
        )

    def test_add_plan(self):
        self.service.add_plan(SubscriptionCategory.MUSIC, PlanType.FREE)
        self.assertIn(SubscriptionCategory.MUSIC, self.service.plans)
        self.assertEqual(self.service.plans[SubscriptionCategory.MUSIC], PlanType.FREE)

    def test_add_subscription_no_start_date(self):
        self.service.start_date = None
        result = self.service.add_subscription("MUSIC", "FREE")
        self.assertTrue(self.service.stop_execution)
        self.assertEqual(
            result, ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.INVALID_DATE
        )

    def test_add_subscription_invalid_category(self):
        self.service.start_date = "22-12-2024"
        self.service.subscription.is_valid_category.return_value = None
        result = self.service.add_subscription("STREAM", "PERSONAL")
        self.assertTrue(self.service.stop_execution)
        self.assertEqual(
            result,
            f"{ErrorCodes.ADD_SUBSCRIPTION_FAILED} {ErrorCodes.INVALID_CATEGORY}",
        )

    def test_add_subscription_duplicate_category(self):
        self.service.start_date = "22-12-2024"
        self.service.subscription.is_valid_category.return_value = (
            SubscriptionCategory.MUSIC
        )
        self.service.plans[SubscriptionCategory.MUSIC] = PlanType.PREMIUM
        result = self.service.add_subscription("MUSIC", "FREE")
        self.assertTrue(self.service.stop_execution)
        self.assertEqual(
            result,
            ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.DUPLICATE_CATEGORY,
        )

    def test_add_subscription_invalid_plan_type(self):
        self.service.start_date = "22-12-2024"
        self.service.subscription.is_valid_category.return_value = (
            SubscriptionCategory.MUSIC
        )
        self.service.plan.is_valid_plan.return_value = None
        result = self.service.add_subscription("MUSIC", "VIP")
        self.assertTrue(self.service.stop_execution)
        self.assertEqual(
            result,
            f"{ErrorCodes.ADD_SUBSCRIPTION_FAILED} {ErrorCodes.INVALID_PLAN_TYPE}",
        )

    def test_add_subscription_success(self):
        self.service.start_date = "22-12-2024"
        self.service.subscription.is_valid_category.return_value = (
            SubscriptionCategory.PODCAST
        )
        self.service.plan.is_valid_plan.return_value = PlanType.PREMIUM
        self.service.add_subscription("PODCAST", "PREMIUM")
        self.assertIn(SubscriptionCategory.PODCAST, self.service.plans)
        self.assertEqual(
            self.service.plans[SubscriptionCategory.PODCAST], PlanType.PREMIUM
        )

    def test_calculate_renewal_dates(self):
        self.service.start_date = datetime.strptime("22-12-2024", DATE_FORMAT)
        self.service.plan.get_details.return_value = {
            "duration_in_months": 3,
            "cost": 500,
        }
        self.service.plans = {SubscriptionCategory.VIDEO: PlanType.PREMIUM}
        renewal_dates = self.service.calculate_renewal_dates()
        self.assertIn(SubscriptionCategory.VIDEO.value, renewal_dates)
        expected_date = (
            self.service.start_date
            + relativedelta(months=3)
            - relativedelta(days=NO_OF_DAYS_BEFORE_TO_NOTIFY)
        ).strftime(DATE_FORMAT)
        self.assertEqual(renewal_dates[SubscriptionCategory.VIDEO.value], expected_date)

    def test_calculate_subscription_cost(self):
        self.service.plan.get_details.return_value = {
            "duration_in_months": 1,
            "cost": 200,
        }
        self.service.plans = {SubscriptionCategory.VIDEO: PlanType.PERSONAL}
        total_cost = self.service.calculate_subscription_cost()
        self.assertEqual(total_cost, 200)

    def test_get_subscriptions_with_subscriptions(self):
        self.service.plans = {SubscriptionCategory.MUSIC: PlanType.PREMIUM}
        result = self.service.get_subscriptions()
        self.assertTrue(result)

    def test_get_subscriptions_no_subscriptions(self):
        self.service.plans = {}
        result = self.service.get_subscriptions()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
