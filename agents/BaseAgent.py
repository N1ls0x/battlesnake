from abc import abstractmethod
from typing import Tuple, Optional

from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.MoveResult import MoveResult
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState


class BaseAgent:

    @abstractmethod
    def get_name(self):
        pass

    def get_color(self) -> Optional[Tuple]:
        return None

    def get_color_hex(self):
        color_tuple = self.get_color()

        if color_tuple is not None:
            return '#%02x%02x%02x' % color_tuple

    def get_author(self):
        return None

    def get_head(self):
        # only for battlesnake online
        # see https://docs.battlesnake.com/references/personalization
        return None

    def get_tail(self):
        # only for battlesnake online
        # see https://docs.battlesnake.com/references/personalization
        return None

    def user_key_pressed(self, key):
        pass

    @abstractmethod
    def start(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    @abstractmethod
    def move(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake) -> MoveResult:
        pass

    @abstractmethod
    def end(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass
