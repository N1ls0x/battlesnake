from enum import Enum
from typing import Optional


class EliminatedCause(Enum):

    EliminatedByCollision = "snake-collision"
    EliminatedBySelfCollision = "snake-self-collision"
    EliminatedByOutOfHealth = "out-of-health"
    EliminatedByHeadToHeadCollision = "head-collision"
    EliminatedByOutOfBounds = "wall-collision"


class EliminationEvent:

    def __init__(self, cause: EliminatedCause, turn: int, by: Optional[str]):
        self.cause: EliminatedCause = cause
        self.turn: int = turn
        self.by: Optional[str] = by

    def export_json(self):
        return {
            "cause": self.cause.value,
            "turn": self.turn,
            "by": self.by
        }