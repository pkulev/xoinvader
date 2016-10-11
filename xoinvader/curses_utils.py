"""Curses helper module."""

import time
import curses

from xoinvader.common import Settings
from xoinvader.utils import Singleton


class _Color(object, metaclass=Singleton):
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
        self._color_map = dict(zip(self._color_names,
                                   range(1, len(self._color_names) + 1)))

    def __getattr__(self, name):
        return self._color_map[name]


Color = _Color()  # noqa


# TODO: rewrite this shit
class Style(object, metaclass=Singleton):
    """Container for style mappings."""

    def __init__(self):
        self._style = dict(
            gui={},
            obj={},
        )

    def init_styles(self, curses):
        """Initialize styles.

        :param curses: curses module to initialize pairs
        :type curses: module
        """

        if Settings.system.no_color:
            for key in Color._color_names:
                self.gui[key] = None

        self.gui["normal"] = curses.color_pair(Color.ui_norm)          \
            | curses.A_BOLD
        self.gui["yellow"] = curses.color_pair(Color.ui_yellow)        \
            | curses.A_BOLD

        self.gui["dp_blank"] = curses.color_pair(Color.dp_blank)       \
            | curses.A_BOLD
        self.gui["dp_ok"] = curses.color_pair(Color.dp_ok)             \
            | curses.A_BOLD
        self.gui["dp_middle"] = curses.color_pair(Color.dp_middle)     \
            | curses.A_BOLD
        self.gui["dp_critical"] = curses.color_pair(Color.dp_critical) \
            | curses.A_BOLD
        self.gui["sh_ok"] = curses.color_pair(Color.sh_ok)             \
            | curses.A_BOLD
        self.gui["sh_mid"] = curses.color_pair(Color.sh_mid)           \
            | curses.A_BOLD

    def __getattr__(self, name):
        return self._style[name]


# TODO: refactor
def get_styles():
    """Return Style object."""
    return Style()


def init_curses_pairs(curses):

    # User interface
    curses.init_pair(Color.ui_norm, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(Color.ui_yellow, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Damage panel
    curses.init_pair(Color.dp_blank, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(Color.dp_ok, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(Color.dp_middle, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(Color.dp_critical, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(Color.sh_ok, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(Color.sh_mid, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Weapons
    curses.init_pair(Color.blaster, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(Color.laser, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(Color.um, curses.COLOR_MAGENTA, curses.COLOR_BLACK)


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
