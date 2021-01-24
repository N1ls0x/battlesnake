import pygame
import time
import argparse
import os
from environment.Battlesnake.renderer.replay_controller import ReplayController
from environment.Battlesnake.importer.Importer import Importer

parser = argparse.ArgumentParser(description='Load and show a replay file.')
parser.add_argument('-f', '--file', help='The path to the replay file', required=True)
args = parser.parse_args()

replay_controller = ReplayController()

replay_controller.load_replay(args.file)
replay_controller.show_game(0)
# Note: On Mac OS there is a bug in pygame 1.9.
# when only a grey window shows up, try installing pygame version 2

while True:
    replay_controller.update()
    pygame.time.wait(10)
