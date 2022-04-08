import numpy as np
import pytest
from background_stock import Background_Stock


@pytest.mark.parametrize(
    "bg_stock, price",
    [
        (Background_Stock(0, "AAPL", 5, 1, 1, np.array([1, 2, 3])), 5),
        (Background_Stock(0, "GOOG", 3, 1, 1, np.array([1, 2, 3])), 3),
    ],
)
def test_get_price(bg_stock, price):
    assert bg_stock.get_price() == price
