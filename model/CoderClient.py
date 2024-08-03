import random
import requests
from model.Color import Code
from abc import ABC, abstractmethod
from retrying import retry

from view.UI import UI


class CoderBaseClient(ABC):
    def __init__(self):
        self._secret_code = []
        self._code_length = Code.code_length
        self._n_color = Code.n_color

    @abstractmethod
    def set_secret_code(self):
        pass

    @abstractmethod
    def get_feedback(self, guess):
        pass


class CoderLocalClient(CoderBaseClient):

    def get_feedback(self, guess):
        if not self._secret_code:
            raise ValueError("Geheimcode wird noch nicht gesetzt")

        # Convert guess to a list of integers for comparison
        guess_temp = [int(i) for i in guess]

        # Ensure the length of the converted guess matches the secret code's length
        if len(guess_temp) != self._code_length:
            raise ValueError("Die Länge des Rates stimmt nicht mit der Geheimcodeslänge überein.")

        black, white = 0, 0
        secret_code_temp = self._secret_code.copy()

        # Count black pegs first (correct color and position)
        for i in range(self._code_length):
            if guess_temp[i] == secret_code_temp[i]:
                black += 1
                # Mark positions that have been matched
                secret_code_temp[i] = guess_temp[i] = None

        # Then count white pegs (correct color, wrong position)
        for i in range(self._code_length):
            if guess_temp[i] is not None and guess_temp[i] in secret_code_temp:
                white += 1
                # Remove the matched color to prevent double counting
                secret_code_temp[secret_code_temp.index(guess_temp[i])] = None

        # Construct feedback string based on black and white peg counts
        feedback = "8" * black + "7" * white
        return feedback

    def set_secret_code(self):
        self._secret_code = [random.randint(1, self._n_color) for _ in range(self._code_length)]


    def set_secret_code_manually(self):
        while True:
            try:
                code = [int(i) for i in input(
                    f"Bitte geben Sie den Geheimcode mit der Nummer von 1 bis {self._n_color} ({self._code_length} Ziffer) ein: ")]
                if len(code) == self._code_length and all(1 <= c <= self._n_color for c in code):
                    self._secret_code = code
                    break
                else:
                    print(f"Falsche Eingabe. Bitte geben Sie nur {self._code_length} -stellige Zahlen von 1 bis {self._n_color} ein.")
            except ValueError:
                print("Bitte geben Sie nur die Nummer ein")

    def get_secret_code(self):
        return ''.join(str(digit) for digit in self._secret_code)


class CoderNetworkClient(CoderBaseClient):
    def __init__(self, ip_address, port):
        super().__init__()
        self._server_URL = f"http://{ip_address}:{port}"
        self._gameID = 0
        self.gamerID = ""

    def create_data(self, gameid, gamerid, positions, colors, value):
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://htwberlin.com/ssr/superhirnserver/move_schema.json",
            "title": "Move",
            "_comment": "Farbkodierung= 1=Rot, 2=Grün, 3=Gelb, 4=Blau, 5=Orange, 6=Braun, 7=Weiss (Bewertung bzw. Spielfarbe), 8=Schwarz (Bewertung bzw. Spielfarbe)",
            "gameid": gameid,
            "gamerid": gamerid,
            "positions": positions,
            "colors": colors,
            "value": value,
            "required": ["gameid", "gamerid", "positions", "colors", "value"]
        }

    @retry(wait_fixed=3000, stop_max_attempt_number=10)
    def send_post_request(self, data):
        try:
            response = requests.post(self._server_URL, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Netzwerkfehler: {e}")
            return None

    def get_feedback(self, guess):
        data = self.create_data(self._gameID, self.gamerID, self._code_length, self._n_color, guess)
        response = self.send_post_request(data)
        return response['value']

    def set_secret_code(self):
        data = self.create_data(self._gameID, self.gamerID, self._code_length, self._n_color, "")
        response = self.send_post_request(data)
        self._gameID = response['gameid']


class CoderClientFactory:
    @staticmethod
    def create(coder_type, ip_address, port):
        if coder_type == 2:
            return CoderLocalClient()
        elif coder_type == 1:
            return CoderNetworkClient(ip_address, port)
        else:
            raise ValueError("Unbekannter Coder-Typ")
