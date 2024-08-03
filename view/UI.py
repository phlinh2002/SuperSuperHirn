import time
from model.Color import Color
from abc import ABC, abstractmethod
from colorama import init, Back, Style
init(autoreset=True)



class UI(ABC):
    def __init__(self):
        self.code_length = 0
        self.role = None
        self.n_color = 0
        self.coder_mode = None
        self.gamerID = ""

    @abstractmethod
    def start_game_print(self):
        pass

    @abstractmethod
    def print_colorlist(self):
        pass

    @abstractmethod
    def print_board(self, guess_list, feedback_list):
        pass

    @abstractmethod
    def result(self, win):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def age_allowed(self):
        pass



class ConsoleUI(UI):

    def start_game_print(self):

        while self.role not in [1, 2]:
            try:
                self.role = int(input(
                    "Möchten Sie als Rater(1) oder Kodierer(2) spielen? \nBitte geben Sie nur 1 (als Rater) oder 2 (als Kodierer) ein: "))
                if (self.role == 1):
                    print("Sie spielen als Rater!")
                    while self.coder_mode not in [1, 2]:
                        try:
                            self.coder_mode = int(input(
                                "Möchten Sie mit einem online- oder offline-Kodierer spielen (1 für online, 2 für offline)?"))
                            if self.coder_mode == 1:
                                self.gamerID = input("Geben Sie bitte Ihr Name ein: ")
                        except ValueError:
                            print("Bitte geben Sie nur 1 oder 2 ein!")
                elif (self.role == 2):
                    self.coder_mode = 2
                    print("Sie spielen als Kodierer!")
                print("------------------------------------------------------------------------")
            except ValueError:
                print("Bitte geben Sie nur 1 oder 2 ein!")

        while self.code_length not in [4, 5]:
            try:
                self.code_length = int(input("Mit welcher Codelänge möchten Sie spielen (nur 4 oder 5)?\n"
                                             "Geben Sie bitte nur 4 oder 5 ein "))
            except ValueError:
                print("Bitte geben Sie nur 4 oder 5 als Nummer ein!\n")

        farbcodierung = "\nFarbkodierung:\n"
        for i in range(1, len(list(Color)) + 1):
            farbcodierung += f"{i}. {Color(i).name}   "
        print(farbcodierung)
        print()

        while not 2 <= self.n_color <= 8:
            try:
                self.n_color = int(input("Mit wie viele Farben möchten Sie spielen?"
                                         "\n Wählen Sie eine Zahl zwischen 2 und 8: "))
            except ValueError:
                print("Bitte geben Sie nur Nummer ein!\n")

        self.print_colorlist()
        print("\t \t \tBoard")

        column_width = 3

        # Header
        header = f"{'Versuch':<{column_width}}"
        header += f"{'Rate':^{self.code_length * column_width}}"
        header += f"\t{'Auswertung':^{self.code_length * column_width}}"

        border_top = '-' * (len(header) + self.code_length)

        print(border_top)
        print(header)
        print(border_top)

        for i in range(11):
            if i != 0:
                try_left = str(i)
                rate_part = 'X' * self.code_length

                feedback_part = '_' * self.code_length

                formatted_line = f"| {try_left:<{column_width}}"
                formatted_line += f"| {rate_part:^{self.code_length * column_width}}"
                formatted_line += f"| {feedback_part:^{self.code_length * column_width}} |"

                print(formatted_line)
        print(border_top + "\n")

    def print_colorlist(self):
        print()
        for i in range(1, self.n_color + 1):
            color = Color(i)
            print(f"{color.colored_background()} {color.name} {Style.RESET_ALL}", end=' | ')
        print("\n")

    def print_colorlist(self):
        print()
        a = ""
        for i in range(self.n_color):
            a += str(Color(i + 1).value) + ". " + Color(i + 1).name + " | "
        print(str((int(len(a) / 2) - 3) * '-') + "Farbe" + str((int(len(a) / 2) - 3) * '-'))
        print(a + "\n")

    def print_board(self, guess_list, feedback_list):
        self.print_colorlist()

        print("\t \t \tBoard")

        column_width = 3

        # Header
        header = f"{'Versuch':<{column_width}}"
        header += f"{'Rate':^{self.code_length * column_width}}"
        header += f"\t{'Auswertung':^{self.code_length * column_width}}"

        border_top = '-' * (len(header) + self.code_length - 1)

        print(border_top)
        print(header)
        print(border_top)

        for i in range(11):
            if i != 0:
                while not len(guess_list) == len(feedback_list):
                    time.sleep(1)
                if (i - 1) < len(guess_list):
                    rate_part = guess_list[i - 1]
                    feedback_part = feedback_list[i - 1]
                else:
                    rate_part = 'X' * self.code_length
                    feedback_part = '_' * self.code_length

                versuch = i
                formatted_line = f"| {versuch:<{column_width}}"

                for num in rate_part:
                    if num.isdigit():
                        color = Color(int(num))
                        formatted_line += f"{color.colored_background()} {num} {Style.RESET_ALL}"
                    else:
                        formatted_line += f" {num} "
                formatted_line += f""
                formatted_line += f"| {feedback_part:^{self.code_length * column_width}} |"

                print(formatted_line)
        print(border_top + "\n")



    def result(self, win):
        if (win):
            print("Sie haben gewonnen!")
        else:
            print("Sie haben verloren!")

    def reset(self):
        self.code_length = 0
        self.role = None
        self.n_color = 0
        self.coder_mode = None

    def age_allowed(self):
        while True:
            try:
                age = int(input("Geben Sie bitte Ihr Alter ein: "))
                if (age < 6):
                    print("Du bist noch nicht erlaubt zu spielen!")
                    return False
                else:
                    return True

            except ValueError:
                print("Bitte geben Sie nur Zahlen ein!")
