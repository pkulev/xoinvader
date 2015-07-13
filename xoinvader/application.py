import time

# ?!
from xoinvader.gui import WeaponWidget, Bar
from xoinvader.ship import GenericXEnemy, Playership
from xoinvader.utils import Point
from xoinvader.render import Renderer
from xoinvader.common import Settings
from xoinvader.handlers import EventHandler


from xoinvader.curses_utils import create_curses_window


class Application(object):
    def __init__(self, startup_args={}):
        self._update_settings_from_args(startup_args)
        self_screen = create_curses_window(None)
        self._state = None
        self._states = {}

        # Ms per frame
        self._mspf = 16

    def _update_settings_from_args(self, args):
        pass

    def create_window(self):
        pass

    def exit(self):
        pass

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, name):
        if name in self._states:
            self._state = self._states[name]
        else:
            raise KeyError("No such state {0}.".format(name))

    def register_state(self, state):
        """Add new state and initiate it with owner."""
        name = state.__class__.__name__
        self._states[name] = state(self)
        if len(self._states) == 1:
            self._state = self._states[name]

    def loop(self):
        while True:
            start_time = time.perf_counter()

            self._state.events()
            self._state.update()
            self._state.render()

            finish_time = time.perf_counter()
            delta = finish_time - start_time
            if delta <= self._mspf:
                time.sleep((self._mspf - delta) / 1000.0)
            else:
                pass # Log FPS drawdowns.
