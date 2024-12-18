import unittest
from src.models.subscription import Subscription
from src.services.topup_service import TopupService
from src.enums.topup_type import TopupType
from src.constants.error_codes import ErrorCodes
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


class TestTopupService(unittest.TestCase):

    def setUp(self):
        self.subscription = Subscription(start_date="01-01-2024")
        self.service = TopupService(self.subscription)

    def test_add_topup_valid(self):
        self.subscription.plans["MUSIC"] = "FREE"
        result = self.service.add_topup(TopupType.FOUR_DEVICE, 2)
        self.assertIsNone(result)
        self.assertIsNotNone(self.subscription.topup)

    def test_add_topup_no_plans(self):
        result = self.service.add_topup(TopupType.FOUR_DEVICE, 2)
        self.assertEqual(
            result,
            ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.SUBSCRIPTION_NOT_FOUND,
        )

    def test_add_topup_duplicate(self):
        self.subscription.plans["MUSIC"] = "FREE"
        self.service.add_topup(TopupType.FOUR_DEVICE, 2)
        result = self.service.add_topup(TopupType.FOUR_DEVICE, 4)
        self.assertEqual(
            result, ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.DUPLICATE_TOPUP
        )


if __name__ == "__main__":
    unittest.main()
