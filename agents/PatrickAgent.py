from typing import Dict,Optional,Tuple
from agents.BaseAgent import BaseAgent
import numpy as np
import random
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.MoveResult import MoveResult
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Direction import Direction
from environment.Battlesnake.model.grid_map import GridMap
from environment.Battlesnake.model.Occupant import Occupant


class PatrickAgent(BaseAgent):

    def get_name(self):
        return 'Patrick'
    
    def get_color(self) -> Optional[Tuple]:
        return (0, 127, 20)

    def start(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    def move(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake) -> MoveResult:
        move = random.choice(list(Direction))
        print(move)
        return MoveResult(direction=move)

    def end(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass