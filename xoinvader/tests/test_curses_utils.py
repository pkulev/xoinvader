"""Tests for xoinvader.curses_utils."""

import time

from xoinvader.curses_utils import Clock, get_clock
from xoinvader.utils import isclose


def test_clock():
    """xoinvader.curses_utils.Clock"""

    assert isinstance(get_clock(), Clock)

    clock = Clock()
    assert clock.get_time() == 0
    # assert clock.get_fps() == 0.0
    ticked = clock.tick()
    t1 = int(time.perf_counter())
    assert isclose(t1, ticked)
    assert clock.get_time() == ticked
