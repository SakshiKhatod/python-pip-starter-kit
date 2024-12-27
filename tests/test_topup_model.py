import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import unittest
from src.enums.topup_type import TopupType
from src.exceptions.topup_exceptions import (
    InvalidTopupTypeError,
    DuplicateTopupError,
    InvalidTopupDurationError,
)
from src.constants.constant import TOPUP_COST_ZERO
from src.models.topup import Topup


# Test for topup model
class TestTopup(unittest.TestCase):

    def setUp(self):
        """Set up a fresh Topup instance before each test."""
        self.topup = Topup()

    def test_add_topup_valid(self):
        """Test adding a valid topup and calculating cost."""
        self.topup.add_topup(TopupType.FOUR_DEVICE.value, 3)  # Adding valid topup
        self.assertEqual(
            self.topup._topup_type, TopupType.FOUR_DEVICE
        )  # Indirectly check topup type
        self.assertEqual(self.topup._duration, 3)  # Check duration
        self.assertEqual(
            self.topup.get_topup_cost(), 150
        )  # Assuming cost for FOUR_DEVICE * 3 months

    def test_add_topup_invalid_type(self):
        """Test adding an invalid topup type."""
        with self.assertRaises(InvalidTopupTypeError):
            self.topup.add_topup("INVALID_TYPE", 3)  # Invalid topup type

    def test_add_duplicate_topup(self):
        """Test adding a duplicate topup raises DuplicateTopupError."""
        self.topup.add_topup(TopupType.FOUR_DEVICE.value, 3)
        with self.assertRaises(DuplicateTopupError):
            self.topup.add_topup(TopupType.FOUR_DEVICE.value, 2)  # Trying to add again

    def test_add_topup_invalid_duration(self):
        """Test adding a topup with an invalid duration."""
        with self.assertRaises(InvalidTopupDurationError):
            self.topup.add_topup(TopupType.FOUR_DEVICE.value, -1)  # Invalid duration

    def test_get_topup_cost_zero_when_no_topup(self):
        """Test that the cost is zero when no topup is added."""
        self.assertEqual(self.topup.get_topup_cost(), TOPUP_COST_ZERO)

    def test_get_topup_cost_with_topup(self):
        """Test that the cost is calculated correctly for a valid topup."""
        self.topup.add_topup(TopupType.FOUR_DEVICE.value, 3)
        self.assertEqual(
            self.topup.get_topup_cost(), 150
        )  # Assuming cost is 50 per month


if __name__ == "__main__":
    unittest.main()
