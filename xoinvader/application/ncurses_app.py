"""NCurses application class."""

import os

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
        """Stop the loop."""

        xoinvader.curses_utils.deinit_curses(self._screen)
        super(CursesApplication, self).stop()

    def loop(self):
        """Start main application loop.

        :return: execution status code
        :rtype: int
        """
        if self._state:
            self._running = True
        else:
            raise AttributeError("There is no avalable state.")

        while self._running:
            try:
                self._state.events()
                self._state.update()
                self._state.render()

                self._tick()
            except KeyboardInterrupt:
                pass

        return os.EX_OK

    def _tick(self):
        """Update clock."""
        self._clock.tick(self._fps)
