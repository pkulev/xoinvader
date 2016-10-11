#! /usr/bin/env python3

"""Main XOInvader module, that is entry point to game.

Prepare environment for starting game and start it."""


import curses
import argparse

import pygame

from xoinvader import constants
from xoinvader.menu import MainMenuState
from xoinvader.application import CursesApplication, PygameApplication
from xoinvader.common import Settings
from xoinvader.curses_utils import Style
from xoinvader.ingame import InGameState
from xoinvader.render import Renderer

from xoinvader.teststate import TestState


def create_game(args=None):
    """Create XOInvader game instance."""
    app = CursesApplication(args)
    Style().init_styles(curses)
    Settings.renderer = Renderer(Settings.layout.field.border)
    app.register_state(InGameState)
    app.register_state(MainMenuState)
    return app


def create_test_game(args=None):
    """Temporary function to create Pygame."""
    app = PygameApplication((800, 600), 0, 32)
    pygame.key.set_repeat(50, 50)
    app.register_state(TestState)
    return app


def parse_args():
    """Parse incoming arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-ns", "--no-sound", action="store_true", help="disable sounds")
    parser.add_argument(
        "-nc", "--no-color", action="store_true", help="disable colors")
    parser.add_argument(
        "-pg", "--pygame", action="store_true", help="use pygame")

    args = parser.parse_args()
    return args


def main():
    """Start the game!"""
    args = parse_args()

    # TODO: backend-drivers; implement proper choosing
    if args.pygame:
        args = args.__dict__
        del args["pygame"]
        args["video_driver"] = constants.DRIVER_SDL
        game = create_test_game(args)
    else:
        args = args.__dict__
        del args["pygame"]
        game = create_game(args)
    return game.loop()


if __name__ == "__main__":
    main()
