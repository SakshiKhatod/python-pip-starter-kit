from datetime import datetime
from src.constants.constant import NO_OF_DAYS_BEFORE_TO_NOTIFY
from src.models.subscription import Subscription
from dateutil.relativedelta import relativedelta


class RenewalService:

    def __init__(self, subscription: Subscription):
        self.subscription = subscription

    def calculate_renewal_dates(self) -> dict:
        renewal_dates = {}
        if isinstance(self.subscription.start_date, str):
            start_date = datetime.strptime(self.subscription.start_date, "%d-%m-%Y")
        else:
            start_date = self.subscription.start_date
        for category, plan in self.subscription.plans.items():

            renewal_date = start_date + relativedelta(months=plan.duration)
            reminder_date = renewal_date - relativedelta(
                days=NO_OF_DAYS_BEFORE_TO_NOTIFY
            )

            renewal_dates[category] = reminder_date.strftime("%d-%m-%Y")
            # print(f"Renewal Date: {renewal_date}, Reminder Date: {reminder_date}")

        return renewal_dates

    def calculate_total_cost(self) -> int:
        total_cost = sum(plan.cost for plan in self.subscription.plans.values())
        if self.subscription.topup:
            total_cost += self.subscription.topup.cost
        return total_cost

    def get_renewal_details(self) -> list:
        renewal_dates = self.calculate_renewal_dates()
        total_cost = self.calculate_total_cost()
        renewal_details = []
        for category, date in renewal_dates.items():
            renewal_details.append(f"RENEWAL_REMINDER {category.name} {date}")
        renewal_details.append(f"RENEWAL_AMOUNT {total_cost}")
        return renewal_details

    def print_renewal_details(self):
        details = self.get_renewal_details()
        for detail in details:
            print(detail)
