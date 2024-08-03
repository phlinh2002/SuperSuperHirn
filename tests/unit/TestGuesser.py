import unittest
from model.Guesser import Guesser, Code

class TestGuesser(unittest.TestCase):

    def setUp(self):
        Code.code_length = 4  # code length.
        Code.n_color = 6      # number of colors.
        self.guesser = Guesser()

    def test_generate_all_possible_codes(self):
        expected_length = Code.n_color ** Code.code_length
        self.assertEqual(len(self.guesser.generate_all_possible_codes()), expected_length)

    def test_reset_code(self):
        self.guesser._code.set_code("1234", 1, Code.n_color)
        self.guesser.reset_code()
        self.assertEqual(self.guesser.get_code(), "")

    def test_simulate_feedback(self):
        feedback = self.guesser.simulate_feedback("1234", "1234")
        self.assertEqual(feedback, "8888")

        feedback = self.guesser.simulate_feedback("1234", "4321")
        self.assertEqual(feedback, "7777")

    def test_parse_feedback(self):
        black, white = self.guesser.parse_feedback("8877")
        self.assertEqual(black, 2)
        self.assertEqual(white, 2)

    def test_automated_guess(self):
        first_guess = self.guesser.automated_guess(None)
        self.assertEqual(len(first_guess), Code.code_length)
        self.assertTrue(all(char.isdigit() and 1 <= int(char) <= Code.n_color for char in first_guess))


if __name__ == '__main__':
    unittest.main()
