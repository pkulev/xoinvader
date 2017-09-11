"""Test xoinvader.collision module."""

import pytest

from xoinvader.collision import (
    Collider, CollisionManager, CollisionManagerNotFound, TypePair
)
from xoinvader.utils import Point


# pylint: disable=invalid-name,protected-access,missing-docstring
@pytest.mark.xfail
def test_collision():

    class Obj(object):
        def __init__(self, pos):
            self.pos = pos

        def type(self):
            return self.__class__.__name__

    with pytest.raises(CollisionManagerNotFound):
        Collider(Obj(Point()), [])

    cm = CollisionManager()
    c1 = Collider(
        Obj(Point()), [
            "##",
            "##",
        ])

    c2 = Collider(
        Obj(Point()), [
            "..",
            ".."
        ])

    assert cm.check_collision(c1, c2) is None

    c3 = Collider(
        Obj(Point()), [
            "##",
            "##"
        ])
    assert cm.check_collision(c1, c3)

    c3.obj.pos = Point(1, 0)
    assert cm.check_collision(c1, c3)
    c3.obj.pos = Point(0, 1)
    assert cm.check_collision(c1, c3)
    c3.obj.pos = Point(1, 1)
    assert cm.check_collision(c1, c3)

    c3.obj.pos = Point(0, 2)
    assert cm.check_collision(c1, c3) is None
    c3.obj.pos = Point(2, 0)
    assert cm.check_collision(c1, c3) is None

    c4 = Collider(
        Obj(Point()), [
            "..",
            ".#",
        ])

    assert cm.check_collision(c1, c4)
    c4.obj.pos = Point(1, 0)
    assert cm.check_collision(c1, c4) is None


def test_type_pair():
    p1 = TypePair("t1", "t2")
    p2 = TypePair("t2", "t1")
    assert p1._pair != p2._pair
    assert p1 != p2
    assert hash(p1) != hash(p2)


@pytest.mark.xfail
def test_collision_manager():
    import gc
    gc.collect()
    assert Collider.__manager__ is None

    # pylint: disable=too-few-public-methods
    class MockManager(object):
        def __call__(self):
            return self

        def _add(self, _collider):
            pass

        def _add_collision(self, other_type, callback=None):
            pass

    m = MockManager()
    Collider.__manager__ = m
    c = Collider("", [], None)
    mm = CollisionManager()
    with pytest.raises(ValueError):
        mm._add_collision(c, "other", lambda: 0)
    assert not mm._colliders
    assert not mm._collisions

    Collider.__manager__ = None
    mm = CollisionManager()

    c1 = Collider("t1", [], None)
    c2 = Collider("t2", [], None)
    mm._add_collision(c1, "t1", lambda: 0)
    assert len(mm._collisions) == 1
    mm._add_collision(c2, "t2", lambda: 0)
    assert len(mm._collisions) == 2
    mm._add_collision(c2, "t1", lambda: 0)
    assert len(mm._collisions) == 3
    c2.add_handler("t1", lambda: 0)
    t = TypePair("t1", "t2")
    assert len(mm._collisions) == 3
    assert len(mm._collisions[t]) == 2


@pytest.mark.xfail
def test_manager_update():

    mm = CollisionManager()

    # pylint: disable=too-few-public-methods
    class Ship(object):
        def __init__(self):
            self.health = 10
            self.pos = Point(0, 10)
            self.collider = Collider(
                "ship", [
                    "..#..",
                    "#####",
                    ".#.#."
                ], Point(0, 10))

        def rocket_collision(self):
            def callback(_):
                self.health -= 10
            return callback

    ship = Ship()

    rocket = Collider(
        "rocket", [
            "#",
            "#",
            "#"
        ], Point(0, 0))

    ship.collider.add_handler("rocket", ship.rocket_collision())

    mm.update()
    assert ship.health == 10

    rocket.update(Point(0, 8))
    mm.update()
    assert ship.health == 10

    rocket.update(Point(0, 9))
    mm.update()
    assert ship.health == 0
