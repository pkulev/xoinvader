"""Rendering routines."""


from abc import ABCMeta, abstractmethod
from typing import List


class Renderable(metaclass=ABCMeta):
    """Base for renderable objects.

    .. class-variables::

    * compound (bool): if object consists of other renderables

    * render_priority (int): priority for renderer, greater -> rendered later

    * draw_on_border (bool): allow or not drawing on border
    if not allowed - renderer will send remove_obsolete signal to object
    """

    compound = False
    render_priority = 0
    draw_on_border = False

    @abstractmethod
    def get_render_data(self):
        """Renderable.get_render_data(None) -> (gpos_list, data_gen)

        Every renderable object must return tuple consist of:
            * gpos_list: list of every Surface's global positions [Points]
            Example: [Point(x=5, y=5), Point(x=10, y=10)]

            * data_gen: generator which yields tuple (lpos, image, style)
            Example: (Point(x=5, y=5), "*", curses.A_BOLD)
        """
        pass

    @classmethod
    def type(cls):
        return cls.__name__

    def remove_obsolete(self, pos):
        """Renderable.remove_obsolete(Point(int, int)) -> None

        Every renderable object must remove old bullets that places behind
        border (field for rendering).

        If object will never change its coordinates it may not implement this
        method.
        """
        pass


class Renderer:
    """Base renderer class. Instance can be used as dummy renderer."""

    def __init__(self, screen):
        self._screen = screen

    @property
    def screen(self):
        return self._screen

    def clear(self):
        pass

    def render_objects(self, objects: List[Renderable]):
        pass

    def present(self):
        pass
