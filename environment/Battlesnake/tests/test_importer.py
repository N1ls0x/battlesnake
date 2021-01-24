import unittest
import json
import os

from environment.Battlesnake.importer.Importer import Importer
from environment.Battlesnake.model.Position import Position


class ImporterTestCase(unittest.TestCase):

    def test_parse_request(self):

        with open(os.path.dirname(__file__) + '/data/request_1.json') as json_file:
            data = json.load(json_file)

        print(data)

        parsed = Importer.parse_request(data)
        print(parsed)

        game_info, turn, board, you = parsed

        self.assertEqual(game_info.id, "game-00fe20da-94ad-11ea-bb37")
        self.assertEqual(game_info.ruleset['name'], "standard")
        self.assertEqual(game_info.ruleset['version'], "v.1.2.3")
        self.assertEqual(game_info.timeout, 500)

        self.assertEqual(turn, 14)
        self.assertEqual(you.snake_id, "snake-508e96ac-94ad-11ea-bb37")
        self.assertEqual(you.snake_name, "My Snake")
        self.assertEqual(you.health, 54)
        self.assertEqual(you.body[1], Position(x=1, y=0))
        self.assertEqual(you.get_length(), 3)
        self.assertEqual(you.latency, "111")
        self.assertEqual(you.shout, "why are we shouting??")
        self.assertEqual(you.squad, "")

        self.assertEqual(board.height, 11)
        self.assertEqual(board.width, 11)
        self.assertEqual(len(board.snakes), 2)
        self.assertEqual(board.snakes[0].snake_id, "snake-508e96ac-94ad-11ea-bb37")
        self.assertEqual(board.snakes[1].snake_id, "snake-b67f4906-94ae-11ea-bb37")
        self.assertEqual(len(board.food), 3)
        self.assertEqual(board.food[0], Position(x=5, y=5))
        self.assertEqual(board.food[1], Position(x=9, y=0))
        self.assertEqual(board.food[2], Position(x=2, y=6))

        self.assertEqual(len(board.hazards), 1)
        self.assertEqual(board.hazards[0], Position(x=3, y=2))

    def test_parse_snake(self):

        data = {
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [
                {"x": 0, "y": 5},
                {"x": 1, "y": 5},
                {"x": 1, "y": 4}
            ],
            "latency": "111",
            "head": {"x": 0, "y": 0},
            "length": 3,
            "shout": "why are we shouting??",
            "squad": "A"
        }

        snake = Importer.parse_snake(data)

        self.assertEqual(snake.snake_id, "snake-508e96ac-94ad-11ea-bb37")
        self.assertEqual(snake.snake_name, "My Snake")
        self.assertEqual(snake.health, 54)
        self.assertEqual(len(snake.body), 3)
        self.assertEqual(snake.body[0], Position(x=0, y=5))
        self.assertEqual(snake.body[1], Position(x=1, y=5))
        self.assertEqual(snake.body[2], Position(x=1, y=4))
        self.assertEqual(snake.get_length(), 3)
        self.assertEqual(snake.latency, "111")
        self.assertEqual(snake.shout, "why are we shouting??")
        self.assertEqual(snake.squad, "A")


if __name__ == '__main__':
    unittest.main()
