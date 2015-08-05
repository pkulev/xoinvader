"""MainMenuState-related input and event handlers."""


import os
import sys

from xoinvader.gui import TextWidget, MenuItemWidget
from xoinvader.keys import *
from xoinvader.state import State
from xoinvader.utils import Point
from xoinvader.common import Settings
from xoinvader.render import render_objects
from xoinvader.handlers import Handler
from xoinvader.curses_utils import deinit_curses


def exit_game_command(actor):
    deinit_curses(actor)
    sys.exit(os.EX_OK)


def to_ingame_command(actor):
    actor.owner.state = "InGameState"


class MainMenuInputHandler(Handler):
    def __init__(self, owner):
        super(MainMenuInputHandler, self).__init__(owner)

        self._command_map = {
            K_ESCAPE : to_ingame_command,
            K_R : exit_game_command
        }

    def handle(self):
        key = self._screen.getch()
        command = self._command_map.get(key)
        if command:
            if command is exit_game_command:
                command(self._screen)
            elif command is to_ingame_command:
                command(self._owner)
            else:
                command(self._actor)


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

        self._objects = [TextWidget(Point(4,4), "Whoooch"),
                         MenuItemWidget(Point(10, 10), "First menu item"),
                         MenuItemWidget(Point(10, 11), "Second menu item")]
#        Settings.renderer.add_object(self._objects[0])
        self._objects[1].select()
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
        for o in self._objects:
            o.update()

    def render(self):
        self._screen.erase()
        self._screen.border(0)
        render_objects(self._objects, self._screen)
