from typing import Dict, Optional, Tuple
import numpy as np
import itertools

from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Direction import Direction


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

    # print("Board")
    # for r in reversed(matrix):
    #    print(r)

    space = 0
    for row in matrix:
        for cell in row:
            if cell == 1:
                space += 1

    return space