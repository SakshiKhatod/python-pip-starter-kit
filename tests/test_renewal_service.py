import unittest
from src.models.subscription import Subscription
from src.services.renewal_service import RenewalService
from src.enums.subscription_category import SubscriptionCategory
from src.models.plan import Plan
from src.enums.plan_type import PlanType

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


class TestRenewalService(unittest.TestCase):

    def setUp(self):
        self.subscription = Subscription(start_date="20-02-2022")
        self.subscription.plans[SubscriptionCategory.MUSIC] = Plan(
            PlanType.PERSONAL, SubscriptionCategory.MUSIC
        )
        self.service = RenewalService(self.subscription)

    def test_calculate_renewal_dates(self):
        renewal_dates = self.service.calculate_renewal_dates()
        self.assertIn(SubscriptionCategory.MUSIC, renewal_dates)
        self.assertEqual(renewal_dates[SubscriptionCategory.MUSIC], "10-03-2022")

    def test_calculate_total_cost(self):
        total_cost = self.service.calculate_total_cost()
        self.assertEqual(total_cost, 100)

    def test_get_renewal_details(self):
        details = self.service.get_renewal_details()
        self.assertIn("RENEWAL_REMINDER MUSIC 10-03-2022", details)
        self.assertIn("RENEWAL_AMOUNT 100", details)


if __name__ == "__main__":
    unittest.main()
