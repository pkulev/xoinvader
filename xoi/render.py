from abc import ABCMeta, abstractmethod


class Renderable(object, metaclass=ABCMeta):
    @abstractmethod
    def get_render_data(self):
        """Renderable.get_render_data(None) -> (gpos_list, data_gen)

        Every renderable object must return tuple consist of:
        * gpos_list: list of every Surface's global positions (List of Points)
          Example: [Point(x=5, y=5), Point(x=10, y=10)]

        * data_gen: generator which yields tuple (lpos, image, style)
          Example: (Point(x=5, y=5), "*", curses.A_BOLD)
        """
        pass


    def remove_obsolete(self, pos):
        """Renderable.remove_obsolete(Point(int, int)) -> None

        Every renderable object must remove old bullets that places behind
        border (field for rendering).

        If object will never change its coordinates it may not implement this
        method.
        """
        pass


class Renderer(object):
    def __init__(self, border):
        self._objects = []
        self._border = border


    def add_object(self, obj):
        self._objects.append(obj)


    def remove_object(self, obj):
        self._objects.remove(obj)


    def render_all(self, screen):
        for obj in self._objects:
            gpos_list, data_gen = obj.get_render_data()

            for data in data_gen:
                for gpos in gpos_list:
                    lpos, image, style = data
                    cpos = gpos + lpos

                    if (cpos.x >= self._border.x or cpos.y >= self._border.y) or \
                       (cpos.x <= 0 or cpos.y <= 0):
                        obj.remove_obsolete(gpos)
                        continue

                    if style:
                        screen.addch(cpos.y, cpos.x, image, style)
                    else:
                        screen.addch(cpos.y, cpos.x, image)
