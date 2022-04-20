import numpy as np
from typing import List

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
        self.price = max(1, price)
        self.volatility = volatility
        self.trend = trend
        self.initial_number_of_historical_prices = number_of_historical_prices
        self.historical_prices = []
        for i in range(number_of_historical_prices):
            self.progress_time()

    # update all atributes of the class when the user push the button "progress time"
    def progress_time(self) -> None:
        # add previous stock price to the list of historical prices
        self.historical_prices.append(self.price)
        
        # update the stock price based on a normal distribution 
        mean = self.price + self.trend
        std = self.volatility*mean/100
        self.price = max(1, int(np.random.normal(mean, std, 1) + 0.5))

    def get_price(self) -> int:
        return self.price

    def get_name(self) -> str:
        return self.name

    def get_historical_prices(self) -> List[int]:
        return self.historical_prices

    def get_id(self) -> int:
        return self.id
    
    def get_initial_number_of_historical_prices(self) -> int:
        return self.initial_number_of_historical_prices
        
