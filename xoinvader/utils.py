"""Various useful tools."""

import copy
import datetime
import logging

# FIXME: temporary backward compatibility
from eaf.core import Vec3 as Point

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


class InfiniteList(list):
    """Infinite list container."""

    def __init__(self, *args, **kwargs):
        super(InfiniteList, self).__init__(*args, **kwargs)
        self._index = 0

    def select(self, index: int) -> object:
        """Set index and return selected element."""

        if not len(self):
            raise IndexError("List is empty")

        if not (0 <= index < len(self)):
            raise IndexError("Index out of bounds.")

        self._index = index
        return self[self._index]

    def current(self) -> object:
        """Return current element."""

        return self[self._index]

    def next(self) -> object:
        """Select next element and return it."""

        try:
            self._index = (self._index + 1) % len(self)
        except ZeroDivisionError:
            raise IndexError("List is empty.")

        return self[self._index]

    def prev(self) -> object:
        """Select previous element and return it."""

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
        self._start = 0.0
        self._current = self._start
        self._running = False

    def _tick(self, dt):
        """Refresh counter."""
        if self.running:
            self._current += dt / 1000

    def _time_is_up(self):
        """return is it time to fire fuction or not.

        :return: time is up
        :rtype: boolean
        """
        return self._current - self._start >= self._end

    def start(self):
        """Start timer."""
        self._running = True
        self._start = 0.0
        self._current = 0.0

    def stop(self):
        """Stop timer."""
        self._running = False

    def restart(self):
        """Restart timer."""
        self._start = 0.0
        self._current = 0.0
        self.start()

    def reset(self):
        """Reset timer."""
        self._running = False
        self._start = 0.0
        self._current = 0.0

    def update(self, dt):
        """Public method for using in loops."""
        if not self.running:
            return

        # Timer's accuracy depends on owner's loop
        self._tick(dt)
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
