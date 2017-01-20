import pytest

from xoinvader.collision import Collider, CollisionManager, TypePair
from xoinvader.utils import Point


def test_collision():
    with pytest.raises(ValueError):
        c = Collider("", [], None)
    cm = CollisionManager()
    c1 = Collider(
        "",
        [
            "##",
            "##",
        ],
        Point(0, 0))

    c2 = Collider(
        "",
        [
            "..",
            ".."
        ],
        Point(0, 0))

    assert cm.check_collision(c1, c2) is None

    c3 = Collider(
        "",
        [
            "##",
            "##"
        ],
        Point(0, 0))
    assert cm.check_collision(c1, c3)

    c3._pos = Point(1, 0)
    assert cm.check_collision(c1, c3)
    c3._pos = Point(0, 1)
    assert cm.check_collision(c1, c3)
    c3._pos = Point(1, 1)
    assert cm.check_collision(c1, c3)

    c3._pos = Point(0, 2)
    assert cm.check_collision(c1, c3) is None
    c3._pos = Point(2, 0)
    assert cm.check_collision(c1, c3) is None

    c4 = Collider(
        "",
        [
            "..",
            ".#",
        ],
        Point(0, 0))

    assert cm.check_collision(c1, c4)
    c4._pos = Point(1, 0)
    assert cm.check_collision(c1, c4) is None


def test_type_pair():
    p1 = TypePair("t1", "t2")
    p2 = TypePair("t2", "t1")
    assert p1._pair == p2._pair
    assert p1 == p2
    assert hash(p1) == hash(p2)


def test_collision_manager():
    import gc
    gc.collect()
    assert Collider.__manager__ is None

    class MockManager(object):
        def __call__(self):
            return self

        def _add(self, _collider):
            pass

    m = MockManager()
    Collider.__manager__ = m
    c = Collider("", [], None)
    mm = CollisionManager()
    with pytest.raises(ValueError):
        mm._add_collision(c, "other", lambda: _)
    assert not mm._colliders
    assert not mm._collisions

    Collider.__manager__ = None
    mm = CollisionManager()

    c1 = Collider("t1", [], None)
    c2 = Collider("t2", [], None)
    mm._add_collision(c1, "t1", lambda: _)
    assert len(mm._collisions) == 1
    mm._add_collision(c2, "t2", lambda: _)
    assert len(mm._collisions) == 2
    mm._add_collision(c2, "t1", lambda: _)
    assert len(mm._collisions) == 3
    c2.add_handler("t1", lambda: _)
    t = TypePair("t1", "t2")
    assert len(mm._collisions) == 3
    assert len(mm._collisions[t]) == 2

def test_manager_update():
    Collider.__manager__ = None
    mm = CollisionManager()

    class Ship(object):
        def __init__(self):
            self.health = 10
            self.pos = Point(0, 10)
            self.collider = Collider("ship",
                                     ["..#..",
                                      "#####",
                                      ".#.#."],
                                     Point(0, 10))

        def rocket_collision(self):
            def callback(_):
                self.health -= 10
            return callback

    ship = Ship()

    r_pos = Point(0, 0)
    rocket = Collider("rocket",
                      ["#",
                       "#",
                       "#"],
                      r_pos)

    ship.collider.add_handler("rocket", ship.rocket_collision())

    mm.update()
    assert ship.health == 10

    r_pos.y = 8
    mm.update()
    assert ship.health == 10

    r_pos.y = 9
    mm.update()
    assert ship.health == 0
