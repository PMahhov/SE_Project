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

    # update all atributes of the class when the user push the button "progress time"
    def progress_time(self) -> None:
        # add previous stock price to the list of historical prices
        np.append(self.historical_prices, self.price)
        
        # update the stock price based on a normal distribution 
        mean = self.price + self.trend
        std = self.volatility
        self.price = int(np.random.normal(mean, std, 1) + 0.5)

    def get_price(self) -> int:
        return self.price

    def get_name(self) -> str:
        return self.name

    def get_historical_prices(self) -> np.array:
        return self.historical_prices
