import logging
import time
import threading

from collections import namedtuple


log_format = "[%(asctime)s] %(levelname)s: %(message)s"
date_format = "%m/%d/%Y %I:%M:%S %p"


def create_logger(lname, fname, fmode="w", level=logging.DEBUG):
    logging.basicConfig(filename=fname,
                        filemode=fmode,
                        format=log_format,
                        datefmt=date_format,
                        level=level)
    return logging.getLogger(lname)


Event = namedtuple("Event", ["type", "val"])


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __repr__(self):
        return "Point(x={}, y={})".format(self._x, self._y)


    __str__ = __repr__


    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)


    @property
    def x(self):
        return self._x


    @x.setter
    def x(self, val):
        self._x = val


    @property
    def y(self):
        return self._y


    @y.setter
    def y(self, val):
        self._y = val


class Surface(object):
    """image is list of lists of char:
        rocket
        [
         ["^"],     ^
         ["|"],     |
         ["*"] ]    *

        ship
        [
         [" "," ","O"," "," "],           O
         ["<","=","H","=",">"],         <=H=>
         [" ","*"," ","*"," "] ]         * *
    """

    def __init__(self, image, style=None, orientation='up'):
        self._image = image if orientation == 'up' else image[::-1]
        self._width = max([len(l) for l in self._image])
        self._height = len(self._image)
        self._style = style


    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width


    def get_image(self):
        for y, row in enumerate(self._image):
            for x, image in enumerate(row):
                yield (Point(x=x, y=y), image, self._style[y][x] if self._style else None)


class Color:
    #user interface
    ui_norm   = 1
    ui_yellow = 2
    #damage panel
    dp_blank    = 3
    dp_ok       = 4
    dp_middle   = 5
    dp_critical = 6
    sh_ok       = 7
    sh_mid      = 8
    #weapons
    blaster = 9
    laser   = 10
    um      = 11


class Layout(object):
    def __init__(self, config=None):
        self._field = {}
        self._gui = {}


    def init_layout(self):
        self._field["border"] = Point(x=90, y=34)
        self._field["spaceship"] = Point(x=self._field["border"].x // 2,
                                         y=self._field["border"].y - 1)

        self._gui["hbar"] = Point(x=2 , y=self._field["border"].y - 1)
        self._gui["sbar"] = Point(x=22, y=self._field["border"].y - 1)
        self._gui["wbar"] = Point(x=self._field["border"].x - 14,
                                  y=self._field["border"].y - 1)

        return self


    @property
    def field(self):
        return self._field


    @property
    def gui(self):
        return self._gui


class InfList(list):
    """Infinite list container"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._index = 0


    def current(self):
        return self[self._index]


    def next(self):
        self._index = (self._index + 1) % len(self)
        return self[self._index]


    def prev(self):
        self._index = (self._index - 1) % len(self)
        return self[self._index]
