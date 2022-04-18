from background_loan import Background_Loan
from information_popup import Information_Popup
import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UIButton, UITextBox, UILabel

class Timeline_Loan:
    def __init__(
        self,
        # id: int,
        loan_reference: Background_Loan,
        timeline_reference,
        top: int,
        box_width: int,
        box_height: int,
        timeline_panel: UIPanel,
        manager: UIManager,
        timestep: str,
        amount_owed: int = 0,
        interest_at_borrowing = None,
    ) -> None:
        self.box_width = box_width
        self.box_height = box_height
        self.left = 0
        self.top = top
        self.manager = manager
        self.timestep = timestep

        # self.id = id
        self.amount_owed = amount_owed
        self.interest_at_borrowing = interest_at_borrowing
        self.loan_reference = loan_reference
        self.timeline_reference = timeline_reference
        self.timestep = timestep

        self.loan_panel_offered = UIPanel(
            relative_rect=pygame.Rect(self.left, self.top, self.box_width + 6, self.box_height * 3 + 10),
            starting_layer_height=0,
            manager=self.manager,
            container=timeline_panel,
            visible=True,
        )        

        self.loan_panel_taken = UIPanel(
            relative_rect=pygame.Rect(self.left, self.top, self.box_width + 6, self.box_height * 3 + 10),
            starting_layer_height=0,
            manager=self.manager,
            container=timeline_panel,
            visible=False,
        )    

        self.namelabel_1 = UILabel(
            relative_rect = pygame.Rect(0,0,self.box_width,self.box_height),
            text = "Loan",
            manager = self.manager,
            container = self.loan_panel_offered,
            )

        self.namelabel_2 = UILabel(
            relative_rect = pygame.Rect(0,0,self.box_width,self.box_height),
            text = "Loan",
            manager = self.manager,
            container = self.loan_panel_taken,
            )

        self.offered_ir_box = UITextBox(
            html_text = "Interest rate: "+f"{self.loan_reference.get_offered_interest_rate():.2f}",
            relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.loan_panel_offered,
        )            

        self.max_amount_box = UITextBox(
            html_text = "Max amount: "+str(self.get_max_amount()),
            relative_rect = pygame.Rect(self.box_width/2,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.loan_panel_offered,
        )            

        self.information_button_1 = UIButton(
            relative_rect = pygame.Rect(self.box_height*0.1,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "i",
            manager = manager,
            container = self.loan_panel_offered,
            tool_tip_text = "Display historical information about the loan"
        )      

        self.information_button_2 = UIButton(
            relative_rect = pygame.Rect(self.box_height*0.1,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "i",
            manager = manager,
            container = self.loan_panel_taken,
            tool_tip_text = "Display historical information about the loan"
        )        

    def update_boxes(self) -> None:
        pass

    def progress_time(self) -> None:
        self.update_boxes()
        try:
            self.offered_ir_box.kill()
            self.max_amount_box.kill()
        except:
            pass
        finally:
            self.offered_ir_box = UITextBox(
            html_text = "Interest rate: "+f"{self.loan_reference.get_offered_interest_rate():.2f}",
            relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.loan_panel_offered,
            )           
            self.max_amount_box = UITextBox(
                html_text = "Max allowed: "+str(self.get_max_amount()),
                relative_rect = pygame.Rect(self.box_width/2,self.box_height,self.box_width/2,self.box_height),
                manager = self.manager,
                container = self.loan_panel_offered,
            )   
    
    def get_max_amount(self) -> int:
        return int(self.timeline_reference.net_worth *  self.loan_reference.get_max_amount_multiplier())

    def progress_amount_owed(self) -> int:
        if self.interest_at_borrowing != None:
            self.amount_owed = int(self.amount_owed * (1 + self.interest_at_borrowing) + 1) # round up

    def take_loan(self, amount: int) -> None:
        self.amount_owed = amount
        self.interest_at_borrowing = self.loan_reference.get_offered_interest_rate()

    def get_loan_reference(self) -> Background_Loan:
        return self.loan_reference

    def pay_off(self, amount: int) -> None:
        self.amount_owed -= amount
        if self.amount_owed == 0:
            self.interest_at_borrowing = None

    def get_amount_owed(self) -> int:
        return self.amount_owed

    def have_loan(self) -> bool:
        return not self.amount_owed

    def display_info(self) -> None:
        try:
            self.info_popup.kill()
        except:
            pass
        finally:
            self.info_popup = Information_Popup("Historical Loan Interest Rates", self.loan_reference.get_historical_interest_rates(), self.loan_reference.get_initial_number_of_historical_interest_rates(), self.timestep, "interest rate", self.manager)
            self.info_popup.display_graph()

    def button_pressed(self, event) -> bool:
        if event.ui_element == self.information_button_1:
            self.display_info()
        elif event.ui_element == self.information_button_2:
            self.display_info()
        else:
            return False
        return True

    def update_attributes(self, new_loan: any) -> None:
        # [TODO] update loan attributes
        # [TODO] self.update_boxes()
        pass
