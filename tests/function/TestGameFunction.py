import unittest
from unittest import mock
from unittest.mock import patch

from controller.Game import Game
from model.Color import Code
from model.Guesser import Guesser
from model.CoderClient import CoderLocalClient


class TestGameFunction(unittest.TestCase):
    def setUp(self):
        self._guesser = Guesser()
        self._code = Code()
        self._coder = CoderLocalClient()
        self._code.set_code_length(4)
        self._code.set_n_color(5)
        self._coder._code_length = 4
        self._coder._n_color = 5

    @mock.patch('builtins.input', side_effect=['1234', '1234'])
    def test_getfeedback1(self, mock_input):
        self._coder.set_secret_code_manually()
        self._guesser.make_guess()
        guess = self._guesser.get_code()
        self.assertEqual("8888", self._coder.get_feedback(guess))

    @mock.patch('builtins.input', side_effect=['1234', '1121'])
    def test_getfeedback2(self, mock_input1):
        self._coder.set_secret_code_manually()
        self._guesser.make_guess()
        guess = self._guesser.get_code()
        self.assertEqual("87", self._coder.get_feedback(guess))

    @mock.patch('builtins.input', return_value='1234')
    def test_reset_code(self, mock_input):
        self._guesser.make_guess()
        self._guesser.reset_code()
        self.assertEqual("", self._guesser.get_code())


if __name__ == '__main__':
    unittest.main()
