import pytest
import os


@pytest.fixture
def default_exporter():
    from environment.Battlesnake.exporter.Exporter import Exporter
    return Exporter(output_folder="replay_test")

@pytest.fixture
def basic_exporter():
    from environment.Battlesnake.exporter.Exporter import Exporter
    return Exporter(output_folder="replay_test", file_name="test.replay")

@pytest.fixture
def sample_env():
    from agents.RandomAgent import RandomAgent
    from agents.SimpleAgent_solution import SimpleAgent
    from environment.battlesnake_environment import BattlesnakeEnvironment
    
    agents = [RandomAgent(), SimpleAgent()]
    env = BattlesnakeEnvironment(
        width=15,
        height=15,
        agents=agents,
        act_timeout=0.2
    )
    env.reset()
    return env

def test_directory_created(basic_exporter):
    assert os.path.exists("replay_test")

def test_game_info(basic_exporter):
    from environment.Battlesnake.model.GameInfo import GameInfo
    g = GameInfo(game_id="test", ruleset_name="standard", ruleset_version="1.0.0", timeout=500)
    basic_exporter.add_initial_state(game_info=g)
    basic_exporter.write_replay_to_file()

    expected = str({"game": g.export_json(), "total_turns": 0, "moves": []}).replace("'", '"')
    with open("replay_test/test.replay", "r", encoding="utf-8") as f:
        result = f.read()

    print(expected)
    print(result)
    assert expected == result
    os.unlink("replay_test/test.replay")

def test_board_state_write(basic_exporter):
    from environment.Battlesnake.model.GameInfo import GameInfo
    from environment.Battlesnake.modes.Standard import StandardGame
    from environment.Battlesnake.model.Snake import Snake

    g = GameInfo(game_id="test", ruleset_name="standard", ruleset_version="1.0.0", timeout=400)
    basic_exporter.add_initial_state(game_info=g)
    
    game = StandardGame()
    game.create_initial_board_state(width=15, height=15, snake_ids=["1", "2"])
    basic_exporter.add_latest_game_step(game)
    basic_exporter.write_replay_to_file()

    expected = str({"game": g.export_json(), "total_turns": 1, "moves": [{
            "height": 15,
            "width": 15,
            "food": [f.export_json() for f in game.state.food],
            "snakes": [s.export_json() for s in game.state.all_snakes]
        }]}).replace("'", '"').replace("None", "null").replace("(", "[").replace(")", "]")

    
    with open("replay_test/test.replay", "r") as f:
        result = f.read()

    assert expected == result
    os.unlink("replay_test/test.replay")

def test_full_replay_cycle():
    from environment.battlesnake_environment import BattlesnakeEnvironment
    from agents.RandomAgent import RandomAgent
    from environment.Battlesnake.importer.Importer import Importer
    from environment.Battlesnake.renderer.game_renderer import GameRenderer

    agents = [RandomAgent(), RandomAgent()]

    env = BattlesnakeEnvironment(
        width=15,
        height=15,
        agents=agents,
        act_timeout=0.1,
        export_games=True
    )

    env.reset()

    while not env.game.is_game_over():
        env.step()

    assert os.path.exists(env.exporter.outpath)
    assert os.path.getsize(env.exporter.outpath) > 0
    game, turns, move_list = Importer.load_replay_file(env.exporter.outpath)

    width, height = move_list[0].width, move_list[0].width
    num_snakes = len(move_list[0].snakes)

    renderer = GameRenderer(width, height, num_snakes)

    assert len(move_list) >= 1
    assert len(move_list) == turns
    assert game

    for move in move_list:
        renderer.display(move)
    
    os.unlink(env.exporter.outpath)

    # TODO: Could be moved special place, so that always at the end
    import shutil
    shutil.rmtree("replays", ignore_errors=True)
    shutil.rmtree("replay_test", ignore_errors=True)