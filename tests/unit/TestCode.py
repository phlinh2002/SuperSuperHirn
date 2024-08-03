import unittest

from model.Color import Code


class TestCode(unittest.TestCase):
    def setUp(self):
        self._code_instance = Code()
        Code.set_code_length(4)
        Code.set_n_color(8)

    def test_set_code_valid_input(self):
        self._code_instance.set_code('1234', 1, Code.n_color)
        expected_code = [1, 2, 3, 4]
        self.assertEqual(self._code_instance.get_code(), expected_code)
    def test_set_code_length(self):
        Code.set_code_length(5)
        self.assertEqual(self._code_instance.code_length, 5)

    def test_set_number_color(self):
        Code.set_n_color(8)
        self.assertEqual(self._code_instance.n_color, 8)

    def test_set_code_invalid_input(self):
        self._code_instance.set_code('invalid_input', 1, Code.n_color)
        self.assertEqual(self._code_instance.get_code(), [])



