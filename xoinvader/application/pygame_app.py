"""Pygame application class."""

import pygame

from xoinvader.application import Application
from xoinvader.render import Renderer


class PygameRenderer(Renderer):

    def clear(self):
        pass

    def render_objects(self, objects):
        pass

    def present(self):
        pass


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
        window = pygame.display.set_mode(resolution, flags, depth)
        renderer = PygameRenderer(window)

        super(PygameApplication, self).__init__(renderer)

        pygame.key.set_repeat(50, 50)

    def set_caption(self, caption: str, icontitle: str = ""):
        """Set window caption.

        :param caption: window caption
        :param icontitle: short title
        """

        pygame.display.set_caption(caption, icontitle)

    def stop(self):
        self._ioloop.add_callback(pygame.quit)
        super(PygameApplication, self).stop()
