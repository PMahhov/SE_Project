from typing import List

import numpy as np


class Background_Stock:
    """
    A predominately data class that stores information about one stock available for the user to take.

    ...
    ATTRIBUTES
    ----------

        id: int,
        name: str,
        price: int,
        volatility: int,
        trend: float,
        change_in_trend: float,
        number_of_historical_prices: int,
    id : int
        unique stock identification number
    name : float
        stock name, should also be unique and will be displayed to user on historical graph
    price : int [1, inf)
        the current price of a stock. After each time skip, a new price is selected from a psuedo-normal distribution defined by volatility and trend
    volatility: float [0.0, 100.0]
        the percentage standard deviation for the normal distribution from which the next price will be taken
    trend: float (-inf, inf)
        price + trend is the mean for the normal distribution from which the next price will be taken
    change_in_trend: float
        the amount that trend changes after each timestep (parallel to mathematical derivative of trend)
    number_of_historical_prices : int [0, inf)
        the number of simulated time intervals that occur before the simulation start
    historical_prices : List[int]
        a list of past prices. Is appended to after each time interval

    METHODS
    -------
    progress_time:
        simulates a time interval skip, updating price by selecting from a normal distribution defined by volatility and trend.
        stores new price to historical_prices

    """
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
