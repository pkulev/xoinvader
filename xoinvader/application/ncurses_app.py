"""NCurses application class."""

import xoinvader.curses_utils
from xoinvader.common import Settings
from xoinvader.application import Application


class CursesApplication(Application):
    """Curses powered application class, default fallback backend.

    :param dict startup_args: arguments for passing to game settings
    """

    def __init__(self):
        super(CursesApplication, self).__init__()

        self._screen = xoinvader.curses_utils.create_window(
            ncols=Settings.layout.field.border.x,
            nlines=Settings.layout.field.border.y)

        self._clock = xoinvader.curses_utils.get_clock()

    def set_caption(self, caption, icontitle=None):
        """Set window caption.

        :param caption: window caption
        :type caption: str

        :param icontitle: short title
        :type icontitle: str
        """
        # Maybe we can update text via terminal API
        pass

    def stop(self):
        self._ioloop.add_callback(
            lambda: xoinvader.curses_utils.deinit_curses(self._screen))
        super(CursesApplication, self).stop()
