"""Various useful tools."""

import copy
import datetime
import logging
import time
try:
    time.perf_counter
except AttributeError:
    time.perf_counter = time.time


LOG_FORMAT = (
    "[%(asctime)s] %(levelname)-8s %(name)s[%(funcName)s]:%(lineno)s:  "
    "%(message)s"
)
"""Log message format string."""

TIME_FORMAT = "%H:%M:%S,%03d"
"""Log time format string."""

DATE_FORMAT = "%Y-%m-%d %a"
"""Initial log entry date format string."""


def setup_logger(name, debug=False, msgfmt=None, timefmt=None):
    """Setup logger with linked log file.

    Do not use it for getting logger, call this once on init,
    then use logging.getLogger(__name__) for getting actual logger.

    :param str name: logger relative name
    :param bool debug: debug mode
    :param str msgfmt: message format
    :param str timefmt: time format

    :return: prepared logger instance
    :rtype: `logging.Logger`
    """

    logger = logging.getLogger(name)
    logger.propagate = False
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
    handler = logging.FileHandler("{0}.log".format(name))
    handler.setLevel(level)
    formatter = logging.Formatter(msgfmt or LOG_FORMAT, timefmt or TIME_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    date = datetime.date.today().strftime(DATE_FORMAT)
    logger.info("*** (%s) Initializing XOInvader ***", date)

    return logger


def isclose(left, right, rel_tol=1e-9, abs_tol=0.0):
    """Check if values are approximately equal.

    :param int,float left: first value
    :param int,float right: second value
    :param float rel_tol: relative tolerance (amount of error allowed)
    :param float abs_tol: minimum absolute tolerance level
    """
    approx = max(rel_tol * max(abs(left), abs(right)), abs_tol)
    return abs(left - right) <= approx


class dotdict(dict):  # pylint: disable=invalid-name
    """Container for dot elements access."""

    def __init__(self, *args, **kwargs):
        super(dotdict, self).__init__(*args, **kwargs)
        self.__dict__ = self
        self._wrap_nested()

    def _wrap_nested(self):
        """Wrap nested dicts for deep dot access."""

        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = dotdict(value)

    def fullcopy(self):
        """Return full copy of internal structure as dotdict.

        :return :class:`xoinvader.utils.dotdict`: full copy
        """

        return dotdict(copy.deepcopy(self))


# pylint: disable=too-few-public-methods
class Point(object):
    """3D point representation.

    :param x: x coordinate
    :type x: integer

    :param y: y coordinate
    :type y: integer

    :param z: z coordinate
    :type z: integer

    :return: Point instance
    :rtype: `xoinvader.utils.Point`
    """

    __slots__ = ["x", "y", "z"]

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "Point(x={0}, y={1}, z={2})".format(self.x, self.y, self.z)

    __str__ = __repr__

    @staticmethod
    def _value_error(operation, value):
        """Raise ValueError with appropriate message."""

        return ValueError(
            "Wrong type to {0} {1}: {2}".format(operation, type(value), value))

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Point(
                x=self.x + other,
                y=self.y + other,
                z=self.z + other)

        elif isinstance(other, Point):
            return Point(
                x=self.x + other.x,
                y=self.y + other.y,
                z=self.z + other.z)
        else:
            raise self._value_error("add", other)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self.__add__(-other)
        elif isinstance(other, Point):
            return Point(
                x=self.x - other.x,
                y=self.y - other.y,
                z=self.z - other.z)
        else:
            raise self._value_error("sub", other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Point(
                x=self.x * other,
                y=self.y * other,
                z=self.z * other)
        # What for point
        else:
            raise self._value_error("mul", other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Point(
                x=self.x / other,
                y=self.y / other,
                z=self.z / other)
        else:
            raise self._value_error("div", other)

    __div__ = __truediv__

    def __eq__(self, other):
        if not isinstance(other, Point):
            raise self._value_error("eq", other)

        return self.x == other.x and self.y == other.y and self.z == other.z

    def __getitem__(self, cons):
        """Cast Point to selected type.

        :param type cons: type to cast to

        :return Point: with casted members
        """

        return Point(
            x=cons(self.x),
            y=cons(self.y),
            z=cons(self.z))


class Surface(object):
    """Representation of graphic objects.

    :param image: source for building image
    :type image: [ [char] ]

    .. note:: add building from string

    :param style: source for building styled image
    :type style: [ [integer(curses constant)] ]

    :return: Surface instance
    :rtype: `xoinvader.utils.Surface`
    """

    # Example:
    #    rocket
    #    [
    #     ["^"],     ^
    #     ["|"],     |
    #     ["*"] ]    *

    #    ship
    #    [
    #     [" "," ","O"," "," "],           O
    #     ["<","=","H","=",">"],         <=H=>
    #     [" ","*"," ","*"," "] ]         * *

    __slots__ = ["_image", "_width", "_height", "_style"]

    def __init__(self, image, style=None):
        self._image = image
        self._width = max([len(l) for l in self._image])
        self._height = len(self._image)
        self._style = style

    @property
    def height(self):
        """Height of the surface.

        :getter: yes
        :setter: no
        :type: integer
        """
        return self._height

    @property
    def width(self):
        """Width of the surface.

        :getter: yes
        :setter: no
        :type: integer
        """
        return self._width

    @property
    def raw(self):
        """Raw image content.

        :getter: yes
        :setter: no
        :type: list
        """
        return self._image

    def get_image(self):
        """Image generator. Allows to renderers render Surfaces.

        :return: image generator
        :rtype: generator(`xoinvader.utils.Point`, string, integer)
        """
        for y, row in enumerate(self._image):
            for x, image in enumerate(row):
                yield (
                    Point(x=x, y=y), image,
                    self._style[y][x] if self._style else None
                )


class InfiniteList(list):
    """Infinite list container."""

    def __init__(self, *args, **kwargs):
        super(InfiniteList, self).__init__(*args, **kwargs)
        self._index = 0

    def current(self):
        """Get current element.

        :return: current element
        :rtype: object
        """
        return self[self._index]

    def next(self):
        """Get next element.

        :return: next element
        :rtype: object
        """
        try:
            self._index = (self._index + 1) % len(self)
        except ZeroDivisionError:
            raise IndexError("List is empty.")
        return self[self._index]

    def prev(self):
        """Get previous element.

        :return: previous element
        :rtype: object
        """
        try:
            self._index = (self._index - 1) % len(self)
        except ZeroDivisionError:
            raise IndexError("List is empty.")
        return self[self._index]


class Timer(object):
    """Simple timer, calls callback when time's up. Doesn't have own loop."""

    def __init__(self, end_time, func):
        self._end = float(end_time)
        self._func = func
        self._start = time.perf_counter()
        self._current = self._start
        self._running = False

    def _tick(self):
        """Refresh counter."""
        if self.running:
            self._current = time.perf_counter()

    def _time_is_up(self):
        """return is it time to fire fuction or not.

        :return: time is up
        :rtype: boolean
        """
        return self._current - self._start >= self._end

    def start(self):
        """Start timer."""
        self._running = True
        self._start = time.perf_counter()
        self._current = time.perf_counter()

    def stop(self):
        """Stop timer."""
        self._running = False

    def restart(self):
        """Restart timer."""
        self._start = time.perf_counter()
        self._current = self._start
        self.start()

    def reset(self):
        """Reset timer."""
        self._running = False
        self._start = 0
        self._current = 0

    def update(self):
        """Public method for using in loops."""
        if not self.running:
            return

        # Timer's accuracy depends on owner's loop
        self._tick()
        if self._time_is_up() and self.running:
            self._func()
            self.stop()

    @property
    def running(self):
        """Is timer running or not.

        :getter: yes
        :setter: no
        :type: boolean
        """
        return self._running

    def get_elapsed(self):
        """Elapsed time from start.

        :return: elapsed time
        :rtype: float
        """
        return self._current - self._start

    def get_remaining(self):
        """Remaining time to fire callback.

        :return: remaining time
        :rtype: float
        """
        return self._end - self.get_elapsed()

    def fire_function(self):
        """Call stored callback."""
        self._func()


class Singleton(type):
    """Singleton metaclass."""

    _instances = {}

    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwds)
        return cls._instances[cls]
