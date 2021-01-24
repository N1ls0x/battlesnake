
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.modes.Standard import StandardGame
from environment.Battlesnake.helper.helper import Helper
from environment.Battlesnake.model.Snake import Snake
from typing import List, Optional, Dict
from environment.Battlesnake.model.Snake import Snake


class SoloGame(StandardGame):

    def __init__(
            self,
            timeout: int = 400,
            game_info: Optional[GameInfo] = None,
            food_spawn_chance=0.15,
            minimumFood=1
    ):
        super().__init__(timeout, game_info, food_spawn_chance, minimumFood)

    def create_game_info(self, game_info: GameInfo, timeout: int):
        if game_info is None:
            game_id = Helper.generate_game_id()
            game_info = GameInfo(game_id=game_id, ruleset_name='solo',
                                 ruleset_version='v1.0.0', timeout=timeout)
        else:
            assert game_info.ruleset['name'] == 'solo'
        return game_info

    def is_game_over(self, board: BoardState) -> bool:
        for s in board.snakes:
            if s.is_alive():
                return False
        return True
