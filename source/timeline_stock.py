from background_stock import Background_Stock
from information_popup import Information_Popup


class Timeline_Stock:
    def __init__(
        self,
        id: int,
        volume: int,
        avg_price_bought: int,
        cash_flow: int,
        stock_reference: Background_Stock,
    ) -> None:
        self.id = id
        self.volume = volume
        self.avg_price_bought = avg_price_bought
        self.cash_flow = cash_flow
        self.stock_reference = stock_reference

    def change_volume(self, volume: int) -> None:
        self.volume = volume

    def display_info(self) -> Information_Popup:
        pass

    def get_price(self) -> int:
        pass
