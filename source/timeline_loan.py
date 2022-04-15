from background_loan import Background_Loan
from information_popup import Information_Popup
from pygame_gui import UIManager

class Timeline_Loan:
    def __init__(
        self,
        # id: int,
        # amount_owed: int,
        # interest_at_borrowing: int,
        loan_reference: Background_Loan,
    ) -> None:
        # self.id = id
        self.amount_owed = 0
        self.interest_at_borrowing = None
        self.loan_reference = loan_reference

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

    def display_info(self, manager: UIManager) -> None:
        info_popup = Information_Popup("Historical Loan Interest Rates", self.loan_reference.get_historical_prices(), manager)
        info_popup.display_graph()

    def button_pressed(self, event) -> bool:
        pass
