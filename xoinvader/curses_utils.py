"""Create and destroy curses windows."""

import curses
from xoinvader.utils import Color


def create_curses_window(ncols, nlines, begin_x=0, begin_y=0):
    """Initialize curses, colors, make and return window."""

    curses.initscr()
    curses.start_color()

    # User interface
    curses.init_pair(Color.ui_norm, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(Color.ui_yellow, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Damage panel
    curses.init_pair(Color.dp_blank, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(Color.dp_ok, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(Color.dp_middle, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(Color.dp_critical, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(Color.sh_ok, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(Color.sh_mid, curses.COLOR_WHITE, curses.COLOR_CYAN)

    # Weapons
    curses.init_pair(Color.blaster, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(Color.laser, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(Color.um, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    screen = curses.newwin(nlines, ncols, begin_x, begin_y)
    screen.keypad(1)
    screen.nodelay(1)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    return screen


def deinit_curses(screen):
    """Destroy window, deinit curses, make console changes back."""

    screen.nodelay(0)
    screen.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()
