from multiprocessing.sharedctypes import Value
from matplotlib import container
from background_stock import Background_Stock
from information_popup import Information_Popup
import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UITextBox, UILabel, UIButton
from pygame_gui.windows import UIMessageWindow
import yaml

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_height = config["screen_height"]
screen_width = config["screen_width"]
info_stock = config["info_stock"]

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

        self.UIobjects = []

        self.stock_panel = UIPanel(
            relative_rect=pygame.Rect(self.left, self.top, self.box_width + 6, self.box_height * 4 + 10),
            starting_layer_height=0,
            manager=self.manager,
            container=timeline_panel,
            visible=True,
        )
        self.UIobjects.append(self.stock_panel)

        self.namelabel = UILabel(
            relative_rect = pygame.Rect(0,0,self.box_width,self.box_height),
            text = self.stock_reference.get_name(),
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            )
        self.UIobjects.append(self.namelabel)

        self.buylabel = UILabel(
            relative_rect = pygame.Rect(0,self.box_height*3,self.box_width/8,self.box_height),
            text = "Buy: ",
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            ) 
        self.UIobjects.append(self.buylabel)    
        
        self.selllabel = UILabel(
            relative_rect = pygame.Rect(self.box_width/2 - 10,self.box_height*3,self.box_width/8,self.box_height),
            text = "Sell: ",
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            ) 
        self.UIobjects.append(self.selllabel)

        self.buyone_button = UIButton(
            relative_rect = pygame.Rect(self.box_width / 8 - 15, self.box_height*3, self.box_width/8, self.box_height),
            text = "x1",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Buy one of this stock"
        )
        self.UIobjects.append(self.buyone_button)

        self.buyten_button = UIButton(
            relative_rect = pygame.Rect(2*self.box_width / 8 - 15, self.box_height*3, self.box_width/8, self.box_height),
            text = "x10",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Buy 10 of this stock"
        )
        self.UIobjects.append(self.buyten_button)

        self.buymax_button = UIButton(
            relative_rect = pygame.Rect(3*self.box_width / 8 - 15, self.box_height*3, self.box_width/8, self.box_height),
            text = "Max",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Buy as much as you can afford"
        ) 
        self.UIobjects.append(self.buymax_button)       

        self.sellone_button = UIButton(
            relative_rect = pygame.Rect(5*self.box_width / 8 - 22, self.box_height*3, self.box_width/8, self.box_height),
            text = "x1",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Sell one of this stock"
        )
        self.UIobjects.append(self.sellone_button)

        self.sellten_button = UIButton(
            relative_rect = pygame.Rect(6*self.box_width / 8 - 22, self.box_height*3, self.box_width/8, self.box_height),
            text = "x10",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Sell 10 of this stock"
        )
        self.UIobjects.append(self.sellten_button)

        self.sellmax_button = UIButton(
            relative_rect = pygame.Rect(7*self.box_width / 8 - 22, self.box_height*3, self.box_width/8, self.box_height),
            text = "Max",
            manager = manager,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Sell all of this stock"
        )     
        self.UIobjects.append(self.sellmax_button)    

        self.pricebox = UITextBox(
            html_text = "Price: "+str(self.stock_reference.get_price()),
            relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel
        )
        self.UIobjects.append(self.pricebox)

        self.graph_button = UIButton(
            relative_rect = pygame.Rect((self.box_height*0.9)+5,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "h",
            manager = manager,
            starting_height = 2,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Display a graph with historical information about the stock"
        )
        self.UIobjects.append(self.graph_button)

        self.information_button = UIButton(
            relative_rect = pygame.Rect(self.box_height*0.1,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "i",
            manager = manager,
            starting_height = 2,
            container = self.stock_panel,
            parent_element = self.stock_panel,
            tool_tip_text = "Display information about stocks"
        )
        self.UIobjects.append(self.information_button)

        self.update_boxes()
    

    def update_boxes(self):
        if self.timeline_reference.timeline_panel.vert_scroll_bar != None:
            for object in self.UIobjects:
                self.timeline_reference.timeline_panel.vert_scroll_bar.join_focus_sets(object)
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
            # net cash flow as measured from start of scenario to current point
            self.cashflowbox = UITextBox(
            html_text = "Net cash flow: " + f"{self.cash_flow:.2f}",
            relative_rect = pygame.Rect(self.box_width/2,self.box_height*2,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.stock_panel,
            parent_element = self.stock_panel
            )

            if self.timeline_reference.timeline_panel.vert_scroll_bar != None:
                for object in [self.volumebox,self.buycostbox,self.cashflowbox]:
                    self.timeline_reference.timeline_panel.vert_scroll_bar.join_focus_sets(object)           
        
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

    def display_graph(self) -> None:
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

    def get_cash_flow(self) -> float:
        return self.cash_flow

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
        elif event.ui_element == self.graph_button:
            self.display_graph()
        elif event.ui_element == self.information_button:
            self.display_info()
        else:
            return False
        return True
    
    def update_attributes(self, new_stock: any) -> None:
        self.volume = new_stock.get_volume()
        self.cash_flow = new_stock.get_cash_flow()

        # update total_cost with update avg_buy_cost when self.update_boxes() is called
        self.total_cost = self.volume * new_stock.get_avg_buy_cost()
        self.update_boxes()
    
    # when i button clicked, display general information about stocks
    def display_info(self) -> None:
        try: 
            self.info_window.kill()
        except:
            pass
        finally:
            self.info_window = UIMessageWindow(
                pygame.Rect(
                    ((screen_width - (2.5 * screen_width/6)) / 2) ,
                    (2 * screen_height / 12),
                    (2.5 * screen_width) / 6,
                    screen_height/2,
                ),
                manager=self.manager,
                window_title= "Stocks",
                html_message=info_stock
            )
