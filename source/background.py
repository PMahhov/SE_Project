from background_loan import Background_Loan
from background_stock import Background_Stock

from timeline import Timeline

import pygame
import pygame_gui
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import UIButton, UILabel, UIPanel, UITextBox


class Background:

    _instance = None

    # Called internally by Python when creating an object of a class
    def __new__(cls):
        if cls._instance is None: # check whether the instance of the variable is None
            print('Creating the object')
            cls._instance = super(Background, cls).__new__(cls) # create a new object with the super() method
        return cls._instance # return the instance variable that contains the object of the Background class

    # Initialize attributes of the class
    def init_class(self, manager: UIManager):
        self.creation_button = UIButton(text= "Split Timeline", tool_tip_text = 'Copy the current timeline into two',
                            relative_rect=pygame.Rect(300,500,200,50),
                            manager = manager)
        self.left_timeline = Timeline()
        self.center_timeline = Timeline()
        self.right_timeline = Timeline()

    # self.timelines = timelines
    # self.stocks = stocks
    # self.loan = loan
    # self.transation_cost = transaction_cost
    # self.win_cond_type = win_cond_type
    # self.win_conds = win_conds

    def load_data(self, scenario_info: str) -> None:
        pass

    def get_stock(self, id: int) -> Background_Stock:
        pass

    def get_loan(self, id: int) -> Background_Loan:
        return self.loan

    def split_timelines(self) -> None:
        pass

    # def merge_timeline(self, Timeline) -> None:
    #     pass

    def progress_time(self) -> None:
        pass
