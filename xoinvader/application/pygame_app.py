"""Pygame application class."""

import pygame

import xoinvader.pygame_utils
from xoinvader.application import Application


class PygameApplication(Application):
    """Pygame powered application backend.

    :param resolution: surface resolution
    :type resolution: (int, int)

    :param flags: collection of additional options
    :type flags: int (bitmask)

    :param depth: number of bits to use for color
    :type depth: int
    """

    def __init__(self, resolution=(0, 0), flags=0, depth=0):
        super(PygameApplication, self).__init__()

        self._screen = pygame.display.set_mode(resolution, flags, depth)
        self._clock = xoinvader.pygame_utils.get_clock()
        pygame.key.set_repeat(50, 50)

    def set_caption(self, caption, icontitle=""):
        """Set window caption.

        :param caption: window caption
        :type caption: str

        :param icontitle: short title
        :type icontitle: str
        """

        if self._screen:
            pygame.display.set_caption(caption, icontitle)

    def _tick(self):
        """Update clock."""
        self._state.events()
        self._state.update()
        self._state.render()

        pygame.display.update()
#        self._clock.tick(self._fps)

    def on_destroy(self):
        """Deinit pygame."""

        pygame.quit()

    def stop(self):
        self._pc.stop()

        def _stop():
            self._ioloop.add_callback(self._ioloop.stop)
            pygame.quit()

        self._ioloop.add_callback(_stop)

