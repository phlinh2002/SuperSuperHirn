from view.UI import ConsoleUI
from model.Board import Board
from model.CoderClient import CoderLocalClient, CoderNetworkClient, CoderClientFactory
from model.Guesser import Guesser
from model.Color import Code


class Game:

    MAX_TRIES = 10
    def __init__(self):
        self._code_length = None
        self._n_color = None
        self._role = None  # 1 = Guesser, 2 = Coder
        self._ui = ConsoleUI()
        self._board = None
        self._guesser = None
        self._coder = None
        self._guesser_has_won = False
        self._coder_mode = None  # 1 = Network Coder, 2 = Local Coder
        self._network_coder_ip = "localhost"
        self._network_coder_port = 3000

    def _set_up(self):
        Code.set_code_length(self._ui.code_length)
        Code.set_n_color(self._ui.n_color)
        self._role = self._ui.role
        self._board = Board()
        self._guesser = Guesser()
        self._coder_mode = self._ui.coder_mode
        self._coder = CoderClientFactory.create(self._coder_mode, self._network_coder_ip, self._network_coder_port)
        self._coder.gamerID = self._ui.gamerID

    # Kann das Game starten oder beenden
    def _start_game(self):
        if not self._ui.age_allowed():
            return
        self._ui.start_game_print()
        self._set_up()
        if self._role == 1:
            self._play_as_guesser()
            if not self._guesser_has_won:
                print(f"Der zu erratende Geheimcode war: {self._coder.get_secret_code()}")
            self._close(self._guesser_has_won)
        else:
            self._coder = CoderLocalClient()
            self._play_as_coder()
            if self._guesser_has_won:
                print("Der Rater hat deinen Code richtig erraten!")
            self._close(not self._guesser_has_won)

    def _play_as_guesser(self):
        self._coder.set_secret_code()
        while not self._end_game():
            self._guesser.make_guess()
            guess = self._guesser.get_code()
            self._board.update_guess_list(guess)
            feedback = self._coder.get_feedback(guess)
            self._board.update_feedback_list(feedback)
            self._ui.print_board(self._board.guess_list, self._board.feedback_list)
            if feedback == "8" * Code.code_length:
                self._guesser_has_won = True
            else:
                self._guesser.reset_code()

    def _play_as_coder(self):
        self._coder.set_secret_code_manually()
        for _ in range(Game.MAX_TRIES):
            guess = self._guesser.automated_guess(self._coder)
            self._board.update_guess_list(guess)

            print(f"Geheimer Farbcode: {self._coder.get_secret_code()}")

            # Prompt the user (coder) to enter the feedback manually
            feedback = input(f"Geben Sie bitte die Feedback ein {guess}: ")


            self._board.update_feedback_list(feedback)
            self._ui.print_board(self._board.guess_list, self._board.feedback_list)

            # Check if the Guesser (system) has correctly guessed the code
            if feedback == "8" * Code.code_length:
                self._guesser_has_won = True
                break

        # If the loop completes, the Guesser did not guess correctly within the maximum tries
        if not self._guesser_has_won:
            self._guesser_has_won = False

    def _end_game(self):
        if self._guesser_has_won:
            return True
        if len(self._board.feedback_list) == Game.MAX_TRIES:
            self._guesser_has_won = False

            return True
        else:
            return False

    def _close(self, result):
        self._ui.result(result)
        print()
        var = int(input("Wollen Sie eine neue Runde spielen ?\nTippen Sie (1) fuer 'Ja' oder (2) fuer 'Nein'"))
        if var == 1:
            self._ui.reset()
            self._guesser_has_won = False
            self._start_game()
        else:
            print("Spiel beendet!")
            return

if __name__ == '__main__':
    ssh = Game()
    ssh._start_game()
