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
import json
import numpy as np

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_height = config["screen_height"]
screen_width = config["screen_width"]


class Background:

    _instance = None

    # Called internally by Python when creating an object of a class
    def __new__(cls):
        if cls._instance is None:  # check whether the instance of the variable is None
            print("Creating the object")
            cls._instance = super(Background, cls).__new__(
                cls
            )  # create a new object with the super() method
        return (
            cls._instance
        )  # return the instance variable that contains the object of the Background class

    # Initialize attributes of the class
    def init_class(self, manager: UIManager, path_level_module: str):

        self.manager = manager
        self.scenario_end = False

        self.load_data(path_level_module)

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
            manager=self.manager,
            visible=False,
        )

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
            action2_short_name="Next Scenario",
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
            action2_short_name="Next Scenario",
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

    def load_data(self, path_level_module: str) -> None:  
        # read level_module JSON file and initialize stocks, loans and other variables
        file = open(path_level_module)
        data_module = json.load(file)

        self.initial_money = data_module["initial_money"]
        
        self.stocks = []
        for stock in data_module["stocks"]:
            self.stocks.append(Background_Stock(stock['id'], stock['name'], stock['price'], stock['volatility'], stock['trend'], stock['number_of_historical_prices']))
        
        loan = data_module["loan"]
        if loan == "None":
            self.loan = None
        else:
            self.loan =  Background_Loan(loan['id'], loan['offered_interest_rate'], loan['volatility'], loan['trend'], loan['number_of_historical_interest_rates'],loan['max_amount_multiplier'])

        self.transaction_cost = data_module['transaction_cost']
        self.tutorial = data_module['tutorial']

        self.timestep = data_module["timestep"]
        self.timelimit = data_module["timelimit"]

        # [TODO] add win conditions and win condition type
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

    def split_timelines(self) -> None:
        # copy center timeline information into left and right timelines
        self.copy_data(self.center_timeline, self.left_timeline)
        self.copy_data(self.center_timeline, self.right_timeline)

        for tl in self.timelines:
            tl.switch_activity()

        self.creation_button.hide()
        self.dropleft_button.show()
        self.dropright_button.show()

    def merge_timeline(self, timeline: Timeline) -> None:
        # copy given timeline information into center timeline
        self.copy_data(timeline, self.center_timeline)

        for tl in self.timelines:
            tl.switch_activity()
            self.creation_button.show()
            self.dropleft_button.hide()
            self.dropright_button.hide()

    def progress_time(self) -> None:
        self.current_time += 1
        self.update_labels()

        if self.current_time >= self.timelimit:
            self.scenario_end = True
            self.end_scenario("Failure")

        # call progress time for background stocks
        for stock in self.stocks:
            stock.progress_time()

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

        # display window with win message
        if type_end == "Victory!":
            self.win_window.show()
        else:
            self.lose_window.show()

        # create button to go to next scenario
        self.next_button.show()
                 
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
                window_title= "Tutorial",
                html_message=self.tutorial
            )
    
    def copy_data(self, sender_timeline: Timeline, receiver_timeline: Timeline) -> None:
        receiver_timeline.update_attributes(sender_timeline.get_money(), sender_timeline.get_net_worth(), sender_timeline.get_stocks(), sender_timeline.get_loan())
    

    def check_win_condition(self) -> None:
        # if win_cond_type == "money": 
        #     win_cond = int
        # if win_cond_type == "stocks":
        #     win_cond = dictionary of stocks and volume for each stock
        # if win_cond_type = "loan":
        #     wind_cond = None 
        
        # the win condition is to reach a particular amount of money
        if self.win_cond_type == "money":
            for timeline in self.timelines:
                if timeline.get_is_active() and timeline.get_money() >= self.win_cond and self.scenario_end == False:
                    self.scenario_end = True
                    self.end_scenario("Victory!")

        # the win condition is to buy a particular amount of stocks
        elif self.win_cond_type == "stock":
            for timeline in self.timelines:
                if timeline.get_is_active():
                    win = True
                    for stock in timeline.get_stocks():
                        if stock.get_volume() < self.win_cond_type[stock.get_id()]:
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
        
        # [TODO]: are there other loose conditions?
    
    def restart_scenario(self) -> None:
        print("restart scenario")
        # [TODO] restart scenario

    def go_to_next_scenario(self) -> None:
        print("go to next scenario")
         # [TODO] go to the next scenario 