from enum import Enum
from src.constants.constant import (
    TOPUP_PLAN_FOUR_DEVICE_PRICE_PER_MONTH,
    TOPUP_PLAN_TEN_DEVICE_PRICE_PER_MONTH,
    TOPUP_PLAN_FOUR_DEVICE_DURATION,
    TOPUP_PLAN_TEN_DEVICE_DURATION,
    TOPUP_PLAN_FOUR_DEVICE,
    TOPUP_PLAN_TEN_DEVICE,
)


# Enums for type of topup
class TopupType(Enum):
    FOUR_DEVICE = "FOUR_DEVICE"
    TEN_DEVICE = "TEN_DEVICE"

    def get_details(self):
        details = {
            TopupType.FOUR_DEVICE: {
                "cost": TOPUP_PLAN_FOUR_DEVICE_PRICE_PER_MONTH,
                "duration": TOPUP_PLAN_FOUR_DEVICE_DURATION,
                "devices": TOPUP_PLAN_FOUR_DEVICE,
            },
            TopupType.TEN_DEVICE: {
                "cost": TOPUP_PLAN_TEN_DEVICE_PRICE_PER_MONTH,
                "duration": TOPUP_PLAN_TEN_DEVICE_DURATION,
                "devices": TOPUP_PLAN_TEN_DEVICE,
            },
        }
        return details[self]
