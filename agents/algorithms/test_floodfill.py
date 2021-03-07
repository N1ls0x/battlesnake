from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.Position import Position

from agents.algorithms.floodfill import flood_fill


def test_floodfill_all():
    you = Snake("a", body=[Position(0,0), Position(1,0), Position(2,0)])
    board_state = BoardState(11, 11, snakes=[you])

    space = flood_fill(board_state, you)
    assert space == 11 * 11


def test_floodfill_two_snakes():
    you = Snake("a", body=[Position(0,0), Position(1,0), Position(2,0)])
    enemy = Snake("b", body=[Position(10,10), Position(9,10), Position(8,10)])
    board_state = BoardState(11, 11, snakes=[you, enemy])

    space = flood_fill(board_state, you)
    assert space == 53
