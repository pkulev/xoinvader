from collections import namedtuple


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


Event = namedtuple("Event", ["type", "val"])
