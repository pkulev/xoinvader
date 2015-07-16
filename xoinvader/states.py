""" Provides main game-specific states. """

import curses

from xoinvader.state import State
from xoinvader.common import Settings
from xoinvader.handlers import EventHandler

from xoinvader.handlers import K_ESCAPE, TestCommand


class InGameState(State):
    def __init__(self, owner):
        super(InGameState, self).__init__(owner)
        self._objects = []
        self._screen = self._owner.screen
        self._actor = self._owner.actor
        self.add_object(self._actor)

        self._events = EventHandler(self)

        # To test state changing
        self._events.input_handler._button_map[K_ESCAPE] = TestCommand()

    def add_object(self, obj):
        self._objects.append(obj)

    def handle_event(self, event):
        raise NotImplementedError

    def events(self):
        # for event in xoinvader.messageBus.get():
        self._events.handle()

    def update(self):
        for obj in self._objects:
            obj.update()

    def render(self):
        self._screen.erase()
        self._screen.border(0)
        self._screen.addstr(0, 2, "Score: %s " % 0)
        self._screen.addstr(0, Settings.layout.field.edge.x // 2 - 4,
                "XOinvader", curses.A_BOLD)

        Settings.renderer.render_all(self._screen)
        self._screen.refresh()

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
        self._events = EventHandler(self)

#    def register_menu_item(self, caption, item_action_list):
    def events(self):
        self._events.handle()

    def update(self):
        pass

    def render(self):
        self._screen.erase()
        self._screen.border(0)
        self._screen.addstr(4, 4, "Whoooch")
