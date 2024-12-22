import sys
from src.constants.constant import (
    INPUT_ZERO,
    INPUT_ONE,
    INPUT_TWO,
    START_SUBSCRIPTION,
    ADD_SUBSCRIPTION,
    ADD_TOPUP,
    PRINT_RENEWAL_DETAILS,
    ONE,
    RENEWAL_REMINDER_MESSAGE,
    RENEWAL_AMOUNT_MESSAGE,
)
from src.constants.error_codes import ErrorCodes
from src.services.subscription_service import SubscriptionService
from src.services.topup_service import TopupService


class ProcessCommands:

    def __init__(self):
        self._subscription_service = SubscriptionService()
        self._topup_service = TopupService()

    def process_start_subscription(self, start_date):
        result = self._subscription_service.start_subscription(start_date)
        if result:
            print(result)

    def process_add_subscription(self, category, plan_type):
        result = self._subscription_service.add_subscription(category, plan_type)
        if result:
            print(result)

    def process_add_topup(self, topup_type, months):
        if self._subscription_service.get_subscriptions():
            result = self._topup_service.add_topup(topup_type, months)
            if result:
                print(result)
        else:
            print(
                ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.SUBSCRIPTIONS_NOT_FOUND
            )

    def calculate_total_cost(self):
        total_subscription_cost = (
            self._subscription_service.calculate_subscription_cost()
        )
        total_topup_cost = self._topup_service.calculate_topup_cost()
        total_cost = total_subscription_cost + total_topup_cost
        return total_cost

    def process_print_renewal_details(self):
        if not self._subscription_service.get_subscriptions():
            print(ErrorCodes.SUBSCRIPTIONS_NOT_FOUND)
            return
        total_cost = self.calculate_total_cost()
        renewal_dates = self._subscription_service.calculate_renewal_dates()
        renewal_details = []
        for category, date in renewal_dates.items():
            renewal_details.append(f"{RENEWAL_REMINDER_MESSAGE} {category} {date}")
        renewal_details.append(f"{RENEWAL_AMOUNT_MESSAGE} {total_cost}")
        for detail in renewal_details:
            print(detail)

    def process_input_commands(self, lines):
        try:
            for line in lines:
                if (
                    self._subscription_service.stop_execution
                    or self._topup_service.stop_execution
                ):
                    break
                parts = line.strip().split()
                if not parts:
                    continue

                command = parts[INPUT_ZERO]
                if command == START_SUBSCRIPTION:
                    self.process_start_subscription(parts[INPUT_ONE])

                elif command == ADD_SUBSCRIPTION:
                    self.process_add_subscription(parts[INPUT_ONE], parts[INPUT_TWO])

                elif command == ADD_TOPUP:
                    self.process_add_topup(parts[INPUT_ONE], int(parts[INPUT_TWO]))

                elif command == PRINT_RENEWAL_DETAILS:
                    self.process_print_renewal_details()

                else:
                    print(ErrorCodes.INVALID_INPUT)
                    return
        except Exception as e:
            print(f"Error occurred: {e}")
            sys.exit(ONE)
