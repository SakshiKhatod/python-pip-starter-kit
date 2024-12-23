import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import unittest
from src.enums.topup_type import TopupType
from src.exceptions.topup_exceptions import InvalidTopupTypeError, DuplicateTopupError
from src.models.topup import Topup


class TestTopup(unittest.TestCase):

    def setUp(self):
        """Set up a fresh Topup instance before each test."""
        self.topup = Topup()

    # Test for a valid topup type
    def test_is_valid_topup_type_valid(self):
        self.assertTrue(self.topup.is_valid_topup_type(TopupType.FOUR_DEVICE.value))

    # Test for invalid topup type
    def test_is_valid_topup_type_invalid(self):
        self.assertFalse(self.topup.is_valid_topup_type("SIX_DEVICE"))

    # Test adding a valid topup and calculating cost
    def test_add_topup_valid(self):
        self.topup.add_topup(TopupType.FOUR_DEVICE.value, 3)
        self.assertEqual(self.topup.topup_type, TopupType.FOUR_DEVICE)
        self.assertEqual(self.topup.duration, 3)
        self.assertEqual(self.topup.cost, 150)

    # Test if InvalidTopupTypeError is raised for invalid topup type
    def test_add_topup_invalid_topup_type(self):
        with self.assertRaises(InvalidTopupTypeError):
            self.topup.add_topup("SIX_DEVICE", 3)

    # Test if DuplicateTopupError is raised when trying to add a topup again
    def test_add_topup_duplicate_topup(self):
        self.topup.add_topup(TopupType.FOUR_DEVICE.value, 3)
        with self.assertRaises(DuplicateTopupError):
            self.topup.add_topup(TopupType.FOUR_DEVICE.value, 2)

    # Test if the cost is correctly calculated based on topup type and duration
    def test_calculate_cost(self):
        self.topup.add_topup(TopupType.FOUR_DEVICE.value, 3)
        self.assertEqual(self.topup.cost, 150)

    # Test getting the topup cost
    def test_get_topup_cost(self):
        self.topup.add_topup(TopupType.FOUR_DEVICE.value, 3)
        self.assertEqual(self.topup.get_topup_cost(), 150)


if __name__ == "__main__":
    unittest.main()
