from background_loan import Background_Loan
from background_stock import Background_Stock

from timeline import Timeline

import pygame
import pygame_gui
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import UIButton, UILabel, UIPanel, UITextBox

import yaml
with open("config.yaml") as config_file:

    config = yaml.safe_load(config_file)
screen_length = config["screen_length"]
screen_width = config["screen_width"]

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
        self.box_width = screen_length/3                    
        self.left_timeline = Timeline(manager, "left", self.box_width, is_active = False)
        self.center_timeline = Timeline(manager, "center", self.box_width, is_active = True)
        self.right_timeline = Timeline(manager, "right", self.box_width, is_active = False)
        self.timelines = [self.left_timeline, self.center_timeline, self.right_timeline]
        self.creation_button = UIButton(text= "Split Timeline", tool_tip_text = 'Copy the current timeline into two',
                            relative_rect=pygame.Rect((screen_length-self.box_width)/2, screen_width-100,self.box_width,50),
                            manager = manager,
                            visible = True)   
        self.dropleft_button = UIButton(text= "Drop Timeline", tool_tip_text = 'Delete this timeline',
                            relative_rect=pygame.Rect((screen_length/3) - 3*self.box_width/4, screen_width-100,self.box_width,50),
                            manager = manager,
                            visible = False)   
        self.dropright_button = UIButton(text= "Drop Timeline", tool_tip_text = 'Delete this timeline',
                            relative_rect=pygame.Rect((2*screen_length/3) - self.box_width/4, screen_width-100,self.box_width,50),
                            manager = manager,
                            visible = False)                                                               

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
        for tl in self.timelines:
            tl.switch_activity()

        self.creation_button.hide()
        self.dropleft_button.show()
        self.dropright_button.show()

        #[TODO] copy center timeline information into left and right timelines

    def merge_timeline(self, Timeline) -> None:
       for tl in self.timelines:
           tl.switch_activity()
           self.creation_button.show()
           self.dropleft_button.hide()
           self.dropright_button.hide()
        
        #[TODO] copy given timeline information into center timeline

    def progress_time(self) -> None:
        pass

    def button_pressed(self, event):
        if event.ui_element == self.creation_button:
            self.split_timelines()
        elif event.ui_element == self.dropleft_button:
            self.merge_timeline(self.right_timeline)
        elif event.ui_element == self.dropright_button:
            self.merge_timeline(self.left_timeline)

        for timeline in self.timelines:
            pass