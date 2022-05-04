from datetime import time
from xmlrpc.client import Boolean
import pygame
import yaml
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UITextBox, UIScrollingContainer, UILabel
from background_stock import Background_Stock
from timeline_stock import Timeline_Stock
from background_stock import Background_Stock
from background_loan import Background_Loan
from timeline_loan import Timeline_Loan
from typing import List

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_width = config["screen_width"]
screen_height = config["screen_height"]


class Timeline:
    def __init__(
        self,
        manager: UIManager,
        side: str,
        box_width: int,
        box_height: int,
        top:int,
        reference_stocks: List[Background_Stock],
        reference_loan: Background_Loan,
        timestep: str,
        is_active: bool,
        money: int,
    ) -> None:
        self.is_active = is_active
        self.money = money
        self.manager = manager
        self.timestep = timestep

        # UI setup
        self.top = top
        self.box_width = box_width
        self.box_height = box_height
        self.side = side
        if self.side == "left":
            self.left = (screen_width / 3) - 3 * box_width / 4
            self.is_active = False
        elif self.side == "center":
            self.left = (screen_width - self.box_width) / 2
            self.is_active = True
        elif self.side == "right":
            self.left = (2 * screen_width / 3) - box_width / 4
            self.is_active = False
        else:
            raise ValueError("Timeline has weird side")

        self.timeline_panel_bg = UIPanel(
            relative_rect=pygame.Rect(self.left, self.top, self.box_width + 6, screen_height-300+7),
            starting_layer_height=0,
            manager=self.manager,
            visible=self.is_active,
        )
        self.timeline_panel = UIScrollingContainer(
            relative_rect=pygame.Rect(0,0,self.box_width, screen_height-300+7),
            starting_height = 1,
            container = self.timeline_panel_bg,
            manager=self.manager,
            visible= self.is_active,
        )
        self.timeline_label = UILabel(
            relative_rect = pygame.Rect(0,0,self.box_width,self.box_height),
            text = "TIMELINE",
            manager = manager,
            container = self.timeline_panel,
        )
        
        self.stocks = []

        stock_top = 2*self.box_height
        stock_panel_size = self.box_height * 4 + 10     # if you change these two, change the corresponding height in the panel creation itself
        loan_panel_size = self.box_height * 3 + 10

        if reference_loan != None:
            stock_top += loan_panel_size

        for background_stock in reference_stocks:
            self.stocks.append(Timeline_Stock(0, background_stock,self,stock_top,self.box_width,self.box_height,self.timeline_panel,self.manager, self.timestep))
            stock_top += stock_panel_size

        self.calculate_net_worth(False)

        if reference_loan != None:
            self.timeline_panel.set_scrollable_area_dimensions((self.box_width-20,(stock_panel_size) * len(reference_stocks) + loan_panel_size + self.box_height*2 + 5))
            self.loan = Timeline_Loan(reference_loan, self, 2*self.box_height, self.box_width,self.box_height,self.timeline_panel,self.manager,self.timestep)
            
        else:
            self.timeline_panel.set_scrollable_area_dimensions((self.box_width-20,(stock_panel_size) * len(reference_stocks) + self.box_height*2 + 5))
            self.loan = None

        for timeline_stock in self.stocks:
            timeline_stock.update_boxes()

        if reference_loan != None:
            self.loan.update_boxes()

        # print("timeline additional check")
        # if not self.is_active:
        #     self.timeline_panel_bg.hide()
        #     self.timeline_panel.hide()
        #     self.loan.loan_panel_offered.hide()
        #     self.loan.loan_panel_taken.hide()
        # else:
        #     self.timeline_panel_bg.show()
        #     self.timeline_panel.show()
        

        self.update_boxes()


    def update_boxes(self):
        if self.timeline_panel.vert_scroll_bar != None:
            for object in [self.timeline_label,self.timeline_panel,self.timeline_panel_bg]:
                self.timeline_panel.vert_scroll_bar.join_focus_sets(object)

        try:
            self.moneybox.kill()
            self.net_worth_box.kill()
        except:
            pass
        finally:
            self.moneybox = UITextBox(
                html_text="Money: " + str(self.money),
                relative_rect=pygame.Rect(0, self.box_height, self.box_width/2, 50),
                container=self.timeline_panel,
                manager=self.manager,
            )
            self.net_worth_box = UITextBox(
                html_text="Net Worth: " + str(self.net_worth),
                relative_rect=pygame.Rect(self.box_width/2, self.box_height, self.box_width/2, 50),
                container=self.timeline_panel,
                manager=self.manager,
            )
            for object in [self.moneybox,self.net_worth_box]:
                self.timeline_panel.vert_scroll_bar.join_focus_sets(object)

    def switch_activity(self) -> None:
        if self.is_active == False:
            self.timeline_panel_bg.show()
            self.is_active = True
        elif self.is_active == True:
            self.timeline_panel_bg.hide()
            self.is_active = False
        else:
            raise ValueError("timeline is neither active or inactive")

    # def buy_max_stock(self, timeline_stock: Timeline_Stock) -> None:
    #     volume = self.money//timeline_stock.get_price()
    #     self.buy_stock(timeline_stock, volume)

    # def buy_stock(self, timeline_stock: Timeline_Stock, volume: int) -> None:
    #     cost = timeline_stock.get_price() * volume
    #     if cost > self.money:# add fee
    #         pass # cannot buy
    #     else: 
    #         timeline_stock.buy(volume)
    #         self.money -= cost

    # def sell_stock(self, timeline_stock: Timeline_Stock, volume: int) -> None:
    #     if volume > timeline_stock.get_volume():# add fee
    #         pass # cannot sell
    #     else: 
    #         timeline_stock.sell(volume)
    #         self.money += volume * timeline_stock.get_price()

    def take_loan(self, amount: int) -> None:
        if self.loan == None:
            raise TypeError("trying to take a nonexistent loan")
    #    elif (self.net_worth *  self.loan.get_loan_reference().get_max_amount_multiplier()) < amount or self.loan.have_loan():         3this is commented out due to level 3
     #       raise ValueError("cannot take loan")
        else:
            self.loan.take_loan(amount)
            self.money += amount

    def pay_max_loan(self) -> None:
        if self.money <= 0 or self.loan.get_amount_owed() <= 0:
            pass # cannot pay off any amount
        else:
            amount = min(self.cash, self.loan.get_amount_owed())
            self.pay_loan(amount)
            self.money -= amount

    def pay_loan(self, amount: int) -> None:
        if self.loan == None:
            raise TypeError("trying to pay a nonexistent loan")
        elif self.loan.get_amount_owed() < amount or self.money < amount or not self.loan.have_loan():
            raise ValueError("cannot pay off loan")
        else:
            self.loan.pay_off(amount)
            self.money -= amount

    def calculate_net_worth(self, loan_exists: bool) -> None:
        self.net_worth = self.money
        for stock in self.stocks:
            self.net_worth += stock.get_total_value()

        if loan_exists:
            self.net_worth -= self.loan.get_amount_owed()

    def progress_time(self) -> None:
        if self.loan != None:
            self.loan.progress_amount_owed()

        self.calculate_net_worth(self.loan != None)         # loan exists if it is not none

        # call progress time for timeline stocks
        for stock in self.stocks:
            stock.progress_time()

        # call progress time for timeline loans: 
        if self.loan != None:
            self.loan.progress_time()

        self.update_boxes()       
             

    def display_historical_information(self, financial_instrument: str, id: int) -> None:
        if financial_instrument == "loan":
            self.loan.display_info(self.manager)
        else:
            for stock in self.stocks:
                if stock.get_id() == id:
                    stock.display_info(self.manager)
                    break


    def button_pressed(self, event) -> bool:
        for stock in self.stocks:
            if stock.button_pressed(event, self):
                for stock in self.stocks:
                    stock.update_boxes()
                self.update_boxes()
                return True
        if self.loan != None:
            if self.loan.button_pressed(event):
                self.loan.update_boxes()
                self.update_boxes()
                return True
        else:
            return False
    
    def get_money(self) -> int:
        return self.money
    
    def get_net_worth(self) -> int:
        return self.net_worth

    def get_stocks(self) -> List[Timeline_Stock]:
        return self.stocks

    def get_loan(self) -> Timeline_Loan:
        return self.loan

    # when the user clicks on the "split timeline" or "merge timeline" button, update the timeline's attributes
    def update_attributes(self, money: int, net_worth: int, new_stocks: List[Timeline_Stock], new_loan: Timeline_Loan, new_panel: UIScrollingContainer) -> None:
        self.money = money
        self.net_worth = net_worth
        
        i = 0
        for stock in self.stocks:
            stock.update_attributes(new_stocks[i])
            i +=1
    
        if new_loan == None:
            self.loan = None
        else:
            self.loan.update_attributes(new_loan)

        if new_panel.vert_scroll_bar != None:
            self.timeline_panel.vert_scroll_bar.scroll_position = new_panel.vert_scroll_bar.scroll_position
            self.timeline_panel.vert_scroll_bar.scroll_wheel_moved = True
            self.timeline_panel.vert_scroll_bar.update(0.0)

        self.update_boxes()

    def get_is_active(self) -> bool:
        return self.is_active