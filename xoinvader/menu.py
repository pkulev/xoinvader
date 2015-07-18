"""MainMenuState-related input and event handlers."""


import os
import sys

from xoinvader.keys import *
from xoinvader.state import State
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


class MainMenuState(State):
    def __init__(self, owner):
        super(MainMenuState, self).__init__(owner)
        self._screen = owner.screen
        self._actor = None

        self._items = {
            "New Game": 1,
            "Continue": 2,
            "Exit": 3}
        self._currentMenu = None
        self._events = MainMenuEventHandler(self)

#    def register_menu_item(self, caption, item_action_list):
    def events(self):
        self._events.handle()

    def update(self):
        pass

    def render(self):
        self._screen.erase()
        self._screen.border(0)
        self._screen.addstr(4, 4, "Whoooch")
