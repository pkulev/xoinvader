#! /usr/bin/env python3

"""Main XOInvader module, that is entry point to game.

Prepare environment for starting game and start it."""


import argparse
import logging

import xoinvader
from xoinvader.application import CursesApplication
from xoinvader import constants


LOG = logging.getLogger(__name__)


def create_game():
    """Create XOInvader game instance."""

    import curses

    from xoinvader.curses_utils import Style

    # TODO: config-management: remove import order dependency
    # problem: importing of .common creates settings dict on import time
    #          then importing of game state pulls Ship and then Mixer
    #          mixer chooses mixer on import time based on settings
    #          update_system_settings called in run time, updates settings...
    #          but dependent entities already created when imported.
    # solutions:
    #          * Remove import time magic
    #            Create defaults, but make decisions on run time only
    #            Maybe this will lead to reorganizing code.

    app = CursesApplication()

    from xoinvader.ingame import InGameState
    from xoinvader.menu import PauseMenuState, GameOverState

    Style().init_styles(curses)
    app.register(InGameState)
    app.register(PauseMenuState)
    app.register(GameOverState)
    return app


def parse_args():
    """Parse incoming arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--debug", action="store_true", help="enable debug mode")
    parser.add_argument(
        "-ns", "--no-sound", action="store_true", help="disable sounds")
    parser.add_argument(
        "-nc", "--no-color", action="store_true", help="disable colors")

    args = parser.parse_args()
    return args


def main():
    """Start the game!"""

    args = parse_args()
    # apply settings to engine settings
    xoinvader.init(args.__dict__)
    LOG.debug("Incoming args: %s", args)

    game = create_game()
    return game.start()


if __name__ == "__main__":
    main()
