import time
import curses

# ?!
from xoinvader.gui import WeaponWidget, Bar
from xoinvader.ship import GenericXEnemy, Playership
from xoinvader.utils import Point
from xoinvader.render import Renderer
from xoinvader.common import Settings
from xoinvader.settings import dotdict
from xoinvader.curses_utils import create_curses_window, style

class _Application(object):
    def __init__(self, startup_args={}):
        self._update_settings_from_args(startup_args)
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
        name = state.__name__
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



class Application(_Application):
    def __init__(self, startup_args={}):
        super(Application, self).__init__(startup_args)
        self._update_settings_from_args(startup_args)
        self.screen = create_curses_window(
                ncols=Settings.layout.field.border.x,
                nlines=Settings.layout.field.border.y)

        # Ms per frame
        self._mspf = 16

        style.init_styles(curses)
        Settings.renderer = Renderer(Settings.layout.field.border)

        self.actor = Playership(Settings.layout.field.player,
                Settings.layout.field.edge, Settings)

        Settings.renderer.add_object(self.actor)

        self.enemy = GenericXEnemy(Point(x=15, y=3), Settings.layout.field.edge,
                Settings)

        Settings.renderer.add_object(self.enemy)

        # GUI style mapping
        self.gui = dotdict(
                hull=Bar(pos=Settings.layout.gui.bar.health, prefix="Hull: ",
                  stylemap={
                      lambda val: 70.0 <= val <= 100.0 : style.gui["dp_ok"],
                      lambda val: 35.0 <= val < 70.0 : style.gui["dp_middle"],
                      lambda val: 0.0 <= val < 35.0 : style.gui["dp_critical"]
                  }),
            shield=Bar(pos=Settings.layout.gui.bar.shield, prefix="Shield: ",
                    stylemap={
                        lambda val: 70.0 <= val <= 100.0 : style.gui["sh_ok"],
                        lambda val: 35.0 <= val < 70.0 : style.gui["sh_mid"],
                        lambda val: 0.0 <= val < 35.0 : style.gui["dp_critical"]
                    }),
            weapon=Bar(pos=Settings.layout.gui.bar.weapon,
                    stylemap={
                        lambda val: 0.0 <= val <= 100.0 : style.gui["dp_ok"]
                    }),
            weapon_info=WeaponWidget(Settings.layout.gui.info.weapon,
                                  self.actor.get_weapon_info)
        )

        for gui_object in self.gui.values():
            Settings.renderer.add_object(gui_object)
