from multiprocessing import managers
import pygame
import yaml
from background_loan import Background_Loan
from background_stock import Background_Stock
from confirmation_dialog import UIConfirmationDialog
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UILabel, UIWindow, UIPanel
from pygame_gui.windows import UIMessageWindow
from timeline import Timeline
from typing import List
import json
import numpy as np

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_height = config["screen_height"]
screen_width = config["screen_width"]

class Background:

    # Singleton class has a private attribute  "instance"
    _instance = None

    # Called internally by Python when creating an object of a class
    def __new__(cls):
        if cls._instance is None:  # check whether the instance of the variable is None
            cls._instance = super(Background, cls).__new__(
                cls
            )  # create a new object with the super() method
        return (
            cls._instance
        )  # return the instance variable that contains the object of the Background class

    # Initialize attributes of the class
    def init_class(self, manager: UIManager, path_level_modules: List[str], index: int = 0):

        self.manager = manager
        self.scenario_end = False
        self.index = index

        # import level module file for current scenario
        self.path_level_modules = path_level_modules
        self.current_module_path = self.path_level_modules[self.index]
        self.load_data(self.current_module_path)

        # Game tracking information
        self.current_time = 1

        # UI poisitioning
        self.box_width = screen_width / 3
        self.box_height = 50
        self.top = 150

        # Creating timeline objects
        self.left_timeline = Timeline(self.manager, "left", self.box_width, self.box_height, self.top, self.stocks, self.loan, self.timestep, is_active=False, money = self.initial_money)
        self.center_timeline = Timeline(
            self.manager, "center", self.box_width, self.box_height, self.top, self.stocks, self.loan, self.timestep, is_active=True, money = self.initial_money)
        self.right_timeline = Timeline(
            self.manager, "right", self.box_width, self.box_height, self.top, self.stocks, self.loan, self.timestep, is_active=False, money = self.initial_money)
        self.timelines = [self.left_timeline, self.center_timeline, self.right_timeline]

        if self.create_loan_at_start:
            for timeline in self.timelines:
                timeline.take_loan(amount = self.start_loan_amount)

        # Creating buttons
        self.creation_button = UIButton(
            text="Split Timeline",
            tool_tip_text="Copy the current timeline into two",
            relative_rect=pygame.Rect(
                (screen_width - self.box_width) / 2,
                screen_height - 100,
                self.box_width,
                self.box_height,
            ),
            starting_height = 3,
            manager=self.manager,
            visible=True,
        )
        self.dropleft_button = UIButton(
            text="Drop Timeline",
            tool_tip_text="Delete this timeline",
            relative_rect=pygame.Rect(
                (screen_width / 3) - 3 * self.box_width / 4,
                screen_height - 100,
                self.box_width,
                self.box_height,
            ),
            starting_height = 3,
            manager=self.manager,
            visible=False,
        )
        self.dropright_button = UIButton(
            text="Drop Timeline",
            tool_tip_text="Delete this timeline",
            relative_rect=pygame.Rect(
                (2 * screen_width / 3) - self.box_width / 4,
                screen_height - 100,
                self.box_width,
                self.box_height,
            ),
            starting_height = 3,
            manager=self.manager,
            visible=False,
        )
        self.timeprogress_button = UIButton(
            text="Next "+self.timestep,
            tool_tip_text="Progress time within the scenario",
            relative_rect=pygame.Rect(
                (screen_width / 2) - self.box_width / 3,
                self.top/2-self.box_height/3,
                2*self.box_width/3,
                self.box_height,
            ),
            starting_height = 3,
            manager=self.manager,
            visible=True,
        )
        self.get_help_button = UIButton(
            text="Tutorial",
            tool_tip_text="Display the level tutorial",
            relative_rect=pygame.Rect(
                (screen_width / 35),
                (screen_height / 25),
                1*self.box_width/3,
                self.box_height,
            ),
            starting_height = 3,
            manager=self.manager,
            visible=True,
        )
        self.next_button = UIButton(
            text="Next",
            relative_rect=pygame.Rect(
                (screen_width / 35) + self.box_width/3 + 10,
                (screen_height / 25),
                1*self.box_width/3,
                self.box_height,
            ),
            starting_height = 3,
            manager=self.manager,
            visible=False,
        )

        # if this is the last scenario, the game should be restarted (load up scenario 1)
        if self.index == len(path_level_modules) - 1:
            text_button_2 = "Restart Game"
        else:
            text_button_2 = "Next Scenario"

        # window will appear if the user wins the scenario
        self.win_window = UIConfirmationDialog(
            pygame.Rect(
                ((screen_width/2) - (self.box_width/2)),
                ((screen_height/2) - (5*self.box_height/2)),
                (1 * self.box_width),
                (5 * self.box_height),
            ),
            manager=self.manager,
            window_title= "Victory!",
            action1_short_name="Restart Scenario",
            action2_short_name=text_button_2,
            action_long_desc=self.win_message,
            visible = 0
        )

        # window will appear if the user loses the scenario
        self.lose_window = UIConfirmationDialog(
            pygame.Rect(
                ((screen_width/2) - (self.box_width/2)),
                ((screen_height/2) - (5*self.box_height/2)),
                (1 * self.box_width),
                (5 * self.box_height),
            ),
            manager=self.manager,
            window_title= "Failure!",
            action1_short_name="Restart Scenario",
            action2_short_name=text_button_2,
            action_long_desc=self.lose_message,
            visible = 0
        )

        # window will appear if the user clicks on the next button
        self.end_choice_window = UIConfirmationDialog(
            pygame.Rect(
                ((screen_width/2) - (self.box_width/2)),
                ((screen_height/2) - (5*self.box_height/2)),
                (1 * self.box_width),
                (5 * self.box_height),
            ),
            manager=self.manager,
            window_title= "Next",
            action1_short_name="Restart Scenario",
            action2_short_name="Next Scenario",
            action_long_desc= "What's next?",
            visible = 0
        )

        self.update_labels()
        self.check_win_condition()
        self.display_tutorial()

    # update the days on the timeprogress label 
    def update_labels(self):
        try:
            self.timeprogress_label.kill()
        except:
            pass
        finally:
            self.timeprogress_panel = UIPanel(
            relative_rect = pygame.Rect(
                    (5*screen_width / 6) - self.box_width / 3,
                    self.top/2-self.box_height/3,
                    self.box_width/2,
                    self.box_height,
            ),
            starting_layer_height = 0,
            manager = self.manager,
        )
            self.timeprogress_label = UILabel(
                text=self.timestep+" "+str(self.current_time)+" / "+str(self.timelimit),
                relative_rect=pygame.Rect(
                    (5*screen_width / 6) - self.box_width / 3,
                    self.top/2-self.box_height/3,
                    self.box_width/2,
                    self.box_height,
            ),
            manager=self.manager,
            visible=True,
        )

    # read level_module JSON file and initialize stocks, loans and other variables
    def load_data(self, path_level_module: str) -> None:  
        file = open(path_level_module)
        data_module = json.load(file)

        self.initial_money = data_module["initial_money"]
        self.level_name = data_module["name"]

        self.stocks = []
        for stock in data_module["stocks"]:
            self.stocks.append(Background_Stock(stock['id'], stock['name'], stock['price'], stock['volatility'], stock['trend'], stock['change_in_trend'], stock['number_of_historical_prices']))
        
        self.create_loan_at_start = False

        # initialize the loan if there is one
        loan = data_module["loan"]
        if loan == "None":
            self.loan = None
        else:
            self.loan =  Background_Loan(loan['id'], loan['offered_interest_rate'], loan['volatility'], loan['trend'], loan['change_in_trend'], loan['c_2_in_trend'], loan['number_of_historical_interest_rates'],loan['max_amount_multiplier'])
            if loan['exists'] == 1:
                self.create_loan_at_start = True
                self.start_loan_amount = loan ['amount_if_taken']

        self.tutorial = data_module['tutorial']

        self.timestep = data_module["timestep"]
        self.timelimit = data_module["timelimit"]

        self.win_cond_type = data_module['win_cond_type']
        self.win_cond = data_module['win_cond']
        self.win_message = data_module['win_message']
        self.lose_message = data_module['lose_message']

    def get_stock(self, id: int) -> Background_Stock:
        for stock in self.stocks:
            if stock.get_id() == id:
                return stock
        return None

    def get_loan(self) -> Background_Loan:
        return self.loan

    # copy center timeline information into left and right timelines
    def split_timelines(self) -> None:
        self.copy_data(self.center_timeline, self.left_timeline)
        self.copy_data(self.center_timeline, self.right_timeline)

        for tl in self.timelines:
            tl.switch_activity()

        self.creation_button.hide()
        self.dropleft_button.show()
        self.dropright_button.show()

    # copy given timeline information into center timeline
    def merge_timeline(self, timeline: Timeline) -> None:
        self.copy_data(timeline, self.center_timeline)

        for tl in self.timelines:
            tl.switch_activity()
            self.creation_button.show()
            self.dropleft_button.hide()
            self.dropright_button.hide()

    # update all time-variable attributes
    def progress_time(self) -> None:
        self.current_time += 1
        self.update_labels()

        if self.current_time >= self.timelimit+1:
            self.scenario_end = True
            self.end_scenario("Failure")

        # call progress time for background stocks
        for stock in self.stocks:
            stock.progress_time()

        # call progress time for the background loan if it exists
        if self.loan != None:
            self.loan.progress_time()

        for timeline in self.timelines:
            timeline.progress_time()


    # end the scenario
    def end_scenario(self, type_end: str) -> None:
        self.timeprogress_button.kill()
        self.scenario_end_panel = UIPanel(
            relative_rect = pygame.Rect(
                (screen_width / 2) - self.box_width / 3,
                self.top/2-self.box_height/3,
                2*self.box_width/3,
                self.box_height,
            ),
            starting_layer_height = 0,
            manager = self.manager,
        )
        self.timeprogress_button = UILabel(
            text="Scenario End - " + type_end,
            relative_rect=pygame.Rect(
                (screen_width / 2) - self.box_width / 3,
                self.top/2-self.box_height/3,
                2*self.box_width/3,
                self.box_height,
            ),
            manager = self.manager,
            visible = True
        )
        self.timeprogress_button.disable()

        # display window with win or lose message
        if type_end == "Victory!":
            self.win_window.show()
        else:
            self.lose_window.show()

        # create button to go to next scenario
        self.next_button.show()

    # called every time the user clicks on a button            
    def button_pressed(self, event) -> None:
        if event.ui_element == self.creation_button:
            self.split_timelines()
        elif event.ui_element == self.dropleft_button:
            self.merge_timeline(self.right_timeline)
        elif event.ui_element == self.dropright_button:
            self.merge_timeline(self.left_timeline)
        elif event.ui_element == self.timeprogress_button:
            self.progress_time()
        elif event.ui_element == self.get_help_button:
            self.display_tutorial()
        elif event.ui_element == self.next_button:
            self.end_choice_window.show()
        elif event.ui_element == self.win_window.action1_button:
            self.restart_scenario()
        elif event.ui_element == self.win_window.action2_button:
            self.go_to_next_scenario()
        elif event.ui_element == self.lose_window.action1_button:
            self.restart_scenario()
        elif event.ui_element == self.lose_window.action2_button:
            self.go_to_next_scenario()
        elif event.ui_element == self.end_choice_window.action1_button:
            self.restart_scenario()
        elif event.ui_element == self.end_choice_window.action2_button:
            self.go_to_next_scenario()
        else:
            for timeline in self.timelines:
                # call button_pressed() in each timeline 
                if timeline.button_pressed(event): # if returns true, no need to check for other timelines
                    break
        for timeline in self.timelines:
            timeline.update_boxes()
            for stock in timeline.stocks:
                stock.update_boxes()
            if timeline.loan != None:
                timeline.loan.update_boxes()
    
        self.check_lose_condition()
        self.check_win_condition()
    
    def display_tutorial(self) -> None:
        try: 
            self.tutorial_window.kill()
        except:
            pass
        finally:
            self.tutorial_window = UIMessageWindow(
                pygame.Rect(
                    (2 * screen_width / 8),
                    (2 * screen_height / 12),
                    (1.5 * self.box_width),
                    (8 * self.box_height),
                ),
                manager=self.manager,
                window_title= self.level_name,
                html_message=self.tutorial
            )
    
    # copy data from 1 timeline to another when the user splits or merges timelines
    def copy_data(self, sender_timeline: Timeline, receiver_timeline: Timeline) -> None:
        receiver_timeline.update_attributes(sender_timeline.get_money(), sender_timeline.get_net_worth(), sender_timeline.get_stocks(), sender_timeline.get_loan(), sender_timeline.timeline_panel)
    
    def check_win_condition(self) -> None:
        # if win_cond_type == "money": 
        #     win_cond = int
        # if win_cond_type == "stock":
        #     win_cond = dictionary of stocks and volume for each stock
        # if win_cond_type = "loan":
        #     wind_cond = "None" 
        
        # the win condition is to reach a particular amount of money
        if self.win_cond_type == "money":
            for timeline in self.timelines:
                if timeline.get_is_active() and timeline.get_money() >= self.win_cond and self.scenario_end == False:
                    self.scenario_end = True
                    self.end_scenario("Victory!")

        # the win condition is to buy a particular amount of stocks and have no debt remaining
        elif self.win_cond_type == "stock":
            for timeline in self.timelines:
                if timeline.get_is_active():
                    win = True
                    for stock in timeline.get_stocks():
                        if stock.get_volume() < self.win_cond[str(stock.get_id())]:
                            win = False
                    if self.loan != None:
                        if timeline.get_loan().have_loan():
                                win = False
                    if win == True and self.scenario_end == False:
                        self.scenario_end = True
                        self.end_scenario("Victory!")
                        break          
        
        # the win condition is to reimburse a loan
        elif self.win_cond_type == "loan":
            for timeline in self.timelines:
                if timeline.get_is_active() and timeline.get_loan().get_amount_owed() <= 0:
                    if self.scenario_end == False:
                        self.scenario_end = True
                        self.end_scenario("Victory!")
                        break

    
    def check_lose_condition(self) -> None:
        # if the user has no money and no stock
        if self.center_timeline.get_is_active() == True:
            if self.center_timeline.get_money() <= 0:
                volume_stocks = 0
                for stock in self.center_timeline.get_stocks():
                    volume_stocks += stock.get_volume()
                if volume_stocks == 0:
                    if self.scenario_end == False:
                        self.scenario_end = True
                        self.end_scenario("Failure")
    
    def restart_scenario(self) -> None:
        self.manager.clear_and_reset()
        self.init_class(manager = self.manager, path_level_modules = self.path_level_modules, index = self.index)

    def go_to_next_scenario(self) -> None:    
        self.manager.clear_and_reset()
        self.init_class(manager = self.manager, path_level_modules = self.path_level_modules, index = (self.index + 1)%len(self.path_level_modules))
    