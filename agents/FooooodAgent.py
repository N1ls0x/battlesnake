from typing import Dict,Optional,Tuple
from agents.BaseAgent import BaseAgent
import numpy as np

from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.MoveResult import MoveResult
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Direction import Direction
from environment.Battlesnake.model.Position import Position
from environment.Battlesnake.model.grid_map import GridMap
from environment.Battlesnake.model.Occupant import Occupant
from environment.Battlesnake.helper.DirectionUtil import DirectionUtil

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class FooooodAgent(BaseAgent):

    def get_name(self):
        return 'HungerOfHadar'

    def get_color(self) -> Optional[Tuple]:
        return (11, 0, 107)

    def start(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    def move(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake) -> MoveResult:
        matrix = [[1] * board.width for i in range(board.height)]
        for snake in board.snakes:
            for p in snake.body:
                matrix[p.y][p.x] = 0
            if snake.snake_id != you.snake_id and len(snake.body) >= len(you.body):
                for d in snake.possible_actions():
                    p = snake.get_head().advanced(d)
                    if p.x >= 0 and p.x < board.width and p.y >= 0 and p.y < board.height:
                        matrix[p.y][p.x] = 0


        p = you.get_head()
        matrix[p.y][p.x] = 1

        print("Board")
        for r in reversed(matrix):
            print(r)

        shortest_path = []
        for p in board.food:
            grid = Grid(matrix=matrix)
            start = grid.node(you.body[0].x, you.body[0].y)
            end = grid.node(p.x, p.y)
            finder = AStarFinder()
            path, runs = finder.find_path(start, end, grid)
            if len(shortest_path) == 0 or (path and len(path) >= 2 and len(path) < len(shortest_path)):
                shortest_path = path

        if shortest_path and len(shortest_path) >= 2:
            d = DirectionUtil.direction_to_reach_field(
                Position(*shortest_path[0]), Position(*shortest_path[1]))
            return MoveResult(direction=d)

        possible_actions = you.possible_actions()

        def is_possible(d: Direction) -> bool:
            p = you.get_head().advanced(d)
            return p.x >= 0 and p.x < board.width and p.y >= 0 and p.y < board.height and matrix[p.y][p.x] != 0

        possible_actions = list(filter(is_possible, possible_actions))
        if possible_actions:
            random_action = np.random.choice(possible_actions)
            return MoveResult(direction=random_action)
        return MoveResult(direction=Direction.UP)

    def end(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass
