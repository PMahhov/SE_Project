import numpy as np


class Background_Stock:
    def __init__(
        self,
        id: int,
        name: str,
        price: int,
        volatility: int,
        trend: int,
        historical_prices: np.array,
    ) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.volatility = volatility
        self.trend = trend
        self.historical_prices = historical_prices

    def progress_time(self) -> None:
        pass

    def get_price(self) -> int:
        return self.price
