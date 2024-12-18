import sys
from src.models.subscription import Subscription
from src.services.subscription_service import SubscriptionService
from src.services.topup_service import TopupService
from src.services.renewal_service import RenewalService
from src.services.helper_functions import (
    is_valid_start_subscription,
    is_valid_add_topup,
    is_valid_category,
    is_valid_plan_type,
)
from src.constants.constant import (
    START_SUBSCRIPTION,
    ADD_SUBSCRIPTION,
    ADD_TOPUP,
    PRINT_RENEWAL_DETAILS,INPUT_ZERO
)
from src.constants.error_codes import ErrorCodes


class CommandProcessor:
    def __init__(self):
        self.subscription = None
        self.subscription_service = None
        self.topup_service = None
        self.renewal_service = None
        self.start_date = None
        self.stop_execution = False

    def handle_start_subscription(self, parts):
        self.start_date = is_valid_start_subscription(parts)
        if self.start_date:
            self.subscription = Subscription(self.start_date)
            self.subscription_service = SubscriptionService(self.subscription)
            self.topup_service = TopupService(self.subscription)
            self.renewal_service = RenewalService(self.subscription)

    def handle_add_subscription(self, parts):
        if not self.start_date:
            print(ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.INVALID_DATE)
            self.stop_execution = True
            return

        category = is_valid_category(parts[1])
        plan_type = is_valid_plan_type(parts[2])
        if category and plan_type:
            result = self.subscription_service.add_subscription(category, plan_type)
            if result == (
                ErrorCodes.ADD_SUBSCRIPTION_FAILED + " " + ErrorCodes.DUPLICATE_CATEGORY
            ):
                print(
                    ErrorCodes.ADD_SUBSCRIPTION_FAILED
                    + " "
                    + ErrorCodes.DUPLICATE_CATEGORY
                )
                self.stop_execution = True
                return
            elif result:
                print(result)

    def handle_add_topup(self, parts):
        topup_name, months = is_valid_add_topup(parts, self.subscription)
        if topup_name and months:
            result = self.topup_service.add_topup(topup_name, months)
            if result == (
                ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.DUPLICATE_TOPUP
            ):
                print(ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.DUPLICATE_TOPUP)
                self.stop_execution = True
                return
            elif result:
                print(result)

    def handle_print_renewal_details(self):
        if not self.subscription or not self.subscription.has_active_subscriptions():
            print(ErrorCodes.SUBSCRIPTION_NOT_FOUND)
            self.stop_execution = True
            return
        else:
            self.renewal_service.print_renewal_details()

    def process_commands(self, lines):
        try:
            for line in lines:
                if self.stop_execution:
                    break
                parts = line.strip().split()
                if not parts:
                    continue

                command = parts[INPUT_ZERO]
                if command == START_SUBSCRIPTION:
                    self.handle_start_subscription(parts)

                elif command == ADD_SUBSCRIPTION:
                    self.handle_add_subscription(parts)

                elif command == ADD_TOPUP:
                    self.handle_add_topup(parts)

                elif command == PRINT_RENEWAL_DETAILS:
                    self.handle_print_renewal_details()

                else:
                    print(ErrorCodes.INVALID_INPUT)
                    return
        except Exception as e:
            print(f"Error occurred: {e}")
            sys.exit(1)
