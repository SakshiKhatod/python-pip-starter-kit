from src.enums.plan_type import PlanType
from src.enums.subscription_category import SubscriptionCategory

PLAN_DETAILS = {
    SubscriptionCategory.MUSIC: {
        PlanType.FREE: {"cost": 0, "duration": 1},
        PlanType.PERSONAL: {"cost": 100, "duration": 1},
        PlanType.PREMIUM: {"cost": 250, "duration": 3},
    },
    SubscriptionCategory.VIDEO: {
        PlanType.FREE: {"cost": 0, "duration": 1},
        PlanType.PERSONAL: {"cost": 200, "duration": 1},
        PlanType.PREMIUM: {"cost": 500, "duration": 3},
    },
    SubscriptionCategory.PODCAST: {
        PlanType.FREE: {"cost": 0, "duration": 1},
        PlanType.PERSONAL: {"cost": 100, "duration": 1},
        PlanType.PREMIUM: {"cost": 300, "duration": 3},
    },
}
