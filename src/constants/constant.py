# constants used in overall application
ZERO = 0
ONE = 1
TWO = 2
THREE = 3
INPUT_ZERO = 0
INPUT_ONE = 1
INPUT_TWO = 2
TOPUP_COST_ZERO = 0
NO_OF_DAYS_BEFORE_TO_NOTIFY = 10
DATE_FORMAT = "%d-%m-%Y"
ADD_TOPUP = "ADD_TOPUP"
ADD_SUBSCRIPTION = "ADD_SUBSCRIPTION"
START_SUBSCRIPTION = "START_SUBSCRIPTION"
RENEWAL_AMOUNT_MESSAGE = "RENEWAL_AMOUNT"
RENEWAL_REMINDER_MESSAGE = "RENEWAL_REMINDER"
PRINT_RENEWAL_DETAILS = "PRINT_RENEWAL_DETAILS"

INPUT_COMMANDS = {
    "START_SUBSCRIPTION": "process_start_subscription",
    "ADD_SUBSCRIPTION": "process_add_subscription",
    "ADD_TOPUP": "process_add_topup",
    "PRINT_RENEWAL_DETAILS": "process_print_renewal_details",
}

#per category price
MUSIC_FREE_PLAN_PRICE=0
MUSIC_FREE_PLAN_VALIDITY=1
MUSIC_PERSONAL_PLAN_PRICE=100
MUSIC_PERSONAL_PLAN_VALIDITY=1
MUSIC_PREMIUM_PLAN_PRICE=250
MUSIC_PREMIUM_PLAN_VALIDITY=3
VIDEO_FREE_PLAN_PRICE=0
VIDEO_FREE_PLAN_VALIDITY=1
VIDEO_PERSONAL_PLAN_PRICE=200
VIDEO_PERSONAL_PLAN_VALIDITY=1
VIDEO_PREMIUM_PLAN_PRICE=500
VIDEO_PREMIUM_PLAN_VALIDITY=3
PODCAST_FREE_PLAN_PRICE=0
PODCAST_FREE_PLAN_VALIDITY=1
PODCAST_PERSONAL_PLAN_PRICE=100
PODCAST_PERSONAL_PLAN_VALIDITY=1
PODCAST_PREMIUM_PLAN_PRICE=300
PODCAST_PREMIUM_PLAN_VALIDITY=3

TOPUP_PLAN_FOUR_DEVICE_PRICE_PER_MONTH=50
TOPUP_PLAN_TEN_DEVICE_PRICE_PER_MONTH=100

TOPUP_PLAN_FOUR_DEVICE_DURATION=1
TOPUP_PLAN_TEN_DEVICE_DURATION=1

TOPUP_PLAN_FOUR_DEVICE=4
TOPUP_PLAN_TEN_DEVICE=10