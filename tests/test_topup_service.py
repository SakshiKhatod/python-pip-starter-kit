import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import unittest
from src.constants.error_codes import ErrorCodes
from src.services.topup_service import TopupService
from unittest.mock import patch, MagicMock


class TestTopupService(unittest.TestCase):

    def setUp(self):
        self.topup_service = TopupService()

    # Test when no topup
    def test_add_topup_no_topup(self):
        with patch("src.services.topup_service.Topup") as MockTopup:
            mock_topup_instance = MagicMock()
            MockTopup.return_value = mock_topup_instance
            mock_topup_instance.is_valid_topup.return_value = True
            mock_topup_instance.calculate_cost.return_value = None

            result = self.topup_service.add_topup("FOUR_DEVICE", 3)
            self.assertIsNone(result)
            mock_topup_instance.is_valid_topup.assert_called_once_with("FOUR_DEVICE", 3)
            mock_topup_instance.calculate_cost.assert_called_once()

    # Test when duplicate toup type
    def test_add_topup_duplicate_topup(self):
        self.topup_service.topup = MagicMock()  # Simulate an existing top-up
        result = self.topup_service.add_topup("FOUR_DEVICE", 3)
        self.assertTrue(self.topup_service.stop_execution)
        self.assertEqual(
            result, f"{ErrorCodes.ADD_TOPUP_FAILED} {ErrorCodes.DUPLICATE_TOPUP}"
        )

    # Test when invalid topup type
    def test_add_topup_invalid_topup_type(self):
        with patch("src.services.topup_service.Topup") as MockTopup:
            mock_topup_instance = MagicMock()
            MockTopup.return_value = mock_topup_instance
            mock_topup_instance.is_valid_topup.return_value = (
                False  # Simulate invalid top-up type
            )

            result = self.topup_service.add_topup("SIX_DEVICE", 3)

            self.assertTrue(self.topup_service.stop_execution)
            self.assertEqual(
                result, f"{ErrorCodes.ADD_TOPUP_FAILED} {ErrorCodes.INVALID_TOPUP_TYPE}"
            )

    # Test to calculate topup cost when no topup is added
    def test_calculate_topup_cost_no_topup(self):
        self.topup_service.topup = None
        result = self.topup_service.calculate_topup_cost()
        self.assertEqual(result, 0)

    # Test when a top-up has been added
    def test_calculate_topup_cost_with_topup(self):
        self.topup_service.topup = MagicMock()
        self.topup_service.topup.cost = 100
        result = self.topup_service.calculate_topup_cost()
        self.assertEqual(result, 100)


if __name__ == "__main__":
    unittest.main()
