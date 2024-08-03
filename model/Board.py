
class Board:

    def __init__(self):
        self.guess_list = []
        self.feedback_list = []

    def update_guess_list(self, code):
        self.guess_list.append(code)

    def update_feedback_list(self, code):
        self.feedback_list.append(code)

    def clear_board(self):
        self.guess_list = []
        self.feedback_list = []
