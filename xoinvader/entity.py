"""Basic Entity."""
# TODO: better module docstring
# pylint: disable=all

from xoinvader import constants
from xoinvader.common import Settings

if Settings.system.video_driver == constants.DRIVER_SDL:
    import pygame
else:
    class pygame(object):
        Rect = object

        @staticmethod
        def Surface(*args, **kwargs):
            pass


# TODO: document
# TODO: make clear interface
# TODO: component system
class Entity(pygame.Rect):
    """Base class for all game objects."""

    def __init__(self, pos, image=pygame.Surface((0, 0))):
        self._image = pygame.image.load(image)
        super(Entity, self).__init__((pos.x, pos.y), self._image.get_size())

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, path):
        self._image = pygame.image.load(path)

    def render(self, screen):
        screen.blit(self.image, self.topleft)  # self.move(*map(lambda x: -x, self.image.get_size())))
        pygame.draw.line(screen, (0, 255, 0), (400, 0), (400, 600), 1)
        pygame.draw.line(screen, (0, 255, 0), (0, 300), (800, 300), 1)
        pygame.draw.circle(screen, (0, 0, 255), (400, 300), 100, 1)
        pygame.draw.rect(screen, (255, 0, 0), (0, 0, 800, 600), 1)
