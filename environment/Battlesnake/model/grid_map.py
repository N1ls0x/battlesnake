from .Position import Position
from typing import Optional, Generic, TypeVar
from .Occupant import Occupant

T = TypeVar('T')


class GridMap(Generic[T]):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid_cache = [[None for _ in range(height)] for _ in range(width)]

    def is_valid_at(self, x: int, y: int):
        return 0 <= x < self.width and 0 <= y < self.height

    def set_value_at(self, x: int, y: int, v: Optional[T], check_range=False):
        if check_range and not self.is_valid_at(x=x, y=y):
            return

        self.grid_cache[x][y] = v

    def set_value_at_position(self, pos: Position, v: Optional[T], check_range=False):
        return self.set_value_at(x=pos.x, y=pos.y, v=v, check_range=check_range)

    def get_value_at_position(self, position: Position) -> T:
        return self.get_value_at(position.x, position.y)

    def get_value_at(self, x: int, y: int) -> T:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None

        return self.grid_cache[x][y]


    def dump(self):
        for y in range(self.height):
            for x in range(self.width):
                o = self.get_value_at(x, y)
                if o == Occupant.Food:
                    print(" x", end="")
                elif o == Occupant.Snake:
                    print(" ~", end="")
                else:
                    print(" _", end="")
            print()
