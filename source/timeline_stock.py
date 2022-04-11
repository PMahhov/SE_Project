from background_stock import Background_Stock
from information_popup import Information_Popup
from pygame_gui import UIManager

class Timeline_Stock:
    def __init__(
        self,
        id: int,
        volume: int,
        total_cost: float,
        stock_reference: Background_Stock,
    ) -> None:
        self.id = id
        self.volume = volume
        self.total_cost = total_cost
        self.stock_reference = stock_reference

    def change_volume(self, volume: int) -> None:
        self.volume = volume

    def display_info(self, manager: UIManager) -> None:
        info_popup = Information_Popup(self.stock_reference.get_name(), self.stock_reference.get_historical_prices(), manager)
        info_popup.display_graph()
        
    def get_price(self) -> int:
        return self.stock_reference.get_price()

    def buy(self, volume_increase: int) -> None:
        self.volume += volume_increase
        self.total_cost += self.get_price()*volume_increase
    
    def sell(self, volume_decrease: int) -> None:
        self.volume -= volume_decrease
        if self.volume == 0:
            self.total_cost = 0
        else:
            self.total_cost -= self.get_avg_buy_cost * volume_decrease

    def get_avg_buy_cost(self) -> float:
        if self.volume == 0:
            return 0
        else:
            return self.total_cost/self.volume

    


