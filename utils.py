from collections import namedtuple
from itertools import chain

__all__ = ['Event', 'Point', 'Surface']


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


class InfList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._index = 0


    def next(self):
        self._index = self._index + 1 if self._index < len(self)-1 else 0
        return self[self._index]

    def prev(self):
        self._index = self._index - 1 if self._index > 0 else len(self)-1
        return self[self._index]

if __name__ == "__main__":
    c1 = InfList([1,2,3])
    print(c1)
    for _ in range(4):
        print(c1.next())

