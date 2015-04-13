import time
import logging


log_format = "[%(asctime)s] %(levelname)s: %(message)s"
date_format = "%m/%d/%Y %I:%M:%S %p"


def create_logger(lname, fname, fmode="w", level=logging.INFO):
    logging.basicConfig(filename=fname,
                        filemode=fmode,
                        format=log_format,
                        datefmt=date_format,
                        level=level)
    return logging.getLogger(lname)


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


class _Color(object):
    def __init__(self):
        self._color_names = [
            # User interface colors
            "ui_norm",
            "ui_yellow",
            # Damage panel colors
            "dp_blank",
            "dp_ok",
            "dp_middle",
            "dp_critical",
            "sh_ok",
            "sh_mid",
            # Weapon's gauge colors
            "blaster",
            "laser",
            "um",
        ]
        self._color_map = dict(zip(self._color_names,
                               range(1, len(self._color_names) + 1)))

    def __getattr__(self, name):
        return self._color_map[name]

Color = _Color()


class Style(object):
    def __init__(self):
        self._style = {
            "gui" : {},
            "obj" : {},
        }

    def init_styles(self, curses):
        self.gui["normal"] = curses.color_pair(Color.ui_norm)   | curses.A_BOLD
        self.gui["yellow"] = curses.color_pair(Color.ui_yellow) | curses.A_BOLD

        self.gui["dp_blank"]    = curses.color_pair(Color.dp_blank)    | curses.A_BOLD
        self.gui["dp_ok"]       = curses.color_pair(Color.dp_ok)       | curses.A_BOLD
        self.gui["dp_middle"]   = curses.color_pair(Color.dp_middle)   | curses.A_BOLD
        self.gui["dp_critical"] = curses.color_pair(Color.dp_critical) | curses.A_BOLD
        self.gui["sh_ok"]       = curses.color_pair(Color.sh_ok)       | curses.A_BOLD
        self.gui["sh_mid"]      = curses.color_pair(Color.sh_mid)      | curses.A_BOLD

    def __getattr__(self, name):
        return self._style[name]

style = Style()


class InfiniteList(list):
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
        if self._running:
            self._current = time.perf_counter()

    def _timeIsUp(self):
        """Return True if time's up, False otherwise."""
        return self._current - self._start >= self._end

    def start(self):
        self._running = True
        self._start = time.perf_counter()

    def stop(self):
        self._running = False

    def restart(self):
        self._start = time.perf_counter()
        self._current = self._start
        self.start()

    def reset(self):
        self._running = False
        self._start = 0
        self._current = 0

    def update(self):
        """Public method for using in loops."""
        if self._running == False:
            return

        self._tick()
        if self._timeIsUp() and self._running:
            self._func()
            self.stop()

            # Timer's accuracy depends on owner's loop
            self._current = self._end
            
    def isRunning(self):
        return self._running

    def getElapsed(self):
        """Return elapsed time."""
        return self._current - self._start

    def getRemaining(self):
        """Return remaining time."""
        return self._end - self.getElapsed()

    def fireFunction(self):
        """Call stored callback."""
        self._func()
