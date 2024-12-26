from src.enums.plan_type import PlanType
from src.enums.subscription_category import SubscriptionCategory
from src.constants import constant

# plan mapping for category and plan with details
PLAN_DETAILS = {
    SubscriptionCategory.MUSIC: {
        PlanType.FREE: {
            "cost": constant.MUSIC_FREE_PLAN_PRICE,
            "duration": constant.MUSIC_FREE_PLAN_VALIDITY,
        },
        PlanType.PERSONAL: {
            "cost": constant.MUSIC_PERSONAL_PLAN_PRICE,
            "duration": constant.MUSIC_PERSONAL_PLAN_VALIDITY,
        },
        PlanType.PREMIUM: {
            "cost": constant.MUSIC_PREMIUM_PLAN_PRICE,
            "duration": constant.MUSIC_PREMIUM_PLAN_VALIDITY,
        },
    },
    SubscriptionCategory.VIDEO: {
        PlanType.FREE: {
            "cost": constant.VIDEO_FREE_PLAN_PRICE,
            "duration": constant.VIDEO_FREE_PLAN_VALIDITY,
        },
        PlanType.PERSONAL: {
            "cost": constant.VIDEO_PERSONAL_PLAN_PRICE,
            "duration": constant.VIDEO_PERSONAL_PLAN_VALIDITY,
        },
        PlanType.PREMIUM: {
            "cost": constant.VIDEO_PREMIUM_PLAN_PRICE,
            "duration": constant.VIDEO_PREMIUM_PLAN_VALIDITY,
        },
    },
    SubscriptionCategory.PODCAST: {
        PlanType.FREE: {
            "cost": constant.PODCAST_FREE_PLAN_PRICE,
            "duration": constant.PODCAST_FREE_PLAN_VALIDITY,
        },
        PlanType.PERSONAL: {
            "cost": constant.PODCAST_PERSONAL_PLAN_PRICE,
            "duration": constant.PODCAST_PERSONAL_PLAN_VALIDITY,
        },
        PlanType.PREMIUM: {
            "cost": constant.PODCAST_PREMIUM_PLAN_PRICE,
            "duration": constant.PODCAST_PREMIUM_PLAN_VALIDITY,
        },
    },
}
