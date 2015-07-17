""" Provides main game-specific states. """

import curses

from xoinvader.state import State
from xoinvader.common import Settings
from xoinvader.handlers import InGameEventHandler


class InGameState(State):
    def __init__(self, owner):
        super(InGameState, self).__init__(owner)
        self._objects = []
        self._screen = self._owner.screen
        self._actor = self._owner.actor
        self.add_object(self._actor)

        self._events = InGameEventHandler(self)

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
