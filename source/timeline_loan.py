from source.background_loan import Background_Loan

class Timeline_Loan:

    def __init__(self, id: int, volume: int, avg_price_bought: int, cash_flow: int, stock_reference: Background_Loan) -> None:
        self.id = id
        self.volume = volume
        self.avg_price_bought = avg_price_bought
        self.cash_flow = cashflow
        self.stock_reference = stock_reference

    def progress_time() -> None:
        pass

    def get_price() -> int:
        return self.price 