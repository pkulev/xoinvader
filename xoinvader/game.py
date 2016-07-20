#! /usr/bin/env python3

"""Main XOInvader module, that is entry point to game.

Prepare environment for starting game and start it."""


import curses
import argparse

from xoinvader.menu import MainMenuState
from xoinvader.ingame import InGameState
from xoinvader.render import Renderer
from xoinvader.common import Settings
from xoinvader.application import get_application
from xoinvader.curses_utils import deinit_curses
from xoinvader.curses_utils import style


class XOInvader(get_application()):
    """Main game class."""
    def __init__(self, startup_args=None):
        super(XOInvader, self).__init__(startup_args)

        # Ms per frame
        self._mspf = 16

        style.init_styles(curses)
        Settings.renderer = Renderer(Settings.layout.field.border)

    def stop(self):
        deinit_curses(self.screen)
        super(XOInvader, self).stop()


def create_game(args=None):
    """Create XOInvader game instance."""
    app = XOInvader(args)
    app.register_state(InGameState)
    app.register_state(MainMenuState)
    return app


def parse_args():
    """Parse incoming arguments."""
    parser = argparse.ArgumentParser()

    add_args = dict(
        no_sound=dict(
            default=False,
            action="store_true",
            help="Disable sounds."))

    parser.add_argument("-ns", "--no-sound", **add_args["no_sound"])

    args = parser.parse_args()
    return args


def main():
    """Start the game!"""
    args = parse_args()

    game = create_game(args.__dict__)
    return game.loop()


if __name__ == "__main__":
    main()
