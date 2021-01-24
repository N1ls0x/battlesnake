from environment.Battlesnake.model.Direction import Direction


class MoveResult:

    def __init__(self, direction: Direction, shout: str = None):
        self.direction: Direction = direction
        self.shout = shout
