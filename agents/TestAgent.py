from typing import Dict,Optional,Tuple
from agents.BaseAgent import BaseAgent
import numpy as np
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.MoveResult import MoveResult
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Direction import Direction
from environment.Battlesnake.model.grid_map import GridMap
from environment.Battlesnake.model.Occupant import Occupant


class TestAgent(BaseAgent):

    def get_name(self):
        return 'Test'
    
    def get_color(self) -> Optional[Tuple]:
        return (0, 127, 21)

    def start(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    def move(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake) -> MoveResult:
        pass

    def end(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

   