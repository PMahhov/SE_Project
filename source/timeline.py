from timeline_loan import Timeline_Loan
from timeline_stock import Timeline_Stock
from typing import List

class Timeline:
    def __init__(
        self,
        # is_active: bool
        # money: int,
        # net_worth: int,
        # stocks: List[Timeline_Stock],
        # loan: Timeline_Loan,
        # active_loan_id: int,
    ) -> None:
        # self.is_active = is_active
        # self.money = money
        # self.net_worth = net_worth
        # self.stocks = stocks
        # self.loan = loan
        # self.active_loan_id = active_loan_id
        pass

    def buy_stock(self, Timeline_Stock, volume: int) -> None:
        pass

    def sell_stock(self, Timeline_Stock, volume: int) -> None:
        pass

    def take_loan(self, Timeline_Stock, amount: int) -> None:
        pass

    def pay_loan(self, amount: int) -> None:
        pass

    def progress_time(self) -> None:
        pass

    def switch_activity(self) -> None:
        pass

def copy_data(self, kept_timeline: Timeline) -> None:
        pass

Timeline.copy_data = copy_data