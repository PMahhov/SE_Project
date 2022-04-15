from multiprocessing.sharedctypes import Value
from matplotlib import container
from background_stock import Background_Stock
from information_popup import Information_Popup
import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UITextBox, UILabel, UIButton

class Timeline_Stock:
    def __init__(
        self,
        volume: int,
        stock_reference: Background_Stock,
        timeline_reference,
        top: int,
        box_width: int,
        box_height: int,
        timeline_panel: UIPanel,
        manager: UIManager,
        timestep: str
    ) -> None:
        self.box_width = box_width
        self.box_height = box_height
        self.left = 0
        self.top = top
        self.manager = manager
        self.timestep = timestep

        self.id = stock_reference.get_id()
        self.volume = volume
        self.total_cost = volume*stock_reference.get_price()
        self.cash_flow = 0

        self.stock_reference = stock_reference
        self.timeline_reference = timeline_reference

        self.stock_panel = UIPanel(
            relative_rect=pygame.Rect(self.left, self.top, self.box_width + 6, self.box_height * 4 + 10),
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

        self.buylabel = UILabel(
            relative_rect = pygame.Rect(0,self.box_height*3,self.box_width/8,self.box_height),
            text = "Buy: ",
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            ) 
        
        self.selllabel = UILabel(
            relative_rect = pygame.Rect(self.box_width/2 - 10,self.box_height*3,self.box_width/8,self.box_height),
            text = "Sell: ",
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            ) 

        self.buyone_button = UIButton(
            relative_rect = pygame.Rect(self.box_width / 8 - 15, self.box_height*3, self.box_width/8, self.box_height),
            text = "x1",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Buy one of this stock"
        )

        self.buyten_button = UIButton(
            relative_rect = pygame.Rect(2*self.box_width / 8 - 15, self.box_height*3, self.box_width/8, self.box_height),
            text = "x10",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Buy 10 of this stock"
        )

        self.buymax_button = UIButton(
            relative_rect = pygame.Rect(3*self.box_width / 8 - 15, self.box_height*3, self.box_width/8, self.box_height),
            text = "Max",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Buy as much as you can afford"
        )        

        self.sellone_button = UIButton(
            relative_rect = pygame.Rect(5*self.box_width / 8 - 22, self.box_height*3, self.box_width/8, self.box_height),
            text = "x1",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Sell one of this stock"
        )

        self.sellten_button = UIButton(
            relative_rect = pygame.Rect(6*self.box_width / 8 - 22, self.box_height*3, self.box_width/8, self.box_height),
            text = "x10",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Sell 10 of this stock"
        )

        self.sellmax_button = UIButton(
            relative_rect = pygame.Rect(7*self.box_width / 8 - 22, self.box_height*3, self.box_width/8, self.box_height),
            text = "Max",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Sell all of this stock"
        )         

        self.pricebox = UITextBox(
            html_text = "Price: "+str(self.stock_reference.get_price()),
            relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel
        )

        self.information_button = UIButton(
            relative_rect = pygame.Rect(self.box_height*0.1,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "i",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Display historical information about the stock"
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
                html_text = "Avg buy cost: " + f"{self.get_avg_buy_cost():.2f}",
                relative_rect = pygame.Rect(0,self.box_height*2,self.box_width/2,self.box_height),
                manager = self.manager,
                container = self.stock_panel,
                parent_element = self.stock_panel
            )                      
            self.cashflowbox = UITextBox(
            html_text = "Cash flow: " + f"{self.cash_flow:.2f}",
            relative_rect = pygame.Rect(self.box_width/2,self.box_height*2,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel
        )           
        
        # enable/disable buy/sell buttons depending on how much money you have
        buyable = self.buyable()
        if buyable >= 1:
            self.buyone_button.enable()
            self.buymax_button.enable()
        else:
            self.buyone_button.disable()
            self.buymax_button.disable()
        if buyable >=10:
            self.buyten_button.enable()
        else:
            self.buyten_button.disable()

        if self.volume >= 1:
            self.sellone_button.enable()
            self.sellmax_button.enable()
        else:
            self.sellone_button.disable()
            self.sellmax_button.disable()
        if self.volume >=10:
            self.sellten_button.enable()
        else:
            self.sellten_button.disable()        

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

    def buyable(self) -> int:
        money = self.timeline_reference.money
        return money//self.get_price()

    def change_volume(self, volume: int) -> None:
        self.volume = volume

    def display_info(self) -> None:
        try:
            self.info_popup.kill()
        except:
            pass
        finally:
            self.info_popup = Information_Popup(self.stock_reference.get_name(), self.stock_reference.get_historical_prices(), self.stock_reference.get_initial_number_of_historical_prices(), self.timestep, "stock price", self.manager)
            self.info_popup.display_graph()
        
    def get_total_value(self) -> int:
        return self.stock_reference.get_price() * self.volume

    def get_price(self) -> int:
        return self.stock_reference.get_price()

    def get_volume(self) -> int:
        return self.volume

    def buy(self, volume_increase: int) -> None:
        if self.buyable() >= volume_increase:
            self.volume += volume_increase
            change = self.get_price()*volume_increase
            self.total_cost += change
            self.timeline_reference.money -= change
            self.cash_flow -= change
        
    def sell(self, volume_decrease: int) -> None:
        if self.volume >= volume_decrease:       
            self.total_cost = ((self.volume - volume_decrease)/self.volume) * self.total_cost
            self.volume -= volume_decrease
            change = self.get_price() * volume_decrease
            self.timeline_reference.money += change
            self.cash_flow += change

    def get_avg_buy_cost(self) -> float:
        if self.volume == 0:
            return 0
        else:
            return self.total_cost/self.volume

    def get_id(self) -> int:
        return self.id


    def button_pressed(self, event, timeline) -> bool:
        if event.ui_element == self.buyone_button:
            self.buy(1)
        elif event.ui_element == self.buyten_button:
            self.buy(10)
        elif event.ui_element == self.buymax_button:
            self.buy(self.buyable())
        elif event.ui_element == self.sellone_button:
            self.sell(1)
        elif event.ui_element == self.sellten_button:
            self.sell(10)
        elif event.ui_element == self.sellmax_button:
            self.sell(self.volume)
        elif event.ui_element == self.information_button:
            self.display_info()
        else:
            return False
        return True
    


