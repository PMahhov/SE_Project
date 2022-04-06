from background_loan import Background_Loan
from information_popup import Information_Popup


class Timeline_Loan:
    def __init__(
        self,
        id: int,
        amount_owed: int,
        interest_at_borrowing: int,
        loan_reference: Background_Loan,
    ) -> None:
        self.id = id
        self.amount_owed = amount_owed
        self.interest_at_borrowing = interest_at_borrowing
        self.loan_reference = loan_reference

    def progress_amount_owed(self) -> int:
        pass

    def display_info(self) -> Information_Popup:
        pass
