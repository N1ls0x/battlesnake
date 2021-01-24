from environment.Battlesnake.model.Food import Food
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.Hazard import Hazard
from environment.Battlesnake.model.Position import Position
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.EliminationEvent import EliminationEvent
from environment.Battlesnake.model.EliminationEvent import EliminatedCause


class Importer:
    
    @staticmethod
    def parse_request(json):

        game_json = json['game']
        turn = json['turn']
        board_json = json['board']
        you_json = json['you']

        game = Importer.parse_game_info(game_json)
        board = Importer.parse_board(board_json)
        you = Importer.parse_snake(you_json)

        return game, turn, board, you

    @staticmethod
    def parse_game_info(json):

        game_id = json['id']
        ruleset = json['ruleset']
        ruleset_name = ruleset['name'] if ruleset is not None else None
        ruleset_version = ruleset['version'] if ruleset is not None else None
        timeout = json['timeout']

        return GameInfo(
            game_id=game_id,
            ruleset_name=ruleset_name,
            ruleset_version=ruleset_version,
            timeout=timeout)

    @staticmethod
    def parse_board(json):
        height = json['height']
        width = json['width']
        food_json_list = json['food']
        hazards_json_list = json['hazards'] if 'hazards' in json else []
        snakes_json_list = json['snakes']
        # kilab specific attribute
        dead_snakes_json_list = json['dead_snakes'] if 'dead_snakes' in json else []

        food = Importer.parse_food_array(food_json_list)
        hazards = Importer.parse_hazard_array(hazards_json_list)
        snakes = Importer.parse_snake_array(snakes_json_list)
        dead_snakes = Importer.parse_snake_array(dead_snakes_json_list)

        board = BoardState(
            width=width,
            height=height,
            food=food,
            hazards=hazards,
            snakes=snakes,
            dead_snakes=dead_snakes
        )

        return board

    @staticmethod
    def parse_snake(json):

        snake_id = json['id']
        snake_name = json['name']
        # kilab specific attribute
        snake_color = json['color'] if 'color' in json else None
        health = json['health']
        body_json_list = json['body']
        latency = json['latency'] if 'latency' in json else 0
        # head = json['head']
        # length = json['length']
        shout = json['shout'] if 'shout' in json else ""
        squad = json['squad'] if 'squad' in json else ""

        body = Importer.parse_position_array(body_json_list)

        snake = Snake(
            snake_id=snake_id,
            snake_name=snake_name,
            snake_color=snake_color,
            health=health,
            body=body,
            latency=latency,
            shout=shout,
            squad=squad,
        )

        if "elimination_event" in json:
            e = json["elimination_event"]
            if e is not None:
                event = EliminationEvent(EliminatedCause(e["cause"]), e["turn"], e["by"])
                snake.elimination_event = event

        return snake

    @staticmethod
    def parse_snake_array(json_list):
        return list(map(Importer.parse_snake, json_list))

    @staticmethod
    def parse_position(json):
        x = json['x']
        y = json['y']

        return Position(x=x, y=y)

    @staticmethod
    def parse_position_array(json_list):
        return list(map(Importer.parse_position, json_list))

    @staticmethod
    def parse_food(json):
        x = json['x']
        y = json['y']

        return Food(x=x, y=y)

    @staticmethod
    def parse_food_array(json_list):
        return list(map(Importer.parse_food, json_list))

    @staticmethod
    def parse_hazard(json):
        x = json['x']
        y = json['y']

        return Hazard(x=x, y=y)

    @staticmethod
    def parse_hazard_array(json_list):
        return list(map(Importer.parse_hazard, json_list))

    @staticmethod
    def load_replay_file(filepath):
        import json
        with open(filepath, "r") as f:
            json_data = json.load(f)
        return Importer.parse_replay(json_data)

    @staticmethod
    def parse_replay(json):
        game = Importer.parse_game_info(json['game'])
        turns = json['total_turns']
        move_list = [Importer.parse_board(b) for b in json['moves']]

        return game, turns, move_list

