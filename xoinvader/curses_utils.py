"""Curses helper module."""

import time

from xoinvader.common import Settings


class Clock:
    """Object that helps to track time."""

    def __init__(self):
        self._mspf = 0
        self._previous_tick = 0
        self._current_tick = int(time.perf_counter())
        self._tick_time = 0

    def tick(self, framerate=0.0):
        """Update the clock.

        :param float framerate: expected FPS
        """

        self._previous_tick = self._current_tick
        self._current_tick = int(time.perf_counter())
        delta = self._current_tick - self._previous_tick

        self._mspf = int(1.0 / framerate * 1000.0) if framerate else delta

        time_s = (self._mspf - delta) / 1000.0
        time.sleep(time_s)
        self._tick_time = int(time.perf_counter()) - self._previous_tick
        return self._tick_time

    def get_fps(self):
        """Compute the clock framerate.

        :return: FPS
        :rtype: float
        """
        pass

    def get_time(self):
        """Time used in previous tick.

        :return: tick duration in milliseconds
        :rtype: int
        """
        return self._tick_time


def get_clock():
    """Helper for unification with other backends."""

    return Clock()
