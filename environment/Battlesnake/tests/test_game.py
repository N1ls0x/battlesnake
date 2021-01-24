import unittest

from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.modes.Standard import StandardGame


class MyTestCase(unittest.TestCase):

    def test_from_game_info(self):
        game_info = GameInfo(game_id="game-abc", ruleset_name='standard', ruleset_version='v1.4.19', timeout=500)

        game = StandardGame(game_info=game_info)

        self.assertEqual(game.game_info.id, "game-abc")


if __name__ == '__main__':
    unittest.main()
