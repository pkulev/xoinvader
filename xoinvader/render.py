"""
    Module that renders graphics to screen.
"""

from operator import attrgetter

from xoinvader.utils import Point


class Renderable(object):
    """Base for renderable objects."""

    render_priority = 0

    def get_render_data(self):
        """Renderable.get_render_data(None) -> (gpos_list, data_gen)

        Every renderable object must return tuple consist of:
            * gpos_list: list of every Surface's global positions [Points]
            Example: [Point(x=5, y=5), Point(x=10, y=10)]

            * data_gen: generator which yields tuple (lpos, image, style)
            Example: (Point(x=5, y=5), "*", curses.A_BOLD)
        """
        raise NotImplementedError

    def remove_obsolete(self, pos):
        """Renderable.remove_obsolete(Point(int, int)) -> None

        Every renderable object must remove old bullets that places behind
        border (field for rendering).

        If object will never change its coordinates it may not implement this
        method.
        """
        pass


def render_objects(objects, screen):
    """Render all renderable objects."""
    border = Point(*screen.getmaxyx()[::-1])

    # TODO: Move sorting to some kind of object manager
    # Must be sorted on adding objects
    for obj in sorted(objects, key=attrgetter("render_priority")):
        gpos_list, data_gen = obj.get_render_data()

        for data in data_gen:
            for gpos in gpos_list:
                lpos, image, style = data
                cpos = gpos + lpos

                if (cpos.x >= border.x or cpos.y >= border.y) \
                   or (cpos.x <= 0 or cpos.y <= 0):

                    obj.remove_obsolete(gpos)
                    continue

                if style:
                    screen.addstr(cpos.y, cpos.x, image, style)
                else:
                    screen.addstr(cpos.y, cpos.x, image)
