from .Occupant import Occupant
from .Direction import Direction
from typing import Optional


class Field:

    def __init__(self,
                 o: Occupant,
                 id: Optional[int],
                 d: Optional[Direction]):

        self.occupant = o
        self.id = id
        self.direction = d

    def WithModifiedDirection(self, d: Direction):
        return Field(self.occupant, self.id, d)
