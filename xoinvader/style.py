"""XOInvader styles."""

import curses

from eaf.meta import Singleton


class Style(metaclass=Singleton):
    """Container for style mappings."""

    def __init__(self):
        self._style = {
            "gui": {},
            "obj": {},
        }

    def init_styles(self, palette):
        """Initialize styles."""

        cpair = curses.color_pair

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
