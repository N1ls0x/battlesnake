from typing import List, Optional
from environment.Battlesnake.model.Position import Position
from environment.Battlesnake.model.Direction import Direction


class DirectionUtil:

    @staticmethod
    def possible_actions(head_direction: Optional[Direction]):

        if head_direction is None:
            return [Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT]
        elif head_direction == Direction.UP:
            return [Direction.UP, Direction.RIGHT, Direction.LEFT]
        elif head_direction == Direction.RIGHT:
            return [Direction.UP, Direction.RIGHT, Direction.DOWN]
        elif head_direction == Direction.DOWN:
            return [Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        elif head_direction == Direction.LEFT:
            return [Direction.UP, Direction.DOWN, Direction.LEFT]
        else:
            print('ERROR unknown direction')
            return None

    @staticmethod
    def direction_to_reach_field(from_position: Position, to_position: Position):

        delta_x = to_position.x - from_position.x
        delta_y = to_position.y - from_position.y

        if delta_x == 0 and delta_y == 0:
            return None
        elif abs(delta_x) > abs(delta_y):
            # horizontale Bewegung

            if delta_x > 0:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        else:
            if delta_y > 0:
                return Direction.UP
            else:
                return Direction.DOWN

    @staticmethod
    def neighbor_positions(pos: Position) -> List[Position]:

        return [
            Position(x=pos.x - 1, y=pos.y),
            Position(x=pos.x, y=pos.y - 1),
            Position(x=pos.x, y=pos.y + 1),
            Position(x=pos.x + 1, y=pos.y),
        ]
