import unittest
from unittest.mock import patch
from src.models.plan import Plan
from src.enums.plan_type import PlanType
from src.enums.subscription_category import SubscriptionCategory
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


# Test for Plan model
class TestPlan(unittest.TestCase):

    def setUp(self):
        self.plan = Plan()

    @patch(
        "src.models.plan.PLAN_DETAILS",
        {
            SubscriptionCategory.MUSIC: {
                PlanType.PERSONAL: {"cost": 100, "duration": 1},
                PlanType.PREMIUM: {"cost": 250, "duration": 3},
            }
        },
    )
    # Test valid plan type
    def test_is_valid_plan(self):
        self.assertEqual(self.plan.is_valid_plan("PERSONAL"), PlanType.PERSONAL)
        self.assertIsNone(self.plan.is_valid_plan("VIP"))  # Test invalid plan type

    # Add a plan and check if it was added to the plans dictionary
    def test_add_plan(self):
        self.plan.add_plan(SubscriptionCategory.MUSIC, PlanType.PERSONAL)
        plans = self.plan.get_plans()
        self.assertIn(SubscriptionCategory.MUSIC, plans)
        self.assertEqual(plans[SubscriptionCategory.MUSIC], PlanType.PERSONAL)

    # Add some plans and check if they are returned correctly
    def test_get_plans(self):
        self.plan.add_plan(SubscriptionCategory.MUSIC, PlanType.PERSONAL)
        self.plan.add_plan(SubscriptionCategory.VIDEO, PlanType.PREMIUM)
        plans = self.plan.get_plans()
        self.assertEqual(len(plans), 2)
        self.assertEqual(plans[SubscriptionCategory.MUSIC], PlanType.PERSONAL)
        self.assertEqual(plans[SubscriptionCategory.VIDEO], PlanType.PREMIUM)

    # Assert that the details match what we expect from PLAN_DETAILS
    def test_get_details_valid_plan(self):
        self.plan.add_plan(SubscriptionCategory.MUSIC, PlanType.PERSONAL)
        details = self.plan.get_plan_details(
            SubscriptionCategory.MUSIC, PlanType.PERSONAL
        )
        self.assertEqual(details["category"], SubscriptionCategory.MUSIC.value)
        self.assertEqual(details["plan_type"], PlanType.PERSONAL.value)
        self.assertEqual(details["cost"], 100)
        self.assertEqual(details["duration_in_months"], 1)


if __name__ == "__main__":
    unittest.main()
