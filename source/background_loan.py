import numpy as np
from typing import List

class Background_Loan:
    def __init__(
        self,
        id: int,
        offered_interest_rate: float,
        volatility: int,
        trend: int,
        number_of_historical_interest_rates: int,
        max_amount_multiplier: float,
    ) -> None:
        self.id = id
        self.offered_interest_rate = offered_interest_rate
        self.volatility = volatility
        self.trend = trend
        self.historical_interest_rates = []
        for i in range(number_of_historical_interest_rates):
            self.progress_time()
        self.max_amount_multiplier = max_amount_multiplier

    # update all atributes of the class when the user push the button "progress time"
    def progress_time(self) -> None:
        # add previous loan interest rate to the list of historical interest rates
        self.historical_interest_rates.append( self.offered_interest_rate)
        
        # update the loan interest rate based on a normal distribution 
        mean = self.offered_interest_rate + self.trend
        std = self.volatility*mean/100
        self.offered_interest_rate = np.random.normal(mean, std, 1)

    def get_historical_interest_rates(self) -> List[float]:
        return self.historical_interest_rates

    def get_max_amount_multiplier(self) -> float:
        return self.max_amount_multiplier
    
    def get_offered_interest_rate(self) -> float:
        return self.offered_interest_rate
    
    def get_id(self) -> int:
        return self.id
