import requests

from agents.BaseAgent import BaseAgent
from environment.Battlesnake.exporter.Exporter import Exporter
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.MoveResult import MoveResult
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.server import BattlesnakeServer


class RemoteAgent(BaseAgent):

    def __init__(self, url: str, config = None):

        if not url.startswith('http'):
            url = 'http://' + url

        self.name = None
        self.url = RemoteAgent.urljoin(url, '?kilab=1')
        self.url_start = RemoteAgent.urljoin(url, 'start')
        self.url_move = RemoteAgent.urljoin(url, 'move')
        self.url_end = RemoteAgent.urljoin(url, 'end')
        self.config = config

        try:
            result = requests.get(self.url)

            if result.status_code != 200:
                raise ValueError('RemoteAgent did not return status 200. Got status {}: \n\n{}'.format(
                    result.status_code, result.text))

            data = result.json()

            if 'name' in data:
                self.name = data['name']

        except requests.RequestException:
            raise ValueError('agent did not respond ({})'.format(self.url))

    def get_name(self):
        if self.name:
            return self.name
        if self.config:
            return f'{self.config}'
        return 'RemoteBattlesnake'

    def get_color(self):
        return None

    def user_key_pressed(self, key):
        pass

    def start(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):

        json_data = Exporter.export_request(
            game_info=game_info, turn=turn, board=board, you=you)

        if self.config:
            json_data["config"] = self.config

        try:
            result = requests.post(
                self.url_start, json=json_data, timeout=game_info.timeout / 1000)
        except requests.RequestException:
            print(json_data)
            print('RemoteAgent ({} raises request exception on start)'.format(self.url))
            return None

        if result.status_code != 200:
            print(json_data)
            print('ERROR: agent did not return 200 on start call',
                  result.status_code)
            print(result.text)

    def move(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake) -> MoveResult:

        json_data = Exporter.export_request(
            game_info=game_info, turn=turn, board=board, you=you)

        try:
            result = requests.post(
                self.url_move, json=json_data, timeout=game_info.timeout / 1000)
        except requests.RequestException:
            print(json_data)
            print('RemoteAgent ({} raises request exception on move)'.format(self.url))
            return None

        if result.status_code == 200:
            data = result.json()

            if data:
                move = data['move'] if 'move' in data else None
                shout = data['shout'] if 'shout' in data else None

                direction = BattlesnakeServer.encode_direction(move)

                return MoveResult(direction=direction, shout=shout)
        else:
            print(json_data)
            print('ERROR: agent did not return 200 on start call',
                  result.status_code)
            print(result.text)

    def end(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):

        json_data = Exporter.export_request(
            game_info=game_info, turn=turn, board=board, you=you)

        try:
            result = requests.post(
                self.url_end, json=json_data, timeout=game_info.timeout / 1000)
        except requests.RequestException:
            print(json_data)
            print('RemoteAgent ({} raises request exception on end)'.format(self.url))
            return None

        if result.status_code != 200:
            print(json_data)
            print('ERROR: agent did not return 200 on end call',
                  result.status_code)
            print(result.text)

    def urljoin(*args):
        """
        Joins given arguments into an url. Trailing but not leading slashes are
        stripped for each argument.
        """

        return "/".join(map(lambda x: str(x).rstrip('/'), args))
