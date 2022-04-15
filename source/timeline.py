from datetime import time
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
        # net_worth: int,
        reference_stocks: List[Background_Stock],
        reference_loan: Background_Loan,
        is_active: bool,
        money: int = 0,
    ) -> None:
        self.is_active = is_active
        self.money = money
        self.manager = manager

        # UI setup
        self.top = top
        self.box_width = box_width
        self.box_height = box_height
        self.side = side
        if self.side == "left":
            self.left = (screen_width / 3) - 3 * box_width / 4
            self.start_hidden = True
        elif self.side == "center":
            self.left = (screen_width - self.box_width) / 2
            self.start_hidden = False
        elif self.side == "right":
            self.left = (2 * screen_width / 3) - box_width / 4
            self.start_hidden = True
        else:
            raise ValueError("Timeline has weird side")

        self.timeline_panel_bg = UIPanel(
            relative_rect=pygame.Rect(self.left, self.top, self.box_width + 6, screen_height-300),
            starting_layer_height=0,
            manager=self.manager,
            visible=not self.start_hidden,
        )
        self.timeline_panel = UIScrollingContainer(
            relative_rect=pygame.Rect(0,0,self.box_width, screen_height-300),
            starting_height = 1,
            container = self.timeline_panel_bg,
            manager=self.manager,
            visible=not self.start_hidden,
        )
        self.timeline_label = UILabel(
            relative_rect = pygame.Rect(0,0,self.box_width,self.box_height),
            text = "TIMELINE",
            manager = manager,
            container = self.timeline_panel,
        )

        
        self.stocks = []
        stock_top = 100
        for background_stock in reference_stocks:
            self.stocks.append(Timeline_Stock(0, background_stock,stock_top,self.box_width,self.box_height,self.timeline_panel,self.manager))
            stock_top += self.box_height * 4 + 10

        self.timeline_panel.set_scrollable_area_dimensions((self.box_width-20,(self.box_height*4 + 10) * len(reference_stocks) + self.box_height*2 + 5))
 
        self.loan = Timeline_Loan(reference_loan)
        self.net_worth = self.calculate_net_worth()
        

        self.update_boxes()


    def update_boxes(self):
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


    def switch_activity(self) -> None:
        if self.is_active == False:
            self.timeline_panel_bg.show()
            self.is_active = True
        elif self.is_active == True:
            self.timeline_panel_bg.hide()
            self.is_active = False
        else:
            raise ValueError("timeline is neither active or inactive")

    def buy_max_stock(self, timeline_stock: Timeline_Stock) -> None:
        volume = self.money//timeline_stock.get_price()
        self.buy_stock(timeline_stock, volume)

    def buy_stock(self, timeline_stock: Timeline_Stock, volume: int) -> None:
        cost = timeline_stock.get_price() * volume
        if cost > self.money:# add fee
            pass # cannot buy
        else: 
            timeline_stock.buy(volume)
            self.money -= cost

    def sell_stock(self, timeline_stock: Timeline_Stock, volume: int) -> None:
        if volume > timeline_stock.get_volume():# add fee
            pass # cannot sell
        else: 
            timeline_stock.sell(volume)
            self.money += volume * timeline_stock.get_price()

    def take_loan(self, amount: int) -> None:
        if (self.net_worth *  self.loan.get_loan_reference().get_max_amount_multiplier()) < amount or self.loan.have_loan():
            pass # cannot take loan
        else:
            self.loan.take_loan(amount)

    def pay_max_loan(self) -> None:
        if self.money <= 0:
            pass # cannot pay off any amount
        else:
            self.pay_loan(min(self.cash, self.loan.get_amount_owed()))

    def pay_loan(self, amount: int) -> None:
        if self.loan.get_amount_owed() < amount or self.money < amount or not self.loan.have_loan():
            pass # cannot pay loan
        else:
            self.loan.pay_off(amount)

    def calculate_net_worth(self) -> int:
        net_worth = self.money
        net_worth -= self.loan.get_amount_owed()
        for stock in self.stocks:
            net_worth += net_worth + stock.get_total_value()
        # [net_worth = net_worth + stock.get_total_value() for stock in self.stocks]
        return net_worth

    def progress_time(self) -> None:
        self.loan.progress_amount_owed()
        self.net_worth = self.calculate_net_worth()
        for stock in self.stocks:
            stock.progress_time()
        # call progress time for timeline loans




def copy_data(self, kept_timeline: Timeline) -> None:
    pass


Timeline.copy_data = copy_data
