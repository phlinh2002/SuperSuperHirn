from enum import Enum
from colorama import init, Back, Style, Fore

init(autoreset=True)



class Color(Enum):
    ROT = 1
    GRUEN = 2
    GELB = 3
    BLAU = 4
    ORANGE = 5
    BRAUN = 6
    WEISS = 7
    SCHWARZ = 8

    def colored_background(self):
        color_backgrounds = {
            Color.ROT: Fore.RED,
            Color.GRUEN: Fore.GREEN,
            Color.GELB: Fore.LIGHTYELLOW_EX,
            Color.BLAU: Fore.BLUE,
            Color.ORANGE: Fore.LIGHTRED_EX,  # Magenta as closest to orange
            Color.BRAUN: Fore.YELLOW,    # Yellow/Brown, as there's no direct brown
            Color.WEISS: Fore.WHITE,
            Color.SCHWARZ: Fore.BLACK,
        }
        return color_backgrounds[self]



class Code:
    code_length = 0
    # Anzahl der zur Verfügung stehenden Farben
    n_color = 0

    # Initialisiert mit einer leeren Liste
    def __init__(self):
        self.code = []

    # setze den uebergebenen Code (string) in der variable self.code
    # Hier wird schon alles geprueft: ob der Code die Laenge und die Anzahl der zur Verfügung stehenden Color respektiert
    def set_code(self, code_input, lower_bound, upper_bound):
        if len(code_input) == Code.code_length and code_input.isdigit():
            for j in code_input:
                if int(j) not in range(lower_bound, upper_bound + 1):
                    print(
                        f"Ungültige Eingabe,  der Farbcode muss nur Zahlen aus {lower_bound} bis {upper_bound} beinhalten")
                    break
                else:
                    self.code.append(int(j))
        else:
            print(
                f"Ungültige Eingabe, die Länge des Farbcodes muss aus {Code.code_length} Stellen und nur aus Nummern bestehen!")

    # Die Funktion gibt den Farbcode als Liste zurueck
    def get_code(self):
        return self.code

    # Statische Funktion, um die Laenge des Farbcodes festzulegen
    @staticmethod
    def set_code_length(length):
        Code.code_length = length

    # Statische Funktion, um die Anzahl der zu nutzenden Color festzulegen
    @staticmethod
    def set_n_color(n_color):
        Code.n_color = n_color


