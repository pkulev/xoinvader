"""Various useful tools."""


import logging
import time
try:
    import time.perf_counter
except ImportError:
    time.perf_counter = time.time


LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"


def create_logger(lname, fname, fmode="w", level=logging.INFO):
    """Create simple logger.

    .. note:: Needs enchancement.

    :param lname: logger name
    :type lname: string

    :param fname: file name
    :type fname: string

    :param fmode: file mode
    :type fmode: string

    :param level: logging level
    :type level: integer

    :return: logger instance
    :rtype: `logging.Logger`
    """
    logging.basicConfig(filename=fname,
                        filemode=fmode,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        level=level)
    return logging.getLogger(lname)


def isclose(left, right, rel_tol=1e-9, abs_tol=0.0):
    """Check if values are approximately equal.

    :param int,float left: first value
    :param int,float right: second value
    :param float rel_tol: relative tolerance (amount of error allowed)
    :param float abs_tol: minimum absolute tolerance level
    """
    return (abs(left - right) <= max(rel_tol *
                                     max(abs(left), abs(right)), abs_tol))


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

    def __init__(self, x=0, y=0, z=0):
        self._x = x
        self._y = y
        self._z = z

    def __repr__(self):
        return "Point(x={0}, y={1}, z={2})".format(self.x, self.y, self.z)

    __str__ = __repr__

    def __add__(self, other):
        return Point(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    @property
    def x(self):
        """x coordinate.

        :getter: yes
        :setter: yes
        :type: integer
        """
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        """y coordinate.

        :getter: yes
        :setter: yes
        :type: integer
        """
        return self._y

    @y.setter
    def y(self, val):
        self._y = val

    @property
    def z(self):
        """z coordinate.

        :getter: yes
        :setter: yes
        :type: integer
        """
        return self._z

    @z.setter
    def z(self, val):
        self._z = val


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

    def get_image(self):
        """Image generator. Allows to renderers render Surfaces.

        :return: image generator
        :rtype: generator(`xoinvader.utils.Point`, string, integer)
        """
        for y, row in enumerate(self._image):
            for x, image in enumerate(row):
                yield (Point(x=x, y=y), image,
                       self._style[y][x] if self._style else None)


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

        self._tick()
        if self._time_is_up() and self.running:
            self._func()
            self.stop()

            # Timer's accuracy depends on owner's loop
            self._current = self._end

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
