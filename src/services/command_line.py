from src.models.subscription import Subscription
from src.services.subscription_service import SubscriptionService
from src.services.topup_service import TopupService
from src.services.renewal_service import RenewalService
from src.constants.error_codes import ErrorCodes
import sys
from .helper_functions import (
    validate_plan_type,
    validate_date,
    validate_category,
    validate_topup_type,
)


def process_commands(lines):
    try:
        subscription = None
        subscription_service = None
        topup_service = None
        renewal_service = None

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            command = parts[0]
            if command == "START_SUBSCRIPTION":
                start_date = parts[1]
                if not validate_date(start_date):
                    print(ErrorCodes.INVALID_DATE)
                    continue
                subscription = Subscription(start_date)
                subscription_service = SubscriptionService(subscription)
                topup_service = TopupService(subscription)
                renewal_service = RenewalService(subscription)

            elif command == "ADD_SUBSCRIPTION":
                if not validate_date(start_date):
                    print(
                        ErrorCodes.ADD_SUBSCRIPTION_FAILED
                        + " "
                        + ErrorCodes.INVALID_DATE
                    )
                    break
                if not subscription:
                    print(
                        ErrorCodes.ADD_SUBSCRIPTION_FAILED
                        + " "
                        + ErrorCodes.SUBSCRIPTION_NOT_FOUND
                    )
                    break

                category_input = parts[1]
                plan_type_input = parts[2]

                # Validate inputs
                category = validate_category(category_input)
                plan_type = validate_plan_type(plan_type_input)
                if not category or not plan_type:
                    break

                result = subscription_service.add_subscription(category, plan_type)
                if result:
                    print(result)
                    break

            elif command == "ADD_TOPUP":
                if not subscription:
                    print(
                        ErrorCodes.ADD_TOPUP_FAILED
                        + " "
                        + ErrorCodes.SUBSCRIPTION_NOT_FOUND
                    )
                    continue

                topup_name_input = parts[1]
                months = int(parts[2])

                # Validate inputs
                topup_name = validate_topup_type(topup_name_input)
                if not topup_name:
                    break

                result = topup_service.add_topup(topup_name, months)
                if result:
                    print(result)
                    break

            elif command == "PRINT_RENEWAL_DETAILS":
                if not subscription:
                    print(ErrorCodes.SUBSCRIPTION_NOT_FOUND)
                    continue
                renewal_service.print_renewal_details()

            else:
                print("INVALID_INPUT")
                break

    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)
