import pygame
import yaml
from background_loan import Background_Loan
from information_popup import Information_Popup
from pygame_gui import UIManager
from pygame_gui.elements import (UIButton, UILabel, UIPanel, UITextBox,
                                 UITextEntryLine)
from pygame_gui.windows import UIMessageWindow

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_height = config["screen_height"]
screen_width = config["screen_width"]
info_loan = config["info_loan"]

class UINumberEntryLine(UITextEntryLine):
    """
    A helper UI class. Overwriting some methods in parent class UITextEntryLine from PygameGUI to fit system: 
        - Number only entry
    Refer to PyGameGUI documentation for specifics: https://pygame-gui.readthedocs.io/en/latest/pygame_gui.elements.html#module-pygame_gui.elements.ui_text_entry_line. 
    """
    def set_select_reference(self, select_button):
        self.select_reference = select_button

    def focus(self):
        # from the pygame module
        super().focus()
        pygame.key.set_repeat(500, 25)

        # new addition to the function, limits allowed characters to just numeric
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
    """
    Represents the status of loan taken by a timeline

    ...
    ATTRIBUTES (non-GUI)
    --------------------
    amount_owed : int [0, inf)
        amount taken on loan
    interest_at_borrowing : float [0.2, inf)
        percentage increase on amount_owed after each timeskip. This is fixed for the duration of the loan
    loan_reference : Background_Loan
        reference to the Background_Loan object upon which this instance of Timeline_Loan was based
    timeline_reference : Timeline
        reference to the Timeline object in which this instance of Timeline_Loan was created

    METHODS (non-GUI)
    -----------------
    get_max_amount : int
        returns the maximal amount borrowable by the timeline, proportional to timeline's net worth
    progress_amount_owed : None
        causes percentage increase on amount_owed based on interest_at_borrowing
    take_loan : None
        takes loan for timeline equal to amount argument
    pay_loan : None
        reduces timeline money and amount_owed to pay off a part (or all) of loan
    have_loan : bool
        returns True is timeline has a loan i.e. amount_owed > 0
    """
    def __init__(
        self,
        loan_reference: Background_Loan,
        timeline_reference,
        top: int,
        box_width: int,
        box_height: int,
        timeline_panel: UIPanel,
        manager: UIManager,
        timestep: str,
        amount_owed: int = 0,
        interest_at_borrowing: float = None,
    ) -> None:

        # GUI attributes
        self.box_width = box_width
        self.box_height = box_height
        self.left = 0
        self.top = top
        self.manager = manager
        self.timestep = timestep

        # Relevant data attributes
        self.amount_owed = amount_owed
        self.interest_at_borrowing = interest_at_borrowing
        self.loan_reference = loan_reference
        self.timeline_reference = timeline_reference

        self.UIobjects = []

        # Timeline_Loan is presented as "Loan (offered)" panel if timeline has not taken a loan 
        self.loan_panel_offered = UIPanel(
            relative_rect=pygame.Rect(
                self.left, self.top, self.box_width + 6, self.box_height * 3 + 10
            ),
            starting_layer_height=0,
            manager=self.manager,
            container=timeline_panel,
            visible = not self.have_loan(),
        )        
        self.UIobjects.append(self.loan_panel_offered)

        # Timeline_Loan is presented as "Loan (taken)" panel if timeline has taken a loan
        self.loan_panel_taken = UIPanel(
            relative_rect=pygame.Rect(
                self.left, self.top, self.box_width + 6, self.box_height * 3 + 10
            ),
            starting_layer_height=0,
            manager=self.manager,
            container=timeline_panel,
            visible = self.have_loan(),
        )    
        self.UIobjects.append(self.loan_panel_taken)

        # Label for "Loan (offered)" panel
        self.namelabel_1 = UILabel(
            relative_rect = pygame.Rect(0,0,self.box_width,self.box_height),
            text = "Loan (offered)",
            manager = self.manager,
            container = self.loan_panel_offered,
            )
        self.UIobjects.append(self.namelabel_1)

        # Label for "Loan (taken)" panel
        self.namelabel_2 = UILabel(
            relative_rect = pygame.Rect(0,0,self.box_width,self.box_height),
            text = "Loan (taken)",
            manager = self.manager,
            container = self.loan_panel_taken,
            )
        self.UIobjects.append(self.namelabel_2)

        # Changing offered interest rate is displayed during "Loan (offered)" status
        self.offered_ir_box = UITextBox(
            html_text = "Interest rate: "+f"{self.loan_reference.get_offered_interest_rate():.2f}", # refers to instance of Background_Loan
            relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.loan_panel_offered,
        )            
        self.UIobjects.append(self.offered_ir_box)          

        # Max borrowable is displayed during "Loan (offered)" status
        self.max_amount_box = UITextBox(
            html_text = "Max amount: "+str(self.get_max_amount()),
            relative_rect = pygame.Rect(self.box_width/2,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.loan_panel_offered,
        )            
        self.UIobjects.append(self.max_amount_box)

        # h button to display historical Information_Popup of generated loan interest rates, for "Loan (offered)" status
        self.graph_button_1 = UIButton(
            relative_rect = pygame.Rect((self.box_height*0.9)+5,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "h",
            manager = manager,
            starting_height = 2,
            container = self.loan_panel_offered,
            tool_tip_text = "Display historical information about the loan"
        )      
        self.UIobjects.append(self.graph_button_1)

        # h button to display historical Information_Popup of generated loan interest rates, for "Loan (taken)" status
        # buttons functionally identical in either state
        self.graph_button_2 = UIButton(
            relative_rect = pygame.Rect((self.box_height*0.9)+5,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "h",
            manager = manager,
            starting_height = 2,
            container = self.loan_panel_taken,
            tool_tip_text = "Display a graph with historical information about the loan"
        )     
        self.UIobjects.append(self.graph_button_2)

        # i button to display informational textbox about loans, for "Loan (offered)" status
        self.information_button_1 = UIButton(
            relative_rect = pygame.Rect(self.box_height*0.1,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "i",
            manager = manager,
            starting_height = 2,
            container = self.loan_panel_offered,
            tool_tip_text = "Display information about loans"
        ) 
        self.UIobjects.append(self.information_button_1)  

        # i button to display informational textbox about loans, for "Loan (taken)" status      
        # buttons functionally identical in either state  
        self.information_button_2 = UIButton(
            relative_rect = pygame.Rect(self.box_height*0.1,self.box_height*0.1,self.box_height*0.8,self.box_height*0.8),
            text = "i",
            manager = manager,
            starting_height = 2,
            container = self.loan_panel_taken,
            tool_tip_text = "Display information about loans"
        )   
        self.UIobjects.append(self.information_button_2)

        # take loan button, for "Loan (offered)" status. Is not enabled until a valid input has been selected
        self.take_loan_button = UIButton(
            relative_rect=pygame.Rect(
                0, self.box_height * 2, self.box_width / 4, self.box_height
            ),
            text="Take loan",
            manager=manager,
            container=self.loan_panel_offered,
            tool_tip_text="Take out a loan with the offered interest rate",
        )
        self.take_loan_button.disable()
        self.UIobjects.append(self.take_loan_button)

        # pay loan button, for "Loan (taken)" status. Is not enabled until a valid input has been selected
        self.pay_loan_button = UIButton(
            relative_rect = pygame.Rect(0, self.box_height * 2, self.box_width / 4, self.box_height),
            text = "Pay back",
            manager = manager,
            container = self.loan_panel_taken,
            tool_tip_text = "Pay off a portion of the taken loan",
        )        
        self.pay_loan_button.disable()
        self.UIobjects.append(self.pay_loan_button)

        # select button for "Loan (offered)" status. 
        self.select_loan_button = UIButton(
            relative_rect = pygame.Rect(15/24 * self.box_width, self.box_height * 2, self.box_width / 6, self.box_height),
            text = "Select",
            manager = manager,
            container = self.loan_panel_offered,
            tool_tip_text = "Select the amount you will take a loan out for",
        )        
        self.select_loan_button.disable()
        self.UIobjects.append(self.select_loan_button)

        # select button for "Loan (taken)" status
        self.select_pay_button = UIButton(
            relative_rect = pygame.Rect(15/24 * self.box_width, self.box_height * 2, self.box_width / 6, self.box_height),
            text = "Select",
            manager = manager,
            container = self.loan_panel_taken,
            tool_tip_text = "Select the amount that you will pay back",
        )             
        self.select_pay_button.disable()
        self.UIobjects.append(self.select_pay_button)

        # Number entry form for "Loan (offered)" status, where user types desired loan amount to take before clicking "Select" button
        # Will be autofilled and autoselected with max borrowable loan when "Max" button is clicked 
        self.take_loan_entry = UINumberEntryLine(
            relative_rect = pygame.Rect(self.box_width/4, self.box_height * 2, 9*self.box_width / 24, self.box_height),
            manager = manager,
            container = self.loan_panel_offered,
        )
        self.take_loan_entry.set_text("[Click to Enter]")   
        self.take_loan_entry.set_select_reference(self.select_loan_button)
        self.UIobjects.append(self.take_loan_entry)

        # Number entry form for "Loan (taken)" status, where user types desired loan amount to pay back before clicking "Select" button
        # Will be autofilled and autoselected with max that can be paid back when "Max" button is clicked 
        self.pay_loan_entry = UINumberEntryLine(
            relative_rect = pygame.Rect(self.box_width/4, self.box_height * 2, 9*self.box_width / 24, self.box_height),
            manager = manager,
            container = self.loan_panel_taken,
        )
        self.pay_loan_entry.set_text("[Click to Enter]")
        self.pay_loan_entry.set_select_reference(self.select_pay_button)
        self.UIobjects.append(self.pay_loan_entry)

        # "Max" button for "Loan (offered)" status
        self.take_max_loan_button = UIButton(
            relative_rect=pygame.Rect(
                19 / 24 * self.box_width,
                self.box_height * 2,
                self.box_width / 7,
                self.box_height,
            ),
            text="Max",
            manager=manager,
            container=self.loan_panel_offered,
            tool_tip_text="Select the maximum amount you can take a loan out for",
        )
        self.UIobjects.append(self.take_max_loan_button)

        # "Max" button for "Loan (taken)" status
        self.pay_max_loan_button = UIButton(
            relative_rect=pygame.Rect(
                19 / 24 * self.box_width,
                self.box_height * 2,
                self.box_width / 7,
                self.box_height,
            ),
            text="Max",
            manager=manager,
            container=self.loan_panel_taken,
            tool_tip_text="Select the maximum amount you can back your loan with",
        )
        self.UIobjects.append(self.pay_max_loan_button)
        self.update_boxes()

    def update_boxes(self) -> None:
        # Updates display of all UI elements at UI event triggers

        # Scrollbar update
        if self.timeline_reference.timeline_panel.vert_scroll_bar != None:
            for object in self.UIobjects:
                self.timeline_reference.timeline_panel.vert_scroll_bar.join_focus_sets(object)

        # Toggling between "Loan (offered)" and 
        if self.timeline_reference.is_active:
            if self.have_loan():
                self.loan_panel_offered.hide()
                self.loan_panel_taken.show()
            else:
                self.loan_panel_offered.show()
                self.loan_panel_taken.hide()

        # input limit changes dynamically according to the length of the current max input value, but not below 16 so the "click to enter" message can be displayed
        self.take_loan_entry.set_text_length_limit(max(len(str(self.get_max_amount())),16))
        self.pay_loan_entry.set_text_length_limit(max(len(str(self.get_amount_owed())),16))

        # Update text of all relevant fields of Loan section
        try:
            self.taken_ir_box.kill()
            self.amount_owed_box.kill()
            self.max_amount_box.kill()
        except:
            pass
        finally:
            # update interest rate
            if self.have_loan():
                self.taken_ir_box = UITextBox(
                    html_text = "Interest rate: "+f"{self.interest_at_borrowing:.2f}",
                    relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
                    manager = self.manager,
                    container = self.loan_panel_taken,
                ) 
                if self.timeline_reference.timeline_panel.vert_scroll_bar != None:
                    self.timeline_reference.timeline_panel.vert_scroll_bar.join_focus_sets(self.taken_ir_box)

            # update current debt
            self.amount_owed_box = UITextBox(
                html_text = "Current debt: "+str(self.get_amount_owed()),
                relative_rect = pygame.Rect(self.box_width/2,self.box_height,self.box_width/2,self.box_height),
                manager = self.manager,
                container = self.loan_panel_taken,
            ) 

            # update max borrowable   
            self.max_amount_box = UITextBox(
                html_text = "Max amount: "+str(self.get_max_amount()),
                relative_rect = pygame.Rect(self.box_width/2,self.box_height,self.box_width/2,self.box_height),
                manager = self.manager,
                container = self.loan_panel_offered,
            )   
            if self.timeline_reference.timeline_panel.vert_scroll_bar != None:
                self.timeline_reference.timeline_panel.vert_scroll_bar.join_focus_sets(self.amount_owed_box)                  

    def progress_time(self) -> None:
        # Progresses time by updating all GUI boxes and offered interest rate display
        self.update_boxes()
        try:
            self.offered_ir_box.kill()
        except:
            pass
        finally:
            self.offered_ir_box = UITextBox(
            html_text = "Interest rate: "+f"{self.loan_reference.get_offered_interest_rate():.2f}",
            relative_rect = pygame.Rect(0,self.box_height,self.box_width/2,self.box_height),
            manager = self.manager,
            container = self.loan_panel_offered,
            )           
    
    def get_max_amount(self) -> int:
        # returns max borrowable. Get max_amount_multiplier from loan_reference and multiplies it with net_worth of timeline_reference
        return int(
            self.timeline_reference.get_net_worth()
            * self.loan_reference.get_max_amount_multiplier()
        )

    def progress_amount_owed(self) -> None:
        # updates amount_owed by multiplying it with (1 + (interest rate a borrowing))
        # formula for fixed interest rate loan. Rounded up to maintain integer amount_owed AND ensures that every taken loan accrues interest even if interest is miniscule
        if self.interest_at_borrowing != None:
            self.amount_owed = int(
                self.amount_owed * (1 + self.interest_at_borrowing / 100) + 1
            )  # +1 for round up

    def take_loan(self, amount: int) -> None:
        # updates amount_owed to amount argument, loan cannot be taken with an existing loan
        self.amount_owed = amount
        # fixes interest to interest rate at borrowing
        self.interest_at_borrowing = self.loan_reference.get_offered_interest_rate()

    def get_loan_reference(self) -> Background_Loan:
        return self.loan_reference

    def pay_off(self, amount: int) -> None:
        # decreases amount_owed by amount argument. 
        # If amount_owed is zero, resets interest_at_borrowing to None.
        self.amount_owed -= amount
        if self.amount_owed == 0:
            self.interest_at_borrowing = None

    def get_amount_owed(self) -> int:
        return self.amount_owed

    def have_loan(self) -> bool:
        # returns True is loan has been taken i.e. amount_owed > 0
        return self.amount_owed > 0

    def display_graph(self) -> None:
        # displays information popup of historical loan interest rates. Uses implemented Information_Popup class
        try:
            self.info_popup.kill()
        except:
            pass
        finally:
            self.info_popup = Information_Popup(
                "Historical Loan Interest Rates",
                self.loan_reference.get_historical_interest_rates(),
                self.loan_reference.get_initial_number_of_historical_interest_rates(),
                self.timestep,
                "interest rate",
                self.manager,
            )
            self.info_popup.display_graph()

    def button_pressed(self, event) -> bool:
        # iterates through all loan buttons to see which, if any, have been clicked and calls corresponding methods
        # returns True if it's a button in this Timeline_Loan to prevent iteration through other buttons, False otherwise

        # upon "h" or "i" click displays historical or information graph
        if event.ui_element == self.graph_button_1:
            self.display_graph()
        elif event.ui_element == self.graph_button_2:
            self.display_graph()
        elif event.ui_element == self.information_button_1:
            self.display_info()
        elif event.ui_element == self.information_button_2:
            self.display_info()

        # upon "Max" click during "Loan (offered)" status, autofills text entry form with max borrowable and selects
        elif event.ui_element == self.take_max_loan_button:
            self.take_loan_entry.set_text(str(self.get_max_amount()))
            self.current_amount = self.get_max_amount()
            self.take_loan_button.enable()

        # upon "Max" click during "Loan (taken)" status, autofills text entry form with max payable and selects
        elif event.ui_element == self.pay_max_loan_button:
            self.current_amount = min(self.get_amount_owed(), self.timeline_reference.get_money())
            self.pay_loan_entry.set_text(str(self.current_amount))
            self.pay_loan_button.enable()

        # upon "Select" click during "Loan (offered)" status, input amount is set and "Take loan" button is enabled 
        elif event.ui_element == self.select_loan_button:
            input = self.take_loan_entry.get_text()
            if input == "":
                proposed_amount = 0
            else:
                proposed_amount = int(self.take_loan_entry.get_text())

            if (
                proposed_amount > self.get_max_amount()
            ):  # if the user inputs too large of a loan proposal, it defaults to max
                self.take_loan_entry.set_text(str(self.get_max_amount()))
                self.current_amount = self.get_max_amount()
                self.take_loan_button.enable()

            elif proposed_amount > 0:
                self.take_loan_entry.set_text(str(proposed_amount))
                self.current_amount = proposed_amount
                self.take_loan_button.enable()
    
            else:
                self.take_loan_button.disable()

        # upon "Take loan" click during "Loan (offered)" status, Loan section is changed to "Loan (taken)" status
        elif event.ui_element == self.take_loan_button:
            self.timeline_reference.take_loan(self.current_amount)
            self.current_amount = None
            self.pay_loan_button.disable()
            if self.pay_loan_entry.get_text() != "[Click to Enter]":
                self.pay_loan_entry.set_text("")

        # upon "Select" click during "Loan (taken)" status, input amount is set and "Pay back" button is enabled 
        elif event.ui_element == self.select_pay_button:
            input = self.pay_loan_entry.get_text()
            if input == "":
                proposed_amount = 0
            else:
                proposed_amount = int(self.pay_loan_entry.get_text())

            if proposed_amount > self.get_amount_owed():
                self.current_amount = min(self.get_amount_owed(), self.timeline_reference.get_money())
                self.pay_loan_entry.set_text(str(self.current_amount))
                self.pay_loan_button.enable()
            
            elif proposed_amount > 0:
                self.current_amount = min(proposed_amount, self.timeline_reference.get_money())
                self.pay_loan_entry.set_text(str(self.current_amount))
                self.pay_loan_button.enable()

            else:
                self.pay_loan_button.disable()

        # upon "Pay back" click during "Loan (taken)" status, Loan section is changed to "Loan (offered)" status
        elif event.ui_element == self.pay_loan_button:
            self.timeline_reference.pay_loan(self.current_amount)
            self.current_amount = None
            self.take_loan_button.disable()
            self.pay_loan_button.disable()

        else:
            return False
        return True

    def update_attributes(self, new_loan: any) -> None:
        # copies attributes of argument Timeline_Loan into this Timeline_Loan, used during a timeline split or merge to ensure proper copying of information
        self.amount_owed = new_loan.amount_owed
        self.interest_at_borrowing = new_loan.interest_at_borrowing
        self.update_boxes()
        self.pay_loan_button.disable()
        self.take_loan_button.disable()
        self.pay_loan_entry.set_text("")
        self.take_loan_entry.set_text("")

   
    def display_info(self) -> None:
        # when i button clicked, displays general information about loans
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