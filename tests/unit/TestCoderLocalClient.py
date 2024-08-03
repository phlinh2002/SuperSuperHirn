import unittest
from unittest.mock import MagicMock, patch
from model.CoderClient import CoderLocalClient, CoderNetworkClient

class TestCoderLocalClient(unittest.TestCase):
    # Set up before each test
    def setUp(self):
        self.coder = CoderLocalClient()
        self.coder._code_length = 4  # code length of 4
        self.coder._n_color = 6      # 6 possible colors

    def test_set_secret_code(self):
        # Test if secret code is set correctly
        self.coder.set_secret_code()
        self.assertEqual(len(self.coder._secret_code), self.coder._code_length)
        # Verify that each color in the secret code is within the allowed range
        all_in_range = all(1 <= color <= self.coder._n_color for color in self.coder._secret_code)
        self.assertTrue(all_in_range)

    def test_get_feedback_correct_guess(self):
        # Test feedback for a correct guess
        self.coder._secret_code = [1, 2, 3, 4]  # Example secret code
        guess = "1234"  # Matching guess
        feedback = self.coder.get_feedback(guess)
        self.assertEqual(feedback, "8888")  # Feedback indicating correct guess

    def test_get_feedback_incorrect_guess(self):
        # Test feedback for an incorrect guess
        self.coder._secret_code = [1, 2, 3, 4]
        guess = "4321"  # Incorrect guess
        feedback = self.coder.get_feedback(guess)
        self.assertEqual(feedback, "7777")  # Feedback indicating correct colors but wrong positions

class TestCoderNetworkClient(unittest.TestCase):
    def setUp(self):
        self.coder = CoderNetworkClient("localhost", 8000)

    @patch('model.CoderClient.requests.post')
    def test_set_secret_code(self, mock_post):
        # Mock the POST request response for setting the secret code
        mock_response = MagicMock(status_code=200, json=lambda: {"gameid": 123})
        mock_post.return_value = mock_response

        self.coder.set_secret_code()
        self.assertEqual(self.coder._gameID, 123)

    @patch('model.CoderClient.requests.post')
    def test_get_feedback(self, mock_post):
        # Mock the POST request response for getting feedback
        mock_feedback = "feedback"
        mock_response = MagicMock(status_code=200, json=lambda: {"value": mock_feedback})
        mock_post.return_value = mock_response

        feedback = self.coder.get_feedback("1234")
        self.assertEqual(feedback, mock_feedback)

if __name__ == '__main__':
    unittest.main()
