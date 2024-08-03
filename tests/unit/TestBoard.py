import unittest

from model.Board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self._board = Board()

    def test_update_guess_list(self):
        self._board.update_guess_list('1234')
        self.assertEqual(self._board.guess_list, ['1234'])

    def test_update_feedback_list(self):
        self._board.update_feedback_list('8888')
        self.assertEqual(self._board.feedback_list, ['8888'])

    def test_update_clear_board(self):
        self._board.update_guess_list(['5678', '1111'])
        self._board.update_feedback_list('8888')
        self._board.clear_board()
        self.assertEqual(self._board.guess_list, [])
        self.assertEqual(self._board.feedback_list, [])