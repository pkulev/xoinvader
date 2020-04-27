"""Curses helper module."""

import time
import curses

from xoinvader.common import Settings
from xoinvader.utils import Singleton


class PairAlreadyRegistered(Exception):

    def __init__(self, attr, value):
        super().__init__(f"Pair with {attr} = {value} already registered."
                         " You can use force=True to redefine it.")


class Palette:
    """Palette abstraction for curses color pairs.

    Has some predefined constants (taken directly from curses),

    Pass to init initial palette as list of tuples of 3 elements: name,
    foreground color, background color:

    palette = Palette([
        ("normal", Palette.COLOR_WHITE, Palette.COLOR_BLACK),
        ("error", Palette.COLOR_RED, Palette.COLOR_BLACK),
    ])
    """

    COLOR_BLACK = curses.COLOR_BLACK
    COLOR_BLUE = curses.COLOR_BLUE
    COLOR_CYAN = curses.COLOR_CYAN
    COLOR_GREEN = curses.COLOR_GREEN
    COLOR_MAGENTA = curses.COLOR_MAGENTA
    COLOR_RED = curses.COLOR_RED
    COLOR_WHITE = curses.COLOR_WHITE
    COLOR_YELLOW = curses.COLOR_YELLOW

    A_BOLD = curses.A_BOLD

    def __init__(self, palette=None):
        self.palette = {}

        idx = 1
        for name, fg, bg in palette or []:
            self.add_pair(idx, name, fg, bg, init=False)
            idx += 1

    def add_pair(self, idx, name, fg, bg, force=False, init=True):
        if name in self.palette and not force:
            raise PairAlreadyRegistered("name", name)

        if (
            idx in [pair["idx"] for pair in self.palette.values()]
            and not force
        ):
            raise PairAlreadyRegistered("idx", idx)

        self.palette[name] = {
            "idx": idx,
            "fg": fg,
            "bg": bg,
        }

        if init:
            curses.init_pair(idx, fg, bg)

    def init_colors(self):
        if not curses.has_colors():
            return

        for pair in self.palette.values():
            curses.init_pair(pair["idx"], pair["fg"], pair["bg"])

    def add_style(self, name, attrs):
        pass

    @property
    def pair_names(self):
        return sorted(self.palette, key=lambda it: self[it]["idx"])

    def __getattr__(self, name):
        return self.palette[name]["idx"]


palette = Palette([
    # User interface colors
    ("ui_norm", Palette.COLOR_WHITE, Palette.COLOR_BLACK),
    ("ui_yellow", Palette.COLOR_YELLOW, Palette.COLOR_BLACK),
    # Damage panel colors
    ("dp_blank", Palette.COLOR_BLACK, Palette.COLOR_BLACK),
    ("dp_ok", Palette.COLOR_GREEN, Palette.COLOR_BLACK),
    ("dp_middle", Palette.COLOR_YELLOW, Palette.COLOR_BLACK),
    ("dp_critical", Palette.COLOR_RED, Palette.COLOR_BLACK),
    ("sh_ok", Palette.COLOR_BLUE, Palette.COLOR_BLACK),
    ("sh_mid", Palette.COLOR_CYAN, Palette.COLOR_BLACK),
    # Weapon's charge colors
    ("blaster", Palette.COLOR_GREEN, Palette.COLOR_BLACK),
    ("laser", Palette.COLOR_BLACK, Palette.COLOR_RED),
    ("um", Palette.COLOR_MAGENTA, Palette.COLOR_BLACK),
])

# TODO: rewrite this shit
class Style(metaclass=Singleton):
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

        cpair = curses_module.color_pair

        self.gui["normal"] = cpair(palette.ui_norm) | curses.A_BOLD
        self.gui["yellow"] = cpair(palette.ui_yellow) | curses.A_BOLD
        self.gui["dp_blank"] = cpair(palette.dp_blank) | curses.A_BOLD
        self.gui["dp_ok"] = cpair(palette.dp_ok) | curses.A_BOLD
        self.gui["dp_middle"] = cpair(palette.dp_middle) | curses.A_BOLD
        self.gui["dp_critical"] = cpair(palette.dp_critical) | curses.A_BOLD
        self.gui["sh_ok"] = cpair(palette.sh_ok) | curses.A_BOLD
        self.gui["sh_mid"] = cpair(palette.sh_mid) | curses.A_BOLD

    def __getattr__(self, name):
        return self._style[name]


# TODO: refactor
def get_styles():
    """Return Style object."""
    return Style()


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

    palette.init_colors()
    Style().init_styles(curses)

    screen = curses.newwin(nlines, ncols, begin_x, begin_y)
    screen.keypad(0)
    screen.nodelay(1)
    curses.noecho()
    curses.cbreak()
    try:
        curses.curs_set(0)
    except curses.error:
        # old terminals may have no cursor modes support
        pass

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
    try:
        curses.curs_set(1)
    except curses.error:
        # old terminals may have no cursor modes support
        pass
    curses.endwin()


class Clock:
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
