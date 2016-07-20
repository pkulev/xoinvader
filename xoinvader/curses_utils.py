"""Create and destroy curses windows."""


import curses


class _Color(object):
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

Color = _Color()


# TODO: rewrite this shit
class Style(object):
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

style = Style()


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
