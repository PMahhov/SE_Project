import pygame
import yaml
from background_loan import Background_Loan
from background_stock import Background_Stock
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UILabel
from timeline import Timeline

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
    def init_class(self, manager: UIManager):

        self.manager = manager
        self.game_end = False

        # Information provided by the level module
        self.timestep = "Day"  # options: "Day", "Month", "Year"
        self.timelimit = 5
            # how many stocks/loans to create, parameters for each

        # Game tracking information
        self.current_time = 1

        # UI poisitioning
        self.box_width = screen_width / 3
        self.box_height = 50
        self.top = 150

        # Creating timeline objects
        self.left_timeline = Timeline(self.manager, "left", self.box_width, self.box_height, self.top, is_active=False)
        self.center_timeline = Timeline(
            self.manager, "center", self.box_width, self.box_height, self.top, is_active=True
        )
        self.right_timeline = Timeline(
            self.manager, "right", self.box_width, self.box_height, self.top, is_active=False
        )
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

        self.update_labels()

    # self.timelines = timelines
    # self.stocks = stocks
    # self.loan = loan
    # self.transation_cost = transaction_cost
    # self.win_cond_type = win_cond_type
    # self.win_conds = win_conds

    def update_labels(self):
        try:
            self.timeprogress_label.kill()
        except:
            pass
        finally:
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

        # [TODO] copy center timeline information into left and right timelines

    def merge_timeline(self, Timeline) -> None:
        for tl in self.timelines:
            tl.switch_activity()
            self.creation_button.show()
            self.dropleft_button.hide()
            self.dropright_button.hide()

        # [TODO] copy given timeline information into center timeline

    def progress_time(self) -> None:
        self.current_time += 1
        self.update_labels()

        if self.current_time >= self.timelimit:
            self.game_end = True
            self.end_game()

        for timeline in self.timelines:
            timeline.progress_time()


    def end_game(self) -> None:
        self.timeprogress_button.kill()
        self.timeprogress_button = UILabel(
            text="Scenario End",
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

    def button_pressed(self, event):
        if event.ui_element == self.creation_button:
            self.split_timelines()
        elif event.ui_element == self.dropleft_button:
            self.merge_timeline(self.right_timeline)
        elif event.ui_element == self.dropright_button:
            self.merge_timeline(self.left_timeline)
        elif event.ui_element == self.timeprogress_button:
            self.progress_time()

        for timeline in self.timelines:
            pass
