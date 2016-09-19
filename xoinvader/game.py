#! /usr/bin/env python3

"""Main XOInvader module, that is entry point to game.

Prepare environment for starting game and start it."""


import curses
import argparse

import pygame

from xoinvader.menu import MainMenuState
from xoinvader.ingame import InGameState
from xoinvader.render import Renderer
from xoinvader.common import Settings
from xoinvader.application import CursesApplication, PygameApplication
from xoinvader.curses_utils import style

from xoinvader.teststate import TestState


def create_game(args=None):
    """Create XOInvader game instance."""
    app = CursesApplication(args)
    style.init_styles(curses)
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
        "-pg", "--pygame", action="store_true", help="use pygame")

    args = parser.parse_args()
    return args


def main():
    """Start the game!"""
    args = parse_args()

    if args.pygame:
        game = create_test_game(args.__dict__)
    else:
        game = create_game(args.__dict__)
    return game.loop()


if __name__ == "__main__":
    main()
