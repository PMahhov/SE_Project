from binascii import rlecode_hqx
from background_loan import Background_Loan
from information_popup import Information_Popup
import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UIButton, UITextBox, UILabel, UITextEntryLine
from pygame_gui.windows import UIMessageWindow

import yaml

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_height = config["screen_height"]
screen_width = config["screen_width"]
info_loan = config["info_loan"]

class UINumberEntryLine(UITextEntryLine):
    def set_select_reference(self, select_button):
        self.select_reference = select_button

    def focus(self):
        # from the pygame module
        super().focus()
        pygame.key.set_repeat(500, 25)

        # new addition to the function
        self.set_text("")
        self.set_allowed_characters("numbers")

        self.select_reference.enable()

    def unfocus(self):
        # from the pygame module
        super().unfocus()
        pygame.key.set_repeat(0)
        self.select_range = [0, 0]
        self.edit_position = 0
        self.cursor_on = False
        self.text_entered = False
        self.redraw()

        # # new addition to the function
        # self.allowed_characters = None
        # self.set_text("[Click to Enter]")        

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

        self.UIobjects = []

        self.loan_panel_offered = UIPanel(
            relative_rect=pygame.Rect(self.left, self.top, self.box_width + 6, self.box_height * 3 + 10),
            starting_layer_height=0,
            manager=self.manager,
            container=timeline_panel,
            visible = not self.have_loan(),
        )        
        self.UIobjects.append(self.loan_panel_offered)

        self.loan_panel_taken = UIPanel(
            relative_rect=pygame.Rect(self.left, self.top, self.box_width + 6, self.box_height * 3 + 10),
            starting_layer_height=0,
            manager=self.manager,
            container=timeline_panel,
            visible = self.have_loan(),
        )    
        self.UIobjects.append(self.loan_panel_taken)

        self.namelabel_1 = UILabel(
            relative_rect = pygame.Rect(0,0,self.box_width,self.box_height),
            text = "Loan (offered)",
            manager = self.manager,
            container = self.loan_panel_offered,
            )
        self.UIobjects.append(self.namelabel_1)

        self.namelabel_2 = UILabel(
            relative_rect = pygame.Rect(0,0,self.box_width,self.box_height),
            text = "Loan (taken)",
            manager = self.manager,
            container = self.loan_panel_taken,
            )
        self.UIobjects.append(self.namelabel_2)

        self.offered_ir_box = UITextBox(
            html_text = "Interest rate: "+f"{self.loan_reference.get_offered_interest_rate():.2f}",
            relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.loan_panel_offered,
        )            
        self.UIobjects.append(self.offered_ir_box)          

        self.max_amount_box = UITextBox(
            html_text = "Max amount: "+str(self.get_max_amount()),
            relative_rect = pygame.Rect(self.box_width/2,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.loan_panel_offered,
        )            
        self.UIobjects.append(self.max_amount_box)

        self.graph_button_1 = UIButton(
            relative_rect = pygame.Rect((self.box_height*0.9)+5,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "h",
            manager = manager,
            starting_height = 2,
            container = self.loan_panel_offered,
            tool_tip_text = "Display historical information about the loan"
        )      
        self.UIobjects.append(self.graph_button_1)

        self.graph_button_2 = UIButton(
            relative_rect = pygame.Rect((self.box_height*0.9)+5,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "h",
            manager = manager,
            starting_height = 2,
            container = self.loan_panel_taken,
            tool_tip_text = "Display a graph with historical information about the loan"
        )     
        self.UIobjects.append(self.graph_button_2)

        self.information_button_1 = UIButton(
            relative_rect = pygame.Rect(self.box_height*0.1,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "i",
            manager = manager,
            starting_height = 2,
            container = self.loan_panel_offered,
            tool_tip_text = "Display information about loans"
        ) 
        self.UIobjects.append(self.information_button_1)  
        
        self.information_button_2 = UIButton(
            relative_rect = pygame.Rect(self.box_height*0.1,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "i",
            manager = manager,
            starting_height = 2,
            container = self.loan_panel_taken,
            tool_tip_text = "Display information about loans"
        )   
        self.UIobjects.append(self.information_button_2)

        self.take_loan_button = UIButton(
            relative_rect = pygame.Rect(0, self.box_height * 2, self.box_width / 4, self.box_height),
            text = "Take loan",
            manager = manager,
            container = self.loan_panel_offered,
            tool_tip_text = "Take out a loan with the offered interest rate",
        )
        self.take_loan_button.disable()
        self.UIobjects.append(self.take_loan_button)

        self.pay_loan_button = UIButton(
            relative_rect = pygame.Rect(0, self.box_height * 2, self.box_width / 4, self.box_height),
            text = "Pay back",
            manager = manager,
            container = self.loan_panel_taken,
            tool_tip_text = "Pay off a portion of the taken loan",
        )        
        self.pay_loan_button.disable()
        self.UIobjects.append(self.pay_loan_button)

        self.select_loan_button = UIButton(
            relative_rect = pygame.Rect(15/24 * self.box_width, self.box_height * 2, self.box_width / 6, self.box_height),
            text = "Select",
            manager = manager,
            container = self.loan_panel_offered,
            tool_tip_text = "Select the amount you will take a loan out for",
        )        
        self.select_loan_button.disable()
        self.UIobjects.append(self.select_loan_button)

        self.select_pay_button = UIButton(
            relative_rect = pygame.Rect(15/24 * self.box_width, self.box_height * 2, self.box_width / 6, self.box_height),
            text = "Select",
            manager = manager,
            container = self.loan_panel_taken,
            tool_tip_text = "Select the amount that you will pay back",
        )             
        self.select_pay_button.disable()
        self.UIobjects.append(self.select_pay_button)

        self.take_loan_entry = UINumberEntryLine(
            relative_rect = pygame.Rect(self.box_width/4, self.box_height * 2, 9*self.box_width / 24, self.box_height),
            manager = manager,
            container = self.loan_panel_offered,
        )
        self.take_loan_entry.set_text("[Click to Enter]")   
        self.take_loan_entry.set_select_reference(self.select_loan_button)
        self.UIobjects.append(self.take_loan_entry)

        self.pay_loan_entry = UINumberEntryLine(
            relative_rect = pygame.Rect(self.box_width/4, self.box_height * 2, 9*self.box_width / 24, self.box_height),
            manager = manager,
            container = self.loan_panel_taken,
        )
        self.pay_loan_entry.set_text("[Click to Enter]")
        self.pay_loan_entry.set_select_reference(self.select_pay_button)
        self.UIobjects.append(self.pay_loan_entry)


        self.take_max_loan_button = UIButton(
            relative_rect = pygame.Rect(19/24 * self.box_width, self.box_height * 2, self.box_width / 7, self.box_height),
            text = "Max",
            manager = manager,
            container = self.loan_panel_offered,
            tool_tip_text = "Select the maximum amount you can take a loan out for",            
        )
        self.UIobjects.append(self.take_max_loan_button)

        self.pay_max_loan_button = UIButton(
            relative_rect = pygame.Rect(19/24 * self.box_width, self.box_height * 2, self.box_width / 7, self.box_height),
            text = "Max",
            manager = manager,
            container = self.loan_panel_taken,
            tool_tip_text = "Select the maximum amount you can back your loan with",            
        )
        self.UIobjects.append(self.pay_max_loan_button)

        self.update_boxes()

    def update_boxes(self) -> None:
        
        if self.timeline_reference.timeline_panel.vert_scroll_bar != None:
            for object in self.UIobjects:
                self.timeline_reference.timeline_panel.vert_scroll_bar.join_focus_sets(object)

        if self.timeline_reference.is_active:
            if self.have_loan():
                self.loan_panel_offered.hide()
                self.loan_panel_taken.show()
            else:
                self.loan_panel_offered.show()
                self.loan_panel_taken.hide()

        self.take_loan_entry.set_text_length_limit(max(len(str(self.get_max_amount())),16))         # input limit changes dynamically according to the length of the current max input value, but not below 16 so the "click to enter" message can be displayed
        self.pay_loan_entry.set_text_length_limit(max(len(str(self.get_amount_owed())),16))

        try: 
            self.taken_ir_box.kill()
            self.amount_owed_box.kill()
        except:
            pass
        finally:
            if self.have_loan() == True:
                self.taken_ir_box = UITextBox(
                    html_text = "Interest rate: "+f"{self.interest_at_borrowing:.2f}",
                    relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
                    manager = self.manager,
                    container = self.loan_panel_taken,
                ) 
                if self.timeline_reference.timeline_panel.vert_scroll_bar != None:
                    self.timeline_reference.timeline_panel.vert_scroll_bar.join_focus_sets(self.taken_ir_box)

            self.amount_owed_box = UITextBox(
                html_text = "Current debt: "+str(self.get_amount_owed()),
                relative_rect = pygame.Rect(self.box_width/2,self.box_height,self.box_width/2,self.box_height),
                manager = self.manager,
                container = self.loan_panel_taken,
            )    
            if self.timeline_reference.timeline_panel.vert_scroll_bar != None:
                self.timeline_reference.timeline_panel.vert_scroll_bar.join_focus_sets(self.amount_owed_box)                  

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
                html_text = "Max amount: "+str(self.get_max_amount()),
                relative_rect = pygame.Rect(self.box_width/2,self.box_height,self.box_width/2,self.box_height),
                manager = self.manager,
                container = self.loan_panel_offered,
            )   
    
    def get_max_amount(self) -> int:
        return int(self.timeline_reference.net_worth *  self.loan_reference.get_max_amount_multiplier())

    def progress_amount_owed(self) -> int:
        if self.interest_at_borrowing != None:
            self.amount_owed = int(self.amount_owed * (1 + self.interest_at_borrowing/100) + 1) # round up

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
        if self.amount_owed > 0:
            return True
        else:
            return False
    

    def display_graph(self) -> None:
        try:
            self.info_popup.kill()
        except:
            pass
        finally:
            self.info_popup = Information_Popup("Historical Loan Interest Rates", self.loan_reference.get_historical_interest_rates(), self.loan_reference.get_initial_number_of_historical_interest_rates(), self.timestep, "interest rate", self.manager)
            self.info_popup.display_graph()

    def button_pressed(self, event) -> bool:
        if event.ui_element == self.graph_button_1:
            self.display_graph()
        elif event.ui_element == self.graph_button_2:
            self.display_graph()
        elif event.ui_element == self.information_button_1:
            self.display_info()
        elif event.ui_element == self.information_button_2:
            self.display_info()

        elif event.ui_element == self.take_max_loan_button:
            self.take_loan_entry.set_text(str(self.get_max_amount()))
            self.current_amount = self.get_max_amount()
            self.take_loan_button.enable()

        elif event.ui_element == self.pay_max_loan_button:
            self.pay_loan_entry.set_text(str(self.get_amount_owed()))
            self.current_amount = self.get_amount_owed()
            self.pay_loan_button.enable()

        elif event.ui_element == self.select_loan_button:
            input = self.take_loan_entry.get_text()
            if input == "":
                proposed_amount = 0
            else:
                proposed_amount = int(self.take_loan_entry.get_text())

            if proposed_amount > self.get_max_amount():                         # if the user inputs too large of a loan proposal, it defaults to max
                self.take_loan_entry.set_text(str(self.get_max_amount()))
                self.current_amount = self.get_max_amount()
                self.take_loan_button.enable()

            elif proposed_amount > 0:
                self.take_loan_entry.set_text(str(proposed_amount))
                self.current_amount = proposed_amount
                self.take_loan_button.enable()
    
            else:
                self.take_loan_button.disable()

        elif event.ui_element == self.take_loan_button:
            self.timeline_reference.take_loan(self.current_amount)
            self.current_amount = None
            self.pay_loan_button.disable()
            if self.pay_loan_entry.get_text() != "[Click to Enter]":
                self.pay_loan_entry.set_text("")

        elif event.ui_element == self.select_pay_button:
            input = self.pay_loan_entry.get_text()
            if input == "":
                proposed_amount = 0
            else:
                proposed_amount = int(self.pay_loan_entry.get_text())

            if proposed_amount > self.get_amount_owed():
                self.pay_loan_entry.set_text(str(self.get_amount_owed()))
                self.current_amount = self.get_amount_owed()
                self.pay_loan_button.enable()
            
            elif proposed_amount > 0:
                self.pay_loan_entry.set_text(str(proposed_amount))
                self.current_amount = proposed_amount
                self.pay_loan_button.enable()

            else:
                self.pay_loan_button.disable()

        elif event.ui_element == self.pay_loan_button:
            self.timeline_reference.pay_loan(self.current_amount)
            self.current_amount = None
            self.take_loan_button.disable()
            self.pay_loan_button.disable()

        else:
            return False
        return True

    def update_attributes(self, new_loan: any) -> None:
        self.amount_owed = new_loan.amount_owed
        self.interest_at_borrowing = new_loan.interest_at_borrowing
        self.update_boxes()

    # when i button clicked, display general information about loans
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
                window_title= "Loans",
                html_message=info_loan
            )