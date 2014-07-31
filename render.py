import logging

from utils import log_format, date_format

logging.basicConfig(filename="render.log",
                    filemode="w",
                    format=log_format,
                    datefmt=date_format,
                    level=logging.DEBUG)

log = logging.getLogger(__name__)

class Renderer(object):
    def __init__(self):
        self.__objects = []


    def add_object(self, obj):
        self.__objects.append(obj)
        log.debug("add object {} \nObjects: {}".format(obj, self.__objects))


    def remove_object(self, obj):
        self.__objects.remove(obj)
        log.debug("del object {}".format(obj))


    def render_all(self, screen):
        log.debug("Rendering...")
        for obj in self.__objects:
            glob_pos, data_gen = obj.get_render_data()
            log.debug("Current object: {} \ng_pos: {}, d_gen: {}".format(obj, glob_pos, data_gen))
            for el in data_gen:
                pos, image, style = el
                log.debug("Pos: {}, char: {}, style: {}".format(pos, image, style))
                screen.addch(glob_pos.y + pos.y, glob_pos.x + pos.x, image)
        log.debug("Rendered succesfully")
