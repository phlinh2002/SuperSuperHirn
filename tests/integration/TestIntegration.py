import responses
from controller.Game import Game
from model.CoderClient import CoderLocalClient
from model.Guesser import Guesser
from view.UI import ConsoleUI
from model.Color import Code
from model.Board import Board

# test game, ui interaction
def test_game_ui_interaction():
    game = Game()
    game._ui = ConsoleUI()
    game._ui.code_length = 4
    game._ui.n_color = 6
    game._ui.role = 1
    game._ui.coder_mode = 2

    game._set_up()
    assert game._role == 1
    assert len(game._board.guess_list) == 0
    assert game._coder is not None


# test communication with network-coder
@responses.activate
def test_network_game_communication():
    # gemockter POST-Requests
    responses.add(responses.POST, 'http://localhost:3010',
                  json={'value': '78'}, status=200)

    game = Game()
    game._ui = ConsoleUI()
    game._ui.code_length = 4
    game._ui.n_color = 6
    game._ui.role = 1
    game._ui.coder_mode = 1

    game._set_up()
    guess = "1212"
    feedback = game._coder.get_feedback(guess)
    # Überprüft, ob die URL des CoderNetworkClient korrekt gesetzt ist.
    assert game._coder._server_URL == "http://localhost:3010"
    assert feedback == '78'


# test board, local-coder interaction
def test_board_update_with_feedback():
    Code.set_code_length(4)
    Code.set_n_color(6)

    board = Board()
    coder = CoderLocalClient()
    coder.set_secret_code()

    guess = "1111"
    feedback = coder.get_feedback(guess)

    board.update_guess_list(guess)
    board.update_feedback_list(feedback)

    assert board.guess_list[-1] == guess
    assert board.feedback_list[-1] == feedback


# test board, guesser interaction
def test_guesser_board_interaction():
    Code.set_code_length(4)
    Code.set_n_color(6)

    guesser = Guesser()
    board = Board()
    coder = CoderLocalClient()
    coder.set_secret_code()

    guess = guesser.automated_guess(coder)
    feedback = coder.get_feedback(guess)

    board.update_guess_list(guess)
    board.update_feedback_list(feedback)

    assert board.guess_list[-1] == guess
    assert board.feedback_list[-1] == feedback
