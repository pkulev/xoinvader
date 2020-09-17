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


def clamp(val, min_val, max_val):
    """Clamp value between boundaries."""

    if max_val < min_val:
        raise ValueError("max_val must be >= min_val")

    return min(max(val, min_val), max_val)


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
