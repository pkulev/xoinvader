from collections import namedtuple


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
                yield (Point(x=x, y=y), image, self.__style)
