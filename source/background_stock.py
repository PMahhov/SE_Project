import pandas as pd

class BackgroundStock:

    def __init__(self, id: int, name: str, price: int, volatility: int, trend: int,  historical_prices: pd.DataFrame) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.volatility = volatility
        self.trend = trend
        self.historical_prices = historical_prices

    def progress_time() -> None:
        pass

    def get_price() -> int:
        return self.price