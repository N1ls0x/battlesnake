from .Direction import Direction


class Position:

    def __init__(self, x: int = None, y: int = None, position: 'Position' = None):

        if position is not None:
            x = position.x
            y = position.y

        if x is None:
            raise ValueError('you must provide (x, y) or position')

        self.x = x
        self.y = y

    def advanced(self, d: Direction):
        if d == Direction.UP:
            return Position(self.x, self.y + 1)
        elif d == Direction.LEFT:
            return Position(self.x - 1, self.y)
        elif d == Direction.RIGHT:
            return Position(self.x + 1, self.y)
        elif d == Direction.DOWN:
            return Position(self.x, self.y - 1)
        else:
            raise ValueError("Invalid direction: {}".format(d))

    def is_position_equal_to(self, c: 'Position'):
        return self.x == c.x and self.y == c.y

    def __eq__(self, other):
        return self.is_position_equal_to(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return '{} ({}, {})'.format(self.__class__.__name__, self.x, self.y)

    def __repr__(self):
        return str(self)

    def export_json(self):
        return {
            'x': self.x,
            'y': self.y
        }
