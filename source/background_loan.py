import pandas as pd

class Background_Loan:

    def __init__(self, id: int, offered_interest_rate: int, historical_interest_rates:  pd.DataFrame, volatility: int, trend: int, max_amount_multiplier: int) -> None:
        self.id = id
        self.offered_interest_rate = offered_interest_rate
        self.historical_interest_rates = historical_interest_rates
        self.volatility = volatility
        self.trend = trend
        self.max_amount_multiplier = max_amount_multiplier

    def progress_time() -> None:
        pass