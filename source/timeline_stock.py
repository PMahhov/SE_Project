from matplotlib import container
from background_stock import Background_Stock
from information_popup import Information_Popup
import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UITextBox, UILabel

class Timeline_Stock:
    def __init__(
        self,
        # id: int,
        # volume: int,
        volume: int,
        stock_reference: Background_Stock,
        top: int,
        box_width: int,
        box_height: int,
        timeline_panel: UIPanel,
        manager: UIManager,
    ) -> None:
        self.box_width = box_width
        self.box_height = box_height
        self.left = 0
        self.top = top
        self.manager = manager

        self.id = id
        self.volume = volume
        self.total_cost = volume*stock_reference.get_price()
        self.stock_reference = stock_reference

        self.stock_panel = UIPanel(
            relative_rect=pygame.Rect(self.left, self.top, self.box_width + 6, self.box_height * 5),
            starting_layer_height=0,
            manager=self.manager,
            container=timeline_panel,
            visible=True,
        )

        self.namelabel = UILabel(
            relative_rect = pygame.Rect(0,0,self.box_width,self.box_height),
            text = self.stock_reference.get_name(),
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            )
        
        self.pricebox = UITextBox(
            html_text = "Price: "+str(self.stock_reference.get_price()),
            relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel
        )
        self.update_boxes()
    

    def update_boxes(self):
        try:
            self.volumebox.kill()
            self.buycostbox.kill()
            self.cashflowbox.kill()
        except:
            pass
        finally:
            self.volumebox = UITextBox(
                html_text = "Volume: "+str(self.volume),
                relative_rect = pygame.Rect(self.box_width/2,self.box_height,self.box_width/2,self.box_height),
                manager = self.manager,
                container = self.stock_panel,
                parent_element = self.stock_panel
            )
            self.buycostbox = UITextBox(
                html_text = "Average buy cost: "+str(self.get_avg_buy_cost()),
                relative_rect = pygame.Rect(0,self.box_height*2,self.box_width/2,self.box_height),
                manager = self.manager,
                container = self.stock_panel,
                parent_element = self.stock_panel
            )                
            self.cashflowbox = UITextBox(
                html_text = "Total cash flow: "+str(self.get_cash_flow()),
                relative_rect = pygame.Rect(self.box_width/2,self.box_height*2,self.box_width/2,self.box_height),
                manager = self.manager,
                container = self.stock_panel,
                parent_element = self.stock_panel
            )                

    def progress_time(self):
        self.update_boxes()
        try:
            self.pricebox.kill()
        except:
            pass
        finally:
            self.pricebox = UITextBox(
                html_text = "Price: "+str(self.stock_reference.get_price()),
                relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
                manager = self.manager,
                container = self.stock_panel,
                parent_element = self.stock_panel
            )

    def change_volume(self, volume: int) -> None:
        self.volume = volume

    def display_info(self, manager: UIManager) -> None:
        info_popup = Information_Popup(self.stock_reference.get_name(), self.stock_reference.get_historical_prices(), manager)
        info_popup.display_graph()
        
    def get_total_value(self) -> int:
        return self.stock_reference.get_price() * self.volume

    def get_price(self) -> int:
        return self.stock_reference.get_price()

    def get_volume(self) -> int:
        return self.volume

    def buy(self, volume_increase: int) -> None:
        self.volume += volume_increase
        self.total_cost += self.get_price()*volume_increase
        self.update_boxes()
    
    def sell(self, volume_decrease: int) -> None:
        self.volume -= volume_decrease
        if self.volume == 0:
            self.total_cost = 0
        else:
            self.total_cost -= self.get_avg_buy_cost() * volume_decrease
        self.update_boxes()

    def get_avg_buy_cost(self) -> float:
        if self.volume == 0:
            return 0
        else:
            return self.total_cost/self.volume

    def get_cash_flow(self) -> int:
        return self.get_total_value() - self.total_cost


    


