import unittest
from unittest.mock import patch

from view.UI import ConsoleUI


class TestUI(unittest.TestCase):
    def setUp(self):
        self._ui = ConsoleUI()

    @patch('builtins.input', return_value='10')
    def test_age_allowed_valid_age(self, mock_input):
        self.assertTrue(self._ui.age_allowed())

    @patch('builtins.input', return_value='2')
    def test_age_allowed_invalid_age(self, mock_input):
        self.assertFalse(self._ui.age_allowed())

    @patch('builtins.input', side_effect=['not a number', '15'])
    def test_age_allowed_non_numeric_input(self, mock_input):
        # Test with a non-numeric input followed by a valid input
        self.assertTrue(self._ui.age_allowed())
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input', return_value='99')
    def test_age_allowed_edge_case_age(self, mock_input):
        # Test an edge case (high age value)
        self.assertTrue(self._ui.age_allowed())
        mock_input.assert_called_once_with('Geben Sie bitte Ihr Alter ein: ')
