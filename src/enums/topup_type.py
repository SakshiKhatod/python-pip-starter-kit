from enum import Enum


class TopupType(Enum):
    FOUR_DEVICE = "FOUR_DEVICE"
    TEN_DEVICE = "TEN_DEVICE"

    def get_details(self):
        details = {
            TopupType.FOUR_DEVICE: {"cost": 50, "duration": 1, "devices": 4},
            TopupType.TEN_DEVICE: {"cost": 100, "duration": 1, "devices": 10},
        }
        return details[self]
