from typing import Dict
from agents.BaseAgent import BaseAgent
import numpy as np
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.MoveResult import MoveResult
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Direction import Direction
from environment.Battlesnake.model.grid_map import GridMap
from environment.Battlesnake.model.Occupant import Occupant


class RandomAgent(BaseAgent):

    def get_name(self):
        return 'RandomSnake'

    def start(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    def move(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake) -> MoveResult:

        possible_actions = you.possible_actions()

        if possible_actions is None:
            return None

        grid_map = board.generate_grid_map()

        busy_action = self.feel_busy(board, you, grid_map)
        if busy_action is not None:
            return MoveResult(direction=busy_action)

        random_action = np.random.choice(possible_actions)
        return MoveResult(direction=random_action)

    def end(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    def feel_busy(self, board: BoardState, snake: Snake, grid_map: GridMap):

        possible_actions = snake.possible_actions()
        head = snake.get_head()

        if possible_actions is None:
            return None

        actions_without_obstacle = []

        for action in possible_actions:
            next_field = head.advanced(action)
            object_at_field = grid_map.get_value_at_position(next_field)

            if board.is_out_of_bounds(next_field):
                continue

            if object_at_field == Occupant.Snake:
                continue

            actions_without_obstacle.append(action)

        if len(actions_without_obstacle) > 0:
            return np.random.choice(actions_without_obstacle)
        else:
            return None
