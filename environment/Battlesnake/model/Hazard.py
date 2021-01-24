from environment.Battlesnake.model.Position import Position


class Hazard(Position):

    def __init__(self, x: int = None, y: int = None, position: Position = None):
        super().__init__(x=x, y=y, position=position)

    def export_json(self):
        return super().export_json()
