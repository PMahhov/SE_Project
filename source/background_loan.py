from typing import List

import numpy as np


class Background_Loan:
    """
    A predominately data class that stores information about the loan available for the user to take.

    ...
    ATTRIBUTES
    ----------

    id : int
        unique loan identification (currently, only one possible loan available, id will be useful in future iterations if there are several loan options)
    offered_interest_rate : float [0.2, inf)
        the interest rate currently offered. When user takes loan, their interest rate will be fixed to the offered_interest_rate and time of taking.
        this will change after each time interval even if the user has taken a loan
    volatility: float [0.0, 100.0]
        the percentage standard deviation for the normal distribution from which the next offered_interest_rate will be taken
    trend: float [-inf, inf]
        offered_interest_rate + trend is the mean for the normal distribution from which the next offered_interest_rate will be taken
    change_in_trend : float (-inf, inf)
        the amount that trend changes after each timetep (parallel to mathematical derivative of trend)
    c_2_in_trend ; float (-inf, inf)
        the amount that change_in_trend changes after each timestep (parallel to mathematical derivative of change_in_trend OR second derivative of trend)
    initial_number_of_historical_interest_rates : int [0, inf)
        the number of simulated time intervals that occur before the simulation start
    historical_interest_rates : List[float]
        a list of past offered_interest_rate. Is appended to after each time interval
    max_amount_multiplier : float (0.0, inf)
        the timeline may borrow an amount proportional to its net worth, the max_amount_multiplier is the proportional coefficient

    METHODS
    -------
    progress_time:
        simulates a time interval skip, updating offered_interest_rate by selecting from a normal distribution defined by volatility and trend.
        stores second last offered_interest_rate to historical_interest_rates

    """

    def __init__(
        self,
        id: int,
        offered_interest_rate: float,
        volatility: float,
        trend: float,
        change_in_trend: float,
        c_2_in_trend: float,
        number_of_historical_interest_rates: int,
        max_amount_multiplier: float,
    ) -> None:

        self.id = id
        self.offered_interest_rate = max(0.2, offered_interest_rate)
        #self.offered_interest_rate = offered_interest_rate
        self.volatility = volatility
        self.trend = trend
        self.change_in_trend = change_in_trend
        self.c_2_in_trend = c_2_in_trend
        self.initial_number_of_historical_interest_rates = number_of_historical_interest_rates
        self.historical_interest_rates = []
        # procedurally generates a period of time intervals equal to number_of_historical_prices
        # initial loan characteristics are similar but a repeat of a level is unlikely to have the same starting loan interest rate and historical information
        for i in range(number_of_historical_interest_rates):
            self.progress_time()
        self.max_amount_multiplier = max_amount_multiplier

    def progress_time(self) -> None:

        # update the loan interest rate based on a normal distribution
        mean = self.offered_interest_rate + self.trend
        std = self.volatility * abs(mean) / 100
        self.offered_interest_rate = max(0.2, np.random.normal(mean, std))
        self.trend += self.change_in_trend 
        self.change_in_trend += self.c_2_in_trend

        # adds previous loan interest rate to the list of historical interest rates
        self.historical_interest_rates.append(self.offered_interest_rate)

    def get_id(self) -> int:
        return self.id

    def get_offered_interest_rate(self) -> float:
        return self.offered_interest_rate

    def get_max_amount_multiplier(self) -> float:
        return self.max_amount_multiplier

    def get_historical_interest_rates(self) -> List[float]:
        return self.historical_interest_rates

    def get_initial_number_of_historical_interest_rates(self) -> int:
        return self.initial_number_of_historical_interest_rates