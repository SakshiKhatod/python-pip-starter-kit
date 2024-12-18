class Subscription:

    def __init__(self, start_date: str):
        self.start_date = start_date
        self.plans = {}
        self.topup = None

    def add_plan(self, category, plan):
        self.plans[category] = plan

    def add_topup(self, topup):
        self.topup = topup

    def has_active_subscriptions(self):
        return len(self.plans) > 0
