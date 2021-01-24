from environment.Battlesnake.model.Position import Position
from typing import List, Optional
from .EliminationEvent import EliminatedCause, EliminationEvent
from environment.Battlesnake.helper.DirectionUtil import DirectionUtil


class Snake:

    def __init__(
            self,
            snake_id: str,
            snake_name=None,
            snake_color=None,
            health=100,
            body: Optional[List[Position]] = None,
            latency=None,
            shout=None,
            squad=None,
    ):

        self.snake_id = snake_id
        self.snake_name = snake_name
        self.snake_color = snake_color
        self.body: List[Position] = body if body is not None else []
        self.health = health
        self.latency = latency
        self.shout = shout
        self.squad = squad
        self.elimination_event: Optional[EliminationEvent] = None

    def is_alive(self):
        return self.elimination_event is None

    def get_head(self) -> Optional[Position]:
        if self.is_alive():
            return self.body[0]
        else:
            return None

    def get_tail(self) -> Optional[Position]:
        if self.is_alive():
            return self.body[len(self.body) - 1]
        else:
            return None

    def get_length(self):
        if len(self.body) == 0:
            return 0

        snake_length = 1
        p = self.body[0]

        for i in range(1, len(self.body)):
            b = self.body[i]
            if p == b:
                break

            p = b
            snake_length += 1

        return snake_length

    def get_current_direction(self) -> Optional[Position]:
        if not self.is_alive() or len(self.body) <= 1:
            return None

        current_position = self.body[0]
        previous_position = self.body[1]

        return DirectionUtil.direction_to_reach_field(previous_position, current_position)

    def set_initial_position(self, starting_position: Position, n=1):
        self.body = [starting_position] * n

    def possible_actions(self):
        """
        Gibt alle erlaubten Richtungen zurück, in die sich die Schlange bewegen darf
        :return: Typ Direction
        """
        head_direction = self.get_current_direction()

        return DirectionUtil.possible_actions(head_direction)

    def export_json(self):

        body_exported = []
        for part in self.body:
            body_exported.append(part.export_json())

        return {
            "id": self.snake_id,
            "name": self.snake_name or "Unknown",
            "color": self.snake_color or (0, 0, 0),
            "health": self.health,
            "latency": self.latency,
            "body": body_exported,
            "elimination_event": self.elimination_event.export_json() if self.elimination_event is not None else None
        }

    def __eq__(self, other):
        return isinstance(other, Snake) and self.snake_id == other.snake_id
