#! /usr/bin/env python3

"""Main XOInvader module, that is entry point to game.

Prepare environment for starting game and start it."""


import curses

from xoinvader.menu import MainMenuState
from xoinvader.ingame import InGameState
from xoinvader.render import Renderer
from xoinvader.common import Settings
from xoinvader.application import Application
from xoinvader.curses_utils import create_curses_window
from xoinvader.curses_utils import deinit_curses
from xoinvader.curses_utils import style


class XOInvader(Application):
    """Main game class."""
    def __init__(self, startup_args=None):
        super(XOInvader, self).__init__(startup_args)
        self.screen = create_curses_window(
                ncols=Settings.layout.field.border.x,
                nlines=Settings.layout.field.border.y)

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
