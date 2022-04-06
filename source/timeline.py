from source.timeline_loan import Timeline_Loan
from source.timeline_stock import Timeline_Stock


class Timeline:
    def __init__(
        self,
        is_active: bool,
        money: int,
        net_worth: int,
        stocks: List[Timeline_Stock],
        loan: Timeline_Loan,
        active_loan_id: int,
    ) -> None:
        self.is_active = is_active
        self.money = money
        self.net_worth = net_worth
        self.stocks = stocks
        self.loan = loan
        self.active_loan_id = active_loan_id

    def buy_stock(Timeline_Stock, volume: int) -> None:
        pass

    def sell_stock(Timeline_Stock, volume: int) -> None:
        pass

    def take_loan(Timeline_Stock, amount: int) -> None:
        pass

    def pay_loan(amount: int) -> None:
        pass

    def progress_time() -> None:
        pass

    def switch_activity() -> None:
        pass

    def copy_data(kept_timeline: Timeline) -> None:
        pass
