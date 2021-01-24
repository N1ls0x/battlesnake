import copy

from .Food import Food
from .Hazard import Hazard
from .Snake import Snake
from typing import List, Optional
from .Position import Position
from .grid_map import GridMap
from .Occupant import Occupant


class BoardState:

    def __init__(
            self,
            width: int,
            height: int,
            snakes: Optional[List[Snake]] = None,
            dead_snakes: Optional[List[Snake]] = None,
            food: Optional[List[Food]] = None,
            hazards: Optional[List[Hazard]] = None,
    ):

        if width < 3 or height < 3:
            raise Exception("World size must be at least 3x3")

        self.snakes: List[Snake] = snakes if snakes is not None else []  # contains only alive snakes
        self.dead_snakes: List[Snake] = dead_snakes if dead_snakes is not None else []
        self.food: List[Food] = food if food is not None else []
        self.hazards: List[Hazard] = hazards if hazards is not None else []
        self.height = height
        self.width = width

    def get_alive_and_dead_snakes(self):
        return self.snakes + self.dead_snakes

    def add_snake(self, snake: Snake):
        self.snakes.append(snake)

    def add_food(self, f: Food):
        self.food.append(f)

    def get_snake_by_id(self, snake_id) -> Optional[Snake]:
        for s in self.snakes:
            if s.snake_id == snake_id:
                return s

        return None

    def get_dead_snake_by_id(self, snake_id) -> Optional[Snake]:
        for s in self.dead_snakes:
            if s.snake_id == snake_id:
                return s

        return None

    def get_alive_or_dead_snake_by_id(self, snake_id) -> Optional[Snake]:
        return self.get_snake_by_id(snake_id) or self.get_dead_snake_by_id(snake_id)

    def is_out_of_bounds(self, p: Position):

        if p.x < 0 or p.x >= self.width:
            return True
        if p.y < 0 or p.y >= self.height:
            return True

        return False

    def is_occupied_by_food(self, p: Position):
        """Returns if the field is occupied by food"""

        for f in self.food:
            if f == p:
                return True
        return False

    def is_occupied_by_snake(self, p: Position):
        """Returns if the field is occupied by snake"""

        for s in self.snakes:
            for b in s.body:
                if b == p:
                    return True

        return False

    def is_occupied(self, p: Position):
        return self.is_occupied_by_food(p) or self.is_occupied_by_snake(p)

    def generate_grid_map(self) -> GridMap[Occupant]:

        grid_cache: GridMap = GridMap(self.width, self.height)

        for f in self.food:
            grid_cache.set_value_at_position(f, Occupant.Food)

        for snake in self.snakes:
            if not snake.is_alive():
                continue

            for b in snake.body:
                grid_cache.set_value_at_position(b, Occupant.Snake)

        return grid_cache

    def finished(self):
        return len(self.snakes) <= 1

    def get_all_snakes_sorted(self, reverse=False):

        def c(s: Snake):
            if s.elimination_event is None:
                return 9999999
            else:
                return s.elimination_event.turn

        all_snakes = self.get_alive_and_dead_snakes()
        snakes = sorted(all_snakes, key=c, reverse=reverse)
        return snakes

    def to_json(self):
        return {
            "height": self.height,
            "width": self.width,
            "food": [f.export_json() for f in self.food],
            "hazards": [h.export_json() for h in self.hazards],
            "snakes": [s.export_json() for s in self.snakes],
            "dead_snakes": [s.export_json() for s in self.dead_snakes],
        }

    def clone(self):
        return copy.deepcopy(self)

    @staticmethod
    def is_obstacle(o: Occupant):
        if o == Occupant.Snake:
            return True
        return False
