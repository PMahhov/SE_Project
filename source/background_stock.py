from typing import List

import numpy as np


class Background_Stock:
    def __init__(
        self,
        id: int,
        name: str,
        price: int,
        volatility: int,
        trend: float,
        change_in_trend: float,
        number_of_historical_prices: int,
    ) -> None:
        self.id = id
        self.name = name
        self.price = max(1, price)
        self.volatility = volatility
        self.trend = trend
        self.change_in_trend = change_in_trend
        self.initial_number_of_historical_prices = number_of_historical_prices
        self.historical_prices = []

        # procedurally generates a period of time intervals equal to number_of_historical_prices
        # initial stock characteristics are similar but a repeat of a level is unlikely to have the same starting stock price and historical information
        for i in range(number_of_historical_prices):
            self.progress_time()

    def progress_time(self) -> None:
        """
        Updates relevant loan attributes after a (previously-specified) time interval
        """

        # update the stock price based on a normal distribution
        mean = self.price + self.trend
        std = self.volatility * abs(mean) / 100
        self.price = max(1, int(np.random.normal(mean, std) + 0.5))
        self.trend += self.change_in_trend

        # add previous stock price to the list of historical prices
        self.historical_prices.append(self.price)

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> int:
        return self.price

    def get_historical_prices(self) -> List[int]:
        return self.historical_prices

    def get_initial_number_of_historical_prices(self) -> int:
        return self.initial_number_of_historical_prices
