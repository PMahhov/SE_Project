import numpy as np


class Background_Stock:
    def __init__(
        self,
        id: int,
        name: str,
        price: int,
        volatility: int,
        trend: int,
        number_of_historical_prices: int,
    ) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.volatility = volatility
        self.trend = trend
        self.number_of_historical_prices = number_of_historical_prices
        self.historical_prices = []

    # update all atributes of the class when the user push the button "progress time"
    def progress_time(self) -> None:
        # add previous stock price to the list of historical prices
        self.historical_prices.append(self.price)
        
        # update the stock price based on a normal distribution 
        mean = self.price + self.trend
        std = self.volatility
        self.price = int(np.random.normal(mean, std, 1) + 0.5)

    def get_price(self) -> int:
        return self.price

    def get_id(self) -> int:
        return self.id
