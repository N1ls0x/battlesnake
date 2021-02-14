from typing import Dict, Optional, Tuple
from agents.BaseAgent import BaseAgent
import numpy as np
import itertools

from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.MoveResult import MoveResult
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Direction import Direction
from environment.Battlesnake.model.Position import Position
from environment.Battlesnake.model.grid_map import GridMap
from environment.Battlesnake.model.Occupant import Occupant
from environment.Battlesnake.helper.DirectionUtil import DirectionUtil
from environment.Battlesnake.modes.Standard import StandardGame

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class SpaceAgent(BaseAgent):

    def get_name(self):
        return 'SpaceAgent'

    def get_color(self) -> Optional[Tuple]:
        return (127, 0, 0)

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

        # print("Board")
        # for r in reversed(matrix):
        #     print(r)
        
        min_spaces: Dict[Direction, int] = dict()
        for d in you.possible_actions():
            min_spaces[d] = min_space(board, you, d)
            shortest_path = []

        for p in board.food:
                grid = Grid(matrix=matrix)
                start = grid.node(you.body[0].x, you.body[0].y)
                end = grid.node(p.x, p.y)
                finder = AStarFinder()
                path, runs = finder.find_path(start, end, grid)
        if  you.health < 30 or len(you.body) < 12 or len(snake.body) > 29 and len(you.body) < len(snake.body):
            if path and len(path) >= 2 and (len(shortest_path) == 0 or len(path) < len(shortest_path)):
                d = DirectionUtil.direction_to_reach_field(
                    Position(*path[0]), Position(*path[1]))
            space = min_spaces[d]
            print("space", space)
            if space >= len(you.body):
               # gucken ob genügent platz
                shortest_path = path

            if shortest_path and len(shortest_path) >= 2:
               d = DirectionUtil.direction_to_reach_field(
                    Position(*shortest_path[0]), Position(*shortest_path[1]))
               return MoveResult(direction=d)

        possible_actions = you.possible_actions()

        matrix = [[1] * board.width for i in range(board.height)]
        for snake in board.snakes:
            for p in snake.body:
                matrix[p.y][p.x] = 0
        def is_possible(d: Direction) -> bool:
            p = you.get_head().advanced(d)
            return p.x >= 0 and p.x < board.width and p.y >= 0 and p.y < board.height and matrix[p.y][p.x] != 0

        if possible_actions:
            possible_actions.sort(key=lambda d: min_spaces[d] if is_possible(d) else -1)
            max_space_action = possible_actions[-1]
            return MoveResult(direction=max_space_action)
        return MoveResult(direction=Direction.UP)

    def end(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    def get_head(self):
        # only for battlesnake online
        # see https://docs.battlesnake.com/references/personalization
        return "pixel"

    def get_tail(self):
        # only for battlesnake online
        # see https://docs.battlesnake.com/references/personalization
        return "pixel"


def distance(a: Position, b: Position) -> int:
    return abs(a.x - b.x) + abs(a.y + b.y)


def min_space(state: BoardState, you: Snake, you_action: Direction) -> int:
    game = StandardGame()
    min_space = state.width * state.height
    enemy_list = []
    enemies = []
    if len(state.snakes) > 3:
        state = state.clone()
        farest_snake = sorted(state.snakes , key=lambda s: distance(s.get_head(), you.get_head()))[-1]
        state.snakes.remove(farest_snake)

    for snake in state.snakes:
        if snake.snake_id != you.snake_id:
            enemy_list.append(snake.possible_actions())
            enemies.append(snake.snake_id)
    enemy_actions_list = list(itertools.product(*enemy_list))
    for enemy_actions in enemy_actions_list:
        actions = {you.snake_id: you_action}
        for enemy, action in zip(enemies, enemy_actions):
            actions[enemy] = action
        next_state = state.clone()
        game.create_next_board_state(next_state, actions)
        space = flood_fill(next_state, you)
        if space < min_space:
            min_space = space
    return min_space


def flood_fill(state: BoardState, you: Snake) -> int:
    queue = []
    for snake in state.snakes:
        if snake.snake_id == you.snake_id:
            queue.append((1, snake.get_head()))

    if not queue:
        return 0  # we are dead

    for snake in state.snakes:
        if snake.snake_id != you.snake_id:
            if len(snake.body) >= len(you.body):
                queue.insert(0, (2, snake.get_head()))
            else:
                queue.append((2, snake.get_head()))

    if len(queue) == 1:
        return state.width * state.width

    matrix = [[0] * state.width for i in range(state.height)]
    for snake in state.snakes:
        for p in snake.body[1:]:
            matrix[p.y][p.x] = 3

    while queue:
        snake, p = queue.pop(0)
        if 0 <= p.x < state.width and 0 <= p.y < state.height:
            if matrix[p.y][p.x] == 0:
                matrix[p.y][p.x] = snake
                for d in Direction:
                    nextp = p.advanced(d)
                    queue.append((snake, nextp))

    print("Board")
    for r in reversed(matrix):
        print(r)

    space = 0
    for row in matrix:
        for cell in row:
            if cell == 1:
                space += 1

    return space


def test_flood_fill():
    print("Hello World")
    assert False
