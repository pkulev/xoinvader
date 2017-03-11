"""Pygame application class."""

import pygame

from xoinvader.application import Application


# pylint: disable=no-member
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

    def stop(self):
        self._ioloop.add_callback(pygame.quit)
        super(PygameApplication, self).stop()
