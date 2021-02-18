from environment.battlesnake_environment import BattlesnakeEnvironment, GameMode
from agents.RemoteAgent import RemoteAgent
from agents.RandomAgent import RandomAgent
from agents.FooooodAgent import FooooodAgent
from agents.SpaceAgent import SpaceAgent
from agents.TestAgent import TestAgent
import time

agents = [
    TestAgent(),
    FooooodAgent(),
    FooooodAgent(),
    SpaceAgent(),
]
env = BattlesnakeEnvironment(
    width=11,
    height=11,
    agents=agents,
    act_timeout=0.4,
    export_games=False,
    speed_initial=2,
)

env.reset()
env.render()

while True:

    step_start_time = time.time()
    env.handle_input()
    env.step()
    env.render()
    step_time = int((time.time() - step_start_time) * 1000)

    env.wait_after_step(step_time)
