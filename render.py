from abc import ABCMeta, abstractmethod

from utils import create_logger


log = create_logger(__name__, "render.log")


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


class Renderer(object):
    def __init__(self):
        self._objects = []


    def add_object(self, obj):
        self._objects.append(obj)
        log.debug("add object {} \nObjects: {}".format(obj, self._objects))


    def remove_object(self, obj):
        self._objects.remove(obj)
        log.debug("del object {}".format(obj))


    def render_all(self, screen):
        log.debug("Rendering...")

        for obj in self._objects:
            gpos_list, data_gen = obj.get_render_data()
            log.debug("Current object: {} \ng_pos: {}, d_gen: {}".format(obj, gpos_list, data_gen))
#FIX
            for gpos in gpos_list:
                for data in data_gen:
                    lpos, image, style = data
                    cpos = gpos + lpos
                    log.debug("Coords [global: {}; local: {}; sum: {}]".format(gpos, lpos, cpos))
                    log.debug("char: {}, style: {}".format(image, style))

                    if style:
                        screen.addch(cpos.y, cpos.x, image, style)
                    else:
                        screen.addch(cpos.y, cpos.x, image)
        log.debug("Rendered succesfully")
