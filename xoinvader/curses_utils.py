"""Curses helper module."""

import time
import curses

from six import add_metaclass

from xoinvader.common import Settings
from xoinvader.utils import Singleton


# pylint: disable=too-few-public-methods
@add_metaclass(Singleton)
class _Color(object):
    """Curses color mapping."""

    def __init__(self):
        self._color_names = [
            # User interface colors
            "ui_norm",
            "ui_yellow",
            # Damage panel colors
            "dp_blank",
            "dp_ok",
            "dp_middle",
            "dp_critical",
            "sh_ok",
            "sh_mid",
            # Weapon's gauge colors
            "blaster",
            "laser",
            "um",
        ]
        self._color_map = dict(
            zip(self._color_names, range(1, len(self._color_names) + 1))
        )

    @property
    def color_names(self):
        """Color names.

        :getter: yes
        :setter: no
        :type: list
        """
        return self._color_names

    def __getattr__(self, name):
        return self._color_map[name]


Color = _Color()  # pylint: disable=invalid-name


# TODO: rewrite this shit
@add_metaclass(Singleton)
class Style(object):
    """Container for style mappings."""

    def __init__(self):
        self._style = dict(
            gui={},
            obj={},
        )

    def init_styles(self, curses_module):
        """Initialize styles.

        :param module curses_module: curses module to initialize pairs
        """

        if Settings.system.no_color:
            for key in Color.color_names:
                self.gui[key] = None

        cpair = curses_module.color_pair

        self.gui["normal"] = cpair(Color.ui_norm) | curses.A_BOLD
        self.gui["yellow"] = cpair(Color.ui_yellow) | curses.A_BOLD
        self.gui["dp_blank"] = cpair(Color.dp_blank) | curses.A_BOLD
        self.gui["dp_ok"] = cpair(Color.dp_ok) | curses.A_BOLD
        self.gui["dp_middle"] = cpair(Color.dp_middle) | curses.A_BOLD
        self.gui["dp_critical"] = cpair(Color.dp_critical) | curses.A_BOLD
        self.gui["sh_ok"] = cpair(Color.sh_ok) | curses.A_BOLD
        self.gui["sh_mid"] = cpair(Color.sh_mid) | curses.A_BOLD

    def __getattr__(self, name):
        return self._style[name]


# TODO: refactor
def get_styles():
    """Return Style object."""
    return Style()


def init_curses_pairs(curses_module):
    """Init curses color pairs.

    :param module curses_module: curses module for pair initialization.
    """

    init_pair = curses_module.init_pair

    # User interface
    init_pair(Color.ui_norm, curses.COLOR_WHITE, curses.COLOR_BLACK)
    init_pair(Color.ui_yellow, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Damage panel
    init_pair(Color.dp_blank, curses.COLOR_BLACK, curses.COLOR_BLACK)
    init_pair(Color.dp_ok, curses.COLOR_GREEN, curses.COLOR_BLACK)
    init_pair(Color.dp_middle, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    init_pair(Color.dp_critical, curses.COLOR_RED, curses.COLOR_BLACK)
    init_pair(Color.sh_ok, curses.COLOR_BLUE, curses.COLOR_BLACK)
    init_pair(Color.sh_mid, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Weapons
    init_pair(Color.blaster, curses.COLOR_GREEN, curses.COLOR_BLACK)
    init_pair(Color.laser, curses.COLOR_BLACK, curses.COLOR_RED)
    init_pair(Color.um, curses.COLOR_MAGENTA, curses.COLOR_BLACK)


def create_window(ncols, nlines, begin_x=0, begin_y=0):
    """Initialize curses, colors, make and return window.

    :param ncols: number of columns
    :type ncols: integer

    :param nlines: number of lines
    :type nlines: integer

    :param begin_x: offset by x
    :type begin_x: integer

    :param begin_y: offset by y
    :type begin_y: integer

    :return: initialized curses window
    :rtype: `curses.Window`
    """
    curses.initscr()
    curses.start_color()

    if not Settings.system.no_color:
        init_curses_pairs(curses)

    # XXX: is this must be the first call of Style?
    Style().init_styles(curses)

    screen = curses.newwin(nlines, ncols, begin_x, begin_y)
    screen.keypad(0)
    screen.nodelay(1)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    return screen


def deinit_curses(screen):
    """Destroy window, deinit curses, make console changes back.

    :param screen: main screen
    :type screen: `curses.Window`
    """
    screen.nodelay(0)
    screen.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()


class Clock():
    """Object that helps to track time."""

    def __init__(self):
        self._mspf = 0
        self._previous_tick = 0
        self._current_tick = int(time.perf_counter())
        self._tick_time = 0

    def tick(self, framerate=0.0):
        """Update the clock.

        :param float framerate: expected FPS
        """

        self._previous_tick = self._current_tick
        self._current_tick = int(time.perf_counter())
        delta = self._current_tick - self._previous_tick

        self._mspf = int(1.0 / framerate * 1000.0) if framerate else delta

        time_s = (self._mspf - delta) / 1000.0
        time.sleep(time_s)
        self._tick_time = int(time.perf_counter()) - self._previous_tick
        return self._tick_time

    def get_fps(self):
        """Compute the clock framerate.

        :return: FPS
        :rtype: float
        """
        pass

    def get_time(self):
        """Time used in previous tick.

        :return: tick duration in milliseconds
        :rtype: int
        """
        return self._tick_time


def get_clock():
    """Helper for unification with other backends."""

    return Clock()
