from src.models.subscription import Subscription
from src.services.subscription_service import SubscriptionService
from src.services.topup_service import TopupService
from src.services.renewal_service import RenewalService
from src.constants.error_codes import ErrorCodes
import sys
from .helper_functions import (
    is_valid_plan_type,
    is_valid_date,
    is_valid_category,
    is_valid_topup_type,
)


def is_valid_start_subscription(parts):
    if len(parts) < 2 or not is_valid_date(parts[1]):
        print(ErrorCodes.INVALID_DATE)
        return None
    return parts[1]


def is_valid_add_topup(parts, subscription):
    if not subscription:
        print(ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.SUBSCRIPTION_NOT_FOUND)
        return None, None
    if len(parts) < 3 or not parts[2].isdigit():
        print(ErrorCodes.ADD_TOPUP_FAILED)
        return None, None
    topup_name_input, months = parts[1], int(parts[2])
    topup_name = is_valid_topup_type(topup_name_input)
    if not topup_name:
        print(ErrorCodes.ADD_TOPUP_FAILED)
        return None, None
    return topup_name, months


def process_commands(lines):
    try:
        subscription = None
        subscription_service = None
        topup_service = None
        renewal_service = None
        start_date = None  # Initialize start_date outside the loop

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue

            command = parts[0]

            # START_SUBSCRIPTION command
            if command == "START_SUBSCRIPTION":
                start_date = is_valid_start_subscription(parts)

                subscription = Subscription(start_date)
                subscription_service = SubscriptionService(subscription)
                topup_service = TopupService(subscription)
                renewal_service = RenewalService(subscription)

            # ADD_SUBSCRIPTION command
            elif command == "ADD_SUBSCRIPTION":
                if not subscription:
                    print(
                        ErrorCodes.ADD_SUBSCRIPTION_FAILED
                        + " "
                        + ErrorCodes.SUBSCRIPTION_NOT_FOUND
                    )
                    return  # Stop execution completely
                if not start_date:  # Check if start_date is invalid or not set
                    print(
                        ErrorCodes.ADD_SUBSCRIPTION_FAILED
                        + " "
                        + ErrorCodes.INVALID_DATE
                    )
                    continue
                category_input = parts[1]
                plan_type_input = parts[2]

                # Validate inputs
                category = is_valid_category(category_input)
                plan_type = is_valid_plan_type(plan_type_input)
                if not category or not plan_type:
                    print(
                        ErrorCodes.ADD_SUBSCRIPTION_FAILED + " INVALID_CATEGORY_OR_PLAN"
                    )
                    return  # Stop execution completely

                # Add subscription and handle duplicate categories
                result = subscription_service.add_subscription(category, plan_type)
                if result == (
                    ErrorCodes.ADD_SUBSCRIPTION_FAILED
                    + " "
                    + ErrorCodes.DUPLICATE_CATEGORY
                ):
                    print(
                        ErrorCodes.ADD_SUBSCRIPTION_FAILED
                        + " "
                        + ErrorCodes.DUPLICATE_CATEGORY
                    )
                    return  # Stop execution completely
                elif result:  # Other errors or success
                    print(result)

            # ADD_TOPUP command
            elif command == "ADD_TOPUP":
                if not subscription:
                    print(
                        ErrorCodes.ADD_TOPUP_FAILED
                        + " "
                        + ErrorCodes.SUBSCRIPTION_NOT_FOUND
                    )
                    return  # Stop execution completely
                print(parts, subscription)
                topup_name, months = is_valid_add_topup(parts, subscription)
                print(topup_name, months)
                if topup_name and months:
                    result = topup_service.add_topup(topup_name, months)
                    if result == (
                        ErrorCodes.ADD_TOPUP_FAILED + " " + ErrorCodes.DUPLICATE_TOPUP
                    ):
                        print(
                            ErrorCodes.ADD_TOPUP_FAILED
                            + " "
                            + ErrorCodes.DUPLICATE_TOPUP
                        )
                        return  # Stop execution completely
                    elif result:
                        print(result)

            # PRINT_RENEWAL_DETAILS command
            elif command == "PRINT_RENEWAL_DETAILS":
                if not subscription or not subscription.has_active_subscriptions():
                    print(ErrorCodes.SUBSCRIPTION_NOT_FOUND)
                    return  # Stop execution completely
                else:
                    renewal_service.print_renewal_details()

            # INVALID_INPUT for unrecognized commands
            else:
                print("INVALID_INPUT")
                return  # Stop execution completely

    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

