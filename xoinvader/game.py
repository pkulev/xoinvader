#! /usr/bin/env python3

"""Main XOInvader module, that is entry point to game.

Prepare environment for starting game and start it."""


import argparse

from xoinvader import application
from xoinvader import constants
from xoinvader import Settings


def create_game(args=None):
    """Create XOInvader game instance."""
    import curses

    import xoinvader
    xoinvader.init(args)

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

    app = application.get_application()()

    from xoinvader.ingame import InGameState
    from xoinvader.menu import MainMenuState

    Style().init_styles(curses)
    app.register_state(InGameState)
    app.register_state(MainMenuState)
    return app


def create_test_game(args=None):
    """Temporary function to create Pygame."""
    import xoinvader
    xoinvader.init(args)

    from xoinvader.teststate import TestState

    app = application.get_application()((800, 600), 0, 32)
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
        "-vd", "--video-driver", default=constants.DRIVER_NCURSES,
        type=str, choices=(constants.DRIVER_NCURSES, constants.DRIVER_SDL),
        help="use pygame")

    args = parser.parse_args()
    return args


def main():
    """Start the game!"""
    args = parse_args()

    # TODO: backend-drivers; implement proper choosing
    if args.video_driver == constants.DRIVER_SDL:
        game = create_test_game(args.__dict__)
    else:
        game = create_game(args.__dict__)

    return game.start()


if __name__ == "__main__":
    main()
