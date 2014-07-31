from collections import namedtuple


log_format = "[%(asctime)s] %(levelname)s: %(message)s"
date_format = "%m/%d/%Y %I:%M:%S %p"

Event = namedtuple("Event", ["type", "val"])


class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __repr__(self):
        return "Point(x={}, y={})".format(self.__x, self.__y)


    @property
    def x(self):
        return self.__x


    @x.setter
    def x(self, val):
        self.__x = val


    @property
    def y(self):
        return self.__y


    @y.setter
    def y(self, val):
        self.__y = val


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

    def __init__(self, image, style=None):
        self.__image = image
        self.__width = max([len(l) for l in image])
        self.__height = len(self.__image)
        self.__style = style


    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width


    def get_image(self):
        for y, row in enumerate(self.__image):
            for x, image in enumerate(row):
                yield (Point(x=x, y=y), image, self.__style[y][x] if self.__style else None)


class Color:
    #user interface
    ui_norm  = 1
    ui_yellow = 2
    #damage panel
    dp_blank    = 3
    dp_ok       = 4
    dp_middle   = 5
    dp_critical = 6
    #weapons
    blaster = 7
    laser   = 8
    um      = 9


class Layout(object):
    def __init__(self, config=None):
        self.__field = {}
        self.__gui = {}

    def init_layout(self):
        self.__field["border"] = Point(x=80, y=24)
        self.__field["spaceship"] = Point(x=self.__field["border"].x // 2,
                                          y=self.__field["border"].y - 1)

        self.__gui["hbar"] = Point(x=2 , y=self.__field["border"].y - 1)
        self.__gui["sbar"] = Point(x=22, y=self.__field["border"].y - 1)

        return self


    @property
    def field(self):
        return self.__field


    @property
    def gui(self):
        return self.__gui
