import os
import json
from datetime import datetime

from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState


class Exporter:

    def __init__(self, output_folder="replays", file_name=None, append_date=False):

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        date = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        filename = file_name or date
        if append_date:
            filename += date

        if not filename.endswith(".replay"):
            filename += ".replay"

        self.outpath = os.path.join(output_folder, filename)
        self.tempfile = os.path.join(output_folder, filename.replace(".replay", ".temp"))

        self.game_meta_info = {}
        self.history = []

    def add_initial_state(self, game_info: GameInfo, board: BoardState):
        self.game_meta_info = game_info.export_json()
        self.history.append(board.to_json())

    def add_latest_game_step(self, board: BoardState):
        self.history.append(board.to_json())

        if board.finished():
            self.write_replay_to_file()

    def write_replay_to_file(self):
        with open(self.tempfile, "w+") as f:
            json.dump({
                "game": self.game_meta_info,
                "total_turns": len(self.history),
                "moves": self.history
            }, f)

        os.rename(self.tempfile, self.outpath)
        print(f"Success! Wrote to {self.outpath}")

    @staticmethod
    def export_request(game_info: GameInfo, turn: int, board: BoardState, you: Snake):

        return {
            'game': game_info.export_json(),
            'turn': turn,
            'board': board.to_json(),
            'you': you.export_json()
        }
