from background_loan import Background_Loan
from background_stock import Background_Stock
from timeline import Timeline


class Background:

    _instance = None

    # find a way to create a private constructor
    def __init__(
        self,
        timelines: list(Timeline),
        stocks: list(Background_Stock),
        loan: Background_Loan,
        transaction_cost: int,
        win_cond_type: str,
        win_conds: dict(str, str),
    ) -> None:
        self.timelines = timelines
        self.stocks = stocks
        self.loan = loan
        self.transation_cost = transaction_cost
        self.win_cond_type = win_cond_type
        self.win_conds = win_conds

    def get_instance() -> self.Background:
        # https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
        pass

    def load_data(scenario_info: str) -> None:
        pass

    def get_stock(id: int) -> Background_Stock:
        pass

    def get_loan(id: int) -> Background_Loan:
        return loan

    def split_timelines() -> None:
        pass

    def merge_timeline(Timeline) -> None:
        pass

    def progress_time() -> None:
        pass
