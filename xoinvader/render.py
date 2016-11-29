"""
    Module that renders graphics to screen.
"""


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
    for obj in objects:
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


# FIXME: DEPRECATED.
# * Make weapon shells as separate entities
# * Implement Compound Object Rendering Protocol
# * Use render_objects function for rendering scene.
class Renderer(object):
    """Handles collection of renderable objects, renders them to screen."""

    def __init__(self, border):
        self._objects = []
        self._border = border

    def add_object(self, obj):
        """Add renderable object."""
        self._objects.append(obj)
        self._objects.sort(key=lambda x: x.render_priority)

    def remove_object(self, obj):
        """Remove renderable object."""
        self._objects.remove(obj)

    def render_all(self, screen):
        """Render all renderable objects."""
        for obj in self._objects:
            gpos_list, data_gen = obj.get_render_data()

            for data in data_gen:
                for gpos in gpos_list:
                    lpos, image, style = data
                    cpos = gpos + lpos

                    if (cpos.x >= self._border.x or cpos.y >= self._border.y) \
                       or (cpos.x <= 0 or cpos.y <= 0):

                        obj.remove_obsolete(gpos)
                        continue

                    if style:
                        screen.addstr(cpos.y, cpos.x, image, style)
                    else:
                        screen.addstr(cpos.y, cpos.x, image)
