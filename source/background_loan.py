import numpy as np


class Background_Loan:
    def __init__(
        self,
        id: int,
        offered_interest_rate: float,
        volatility: int,
        trend: int,
        historical_interest_rates: np.array,
        max_amount_multiplier: float,
    ) -> None:
        self.id = id
        self.offered_interest_rate = offered_interest_rate
        self.volatility = volatility
        self.trend = trend
        self.historical_interest_rates = historical_interest_rates
        self.max_amount_multiplier = max_amount_multiplier

    # update all atributes of the class when the user push the button "progress time"
    def progress_time(self) -> None:
        # add previous loan interest rate to the list of historical interest rates
        np.append(self.historical_interest_rates, self.offered_interest_rate)
        
        # update the loan interest rate based on a normal distribution 
        mean = self.offered_interest_rate + self.trend
        std = self.volatility
        self.offered_interest_rate = np.random.normal(mean, std, 1)

    def get_historical_interest_rates(self) -> np.array:
        return self.historical_interest_rates

    def get_max_amount_multiplier(self) -> float:
        return self.max_amount_multiplier
    
    def get_offered_interest_rate(self) -> float:
        return self.offered_interest_rate
