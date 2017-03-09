import pytest

from xoinvader.level import Level


def test_wave():
    e = Level()

    class MockObject(object):
        def __init__(self):
            self.value = 0

        def add(self):
            self.value += 10

    a = MockObject()
    b = MockObject()

    e.add_event(10, a.add)
    e.add_event(20, b.add)

    e.speed = 10
    e.update()
    assert a.value == 0
    assert b.value == 0
    e.start()
    e.update()
    assert a.value == 10
    assert b.value == 0
    e.update()
    assert a.value == 10
    assert b.value == 10

    assert not e.running
