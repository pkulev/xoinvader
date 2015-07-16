"""MainMenuState-related input and event handlers."""


import os
import sys

from xoinvader.keys import *
from xoinvader.handlers import Command, Handler
from xoinvader.curses_utils import deinit_curses


class ExitGameCommand(Command):
    def execute(self, actor):
        deinit_curses(actor)
        sys.exit(os.EX_OK)

class ToInGameCommand(Command):
    def execute(self, actor):
        actor.owner.state = "InGameState"


class MainMenuInputHandler(Handler):
    def __init__(self, owner):
        super(MainMenuInputHandler, self).__init__(owner)

        self._command_map = {
            K_ESCAPE : ToInGameCommand(),
            K_R : ExitGameCommand()
        }

    def handle(self):
        key = self._screen.getch()
        cmd = self._command_map.get(key, None)
        if cmd:
            if isinstance(cmd, ExitGameCommand):
                cmd.execute(self._screen)
            elif isinstance(cmd, ToInGameCommand):
                cmd.execute(self._owner)
            else:
                cmd.execute(self._actor)


class MainMenuEventHandler(Handler):
    def __init__(self, owner):
        super(MainMenuEventHandler, self).__init__(owner)

        self._input_handler = MainMenuInputHandler(owner)

    def handle(self):
        self._input_handler.handle()
        # Some other event stuff
