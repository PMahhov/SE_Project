import numpy as np
import pytest
from background_loan import Background_Loan


@pytest.mark.parametrize(
    "bg_loan, historical_length",
    [
        # Background_Loan(id, offered_interest_rate, volatility, trend, number_of_historical_interest_rates, max_amount_multiplier)
        (Background_Loan(0, 10, 3, 0, 2, 2.2), 2),
        (Background_Loan(1, -5, 3, 5, 5, 2.2), 5),
        (Background_Loan(2, 10, 7, -80, 10, 2.2), 10),
    ],
)
def test_init(bg_loan: Background_Loan, historical_length: int):
    assert len(bg_loan.get_historical_interest_rates()) == historical_length
    assert bg_loan.get_offered_interest_rate() >= 1
    assert min(bg_loan.get_historical_interest_rates()) >= 1

