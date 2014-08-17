from abc import ABCMeta, abstractmethod

from utils import create_logger


log = create_logger(__name__, "render.log")


class Renderable(object, metaclass=ABCMeta):
    @abstractmethod
    def get_render_data(self):
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
            glob_pos, data_gen = obj.get_render_data()
            log.debug("Current object: {} \ng_pos: {}, d_gen: {}".format(obj, glob_pos, data_gen))
#FIX
            for global_pos in glob_pos:
                for el in data_gen:
                    pos, image, style = el
                    log.debug("Pos: {}, char: {}, style: {}".format(pos, image, style))

                    if style:
                        screen.addch(glob_pos.y + pos.y, glob_pos.x + pos.x, image, style)
                    else:
                        screen.addch(glob_pos.y + pos.y, glob_pos.x + pos.x, image)
        log.debug("Rendered succesfully")
