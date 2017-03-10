"""Test xoinvader.curses_utils module."""

import time

from xoinvader.curses_utils import Clock, get_clock
from xoinvader.utils import isclose


# pylint: disable=invalid-name
def test_clock():
    """xoinvader.curses_utils.Clock"""

    assert isinstance(get_clock(), Clock)

    clock = Clock()
    t1 = int(time.perf_counter())
    assert clock.get_time() == 0
    # assert clock.get_fps() == 0.0
    ticked = clock.tick()
    t2 = int(time.perf_counter())
    assert isclose(t2 - t1, ticked)
    assert clock.get_time() == ticked
