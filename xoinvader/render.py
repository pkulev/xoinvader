"""Rendering routines."""


from abc import ABCMeta, abstractmethod
from operator import attrgetter

from six import add_metaclass

from xoinvader.common import Settings
from xoinvader.utils import Point


INVISIBLE_SYMBOLS = " "
"""Symbols that renderer must not render on the screen."""


@add_metaclass(ABCMeta)
class Renderable(object):
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


# TODO: [advanced-render]
# * use render for curses and SDL windows
def render_objects(objects, screen):
    """Render all renderable objects.

    :param collections.Iterable objects: objects to render
    :param curses._Window screen: curses screen
    """
    border = Point(*screen.getmaxyx()[::-1])

    # TODO: Move sorting to some kind of object manager
    # Must be sorted on adding objects
    for obj in sorted(objects, key=attrgetter("render_priority")):
        gpos_list, data_gen = obj.get_render_data()

        for data in data_gen:
            for gpos in gpos_list:
                lpos, image, style = data
                cpos = (gpos + lpos)[int]

                if (
                        (cpos.x >= border.x - 1 or cpos.y >= border.y - 1) or
                        (cpos.x <= 0 or cpos.y <= 0)
                ) and not obj.draw_on_border:
                    obj.remove_obsolete(gpos)
                    continue

                if image in INVISIBLE_SYMBOLS:
                    continue

                if style:
                    screen.addstr(
                        cpos.y, cpos.x,
                        image.encode(Settings.system.encoding), style)
                else:
                    screen.addstr(cpos.y, cpos.x, image)
