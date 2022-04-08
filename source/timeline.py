import pygame
import yaml
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UITextBox

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_length = config["screen_length"]
screen_width = config["screen_width"]


class Timeline:
    def __init__(
        self,
        manager: UIManager,
        side: str,
        box_width: int,
        is_active: bool,
        # net_worth: int,
        # stocks: List[Timeline_Stock],
        # loan: Timeline_Loan,
        # active_loan_id: int,
        money: int = 0,
    ) -> None:
        self.is_active = is_active
        self.money = money
        self.manager = manager
        # self.net_worth = net_worth
        # self.stocks = stocks
        # self.loan = loan
        # self.active_loan_id = active_loan_id

        # UI setup
        self.top = 150
        self.box_width = box_width
        self.side = side
        if self.side == "left":
            self.left = (screen_length / 3) - 3 * box_width / 4
            self.start_hidden = True
        elif self.side == "center":
            self.left = (screen_length - self.box_width) / 2
            self.start_hidden = False
        elif self.side == "right":
            self.left = (2 * screen_length / 3) - box_width / 4
            self.start_hidden = True
        else:
            raise ValueError("Timeline has weird side")

        self.timeline_panel = UIPanel(
            relative_rect=pygame.Rect(self.left, self.top, self.box_width + 6, 510),
            starting_layer_height=0,
            manager=self.manager,
            visible=not self.start_hidden,
        )
        self.update_boxes()

    def update_boxes(self):
        try:
            self.moneybox.kill()
        except:
            pass
        finally:
            self.moneybox = UITextBox(
                html_text="Money: " + str(self.money),
                relative_rect=pygame.Rect(0, 50, self.box_width, 50),
                container=self.timeline_panel,
                manager=self.manager,
            )

    def switch_activity(self) -> None:
        if self.is_active == False:
            self.timeline_panel.show()
            self.is_active = True
        elif self.is_active == True:
            self.timeline_panel.hide()
            self.is_active = False
        else:
            raise ValueError("timeline is neither active or inactive")

    def buy_stock(self, Timeline_Stock, volume: int) -> None:
        pass

    def sell_stock(self, Timeline_Stock, volume: int) -> None:
        pass

    def take_loan(self, Timeline_Stock, amount: int) -> None:
        pass

    def pay_loan(self, amount: int) -> None:
        pass

    def progress_time(self) -> None:
        pass




def copy_data(self, kept_timeline: Timeline) -> None:
    pass


Timeline.copy_data = copy_data
