import itertools
import random
from model.Color import Code


class Guesser:
    def __init__(self):
        # Initialize the Guesser with a code, list of all possible guesses, and a flag for the initial guess.
        self._code = Code()
        self.possible_guesses = self.generate_all_possible_codes()
        self.knuth_set = self.possible_guesses.copy()  # A set for Knuth's algorithm
        self.initial_guess = True  # Flag to indicate the first guess

    def make_guess(self):
        # Allows a user to make a guess until the guess length matches the code length.
        while len(self._code.get_code()) != Code.code_length:
            code_input = input("\nVersuchen Sie den Farbcode zu raten: ")
            self._code.set_code(code_input, 1, Code.n_color)

    def get_code(self):
        # Returns the current code as a string.
        return "".join(str(element) for element in self._code.get_code())

    def reset_code(self):
        self._code.code = []

    def generate_all_possible_codes(self):
        return [''.join(map(str, code)) for code in
                itertools.product(range(1, Code.n_color + 1), repeat=Code.code_length)]

    def automated_guess(self, coder):
        # Generates all possible codes using a Cartesian product.
        if self.initial_guess:
            guess = ''.join(str(random.randint(1, Code.n_color)) for _ in range(Code.code_length))
            self.initial_guess = False
        else:
            last_guess = self.get_code()
            last_feedback = coder.get_feedback(last_guess)
            self.narrow_down_possibilities(last_guess, last_feedback)
            guess = self.choose_next_guess()

        # Reset the code before setting a new guess
        self.reset_code()
        self._code.set_code(guess, 1, Code.n_color)
        return guess

    def narrow_down_possibilities(self, last_guess, last_feedback):
        # Reduces the set of possible guesses based on the feedback from the last guess.
        self.possible_guesses = [
            guess for guess in self.possible_guesses
            if self.simulate_feedback(guess, last_guess) == last_feedback
        ]
        self.knuth_set = self.possible_guesses.copy()

    def choose_next_guess(self):
        # Chooses the next guess using the minimax approach. If only one possibility remains, return it.
        if len(self.possible_guesses) == 1:
            return self.possible_guesses[0]
        return min(self.knuth_set, key=self.calculate_minimax_score)

    def calculate_minimax_score(self, guess):
        # Calculates the minimax score for a given guess.
        score_map = {}
        for possible_feedback in self.all_possible_feedbacks():
            score_map[possible_feedback] = 0
        for other_guess in self.possible_guesses:
            feedback = self.simulate_feedback(guess, other_guess)
            score_map[feedback] += 1
        return max(score_map.values())

    def all_possible_feedbacks(self):
        # Generates all possible feedback combinations.
        feedbacks = []
        for black in range(Code.code_length + 1):
            for white in range(Code.code_length - black + 1):
                feedbacks.append('8' * black + '7' * white)
        return feedbacks

    def simulate_feedback(self, guess, secret_code):
        # Simulates feedback based on a guess and the secret code, counting 'black' and 'white' responses.
        black, white = 0, 0
        guess_temp, secret_code_temp = list(guess), list(secret_code)
        for i in range(Code.code_length):
            if guess_temp[i] == secret_code_temp[i]:
                black += 1
                guess_temp[i] = secret_code_temp[i] = None
        for i in range(Code.code_length):
            if guess_temp[i] and guess_temp[i] in secret_code_temp:
                white += 1
                secret_code_temp[secret_code_temp.index(guess_temp[i])] = None
        return "8" * black + "7" * white

    def parse_feedback(self, feedback):
        # Parses feedback into counts of 'black' and 'white' responses.
        return feedback.count('8'), feedback.count('7')
