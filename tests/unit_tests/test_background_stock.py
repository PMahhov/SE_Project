import pytest
from background_stock import Background_Stock


@pytest.mark.parametrize(
    "bg_stock, historical_length",
    [
        (Background_Stock(0, "AAPL", 5, 1, 1, 2, 10), 10),
        (Background_Stock(0, "GOOG", 3, 50, -100, .5, 3), 3),
        (Background_Stock(0, "TSLA", -7, 1, 1, 7, 1), 1),
    ],
)
def test_init(bg_stock: Background_Stock, historical_length: int):
    assert len(bg_stock.get_historical_prices()) == historical_length
    assert bg_stock.get_price() >= 1
    assert min(bg_stock.get_historical_prices()) >= 1
