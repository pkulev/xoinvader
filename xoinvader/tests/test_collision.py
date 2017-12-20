"""Test xoinvader.collision module."""

import pytest

from xoinvader import collision
from xoinvader.collision import (
    Collider, CollisionManager, CollisionManagerNotFound, TypePair
)
from xoinvader.utils import Point


# pylint: disable=invalid-name,protected-access
def test_collision(mock_state):
    """Generic test for Collider and CollisionManager."""

    class Obj(object):
        def __init__(self, pos):
            self.pos = pos

        def type(self):
            return self.__class__.__name__

    state = mock_state(mock_app=True)

    with pytest.raises(CollisionManagerNotFound):
        Collider(Obj(Point()), [])

    cm = CollisionManager()
    state.collision = cm

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

    assert len(cm._colliders) == 4
    cm.remove(c4)
    assert len(cm._colliders) == 3


def test_type_pair():
    p1 = TypePair("t1", "t2")
    p2 = TypePair("t2", "t1")
    assert p1._pair != p2._pair
    assert p1 != p2
    assert hash(p1) != hash(p2)
    assert str(p1) == "TypePair(t1, t2)"


def test_manager_update(mock_state):

    state = mock_state(mock_app=True)
    cmanager = CollisionManager()
    state.collision = cmanager

    # pylint: disable=too-few-public-methods
    class Ship(object):
        def __init__(self):
            self.health = 10
            self.pos = Point(0, 10)
            self._collider = Collider(
                self, [
                    "..#..",
                    "#####",
                    ".#.#."
                ])

        def type(self):
            return self.__class__.__name__

        @collision.register("Ship", "Rocket")
        def collide(self, other, rect):
            self.health -= other.damage

    class Rocket(object):

        def __init__(self):
            self.damage = 10
            self.pos = Point(0, 0)
            self._collider = Collider(
                self, [
                    "#",
                    "#",
                    "#",
                ])

        def type(self):
            return self.__class__.__name__

    ship = Ship()
    rocket = Rocket()

    cmanager.update()
    assert ship.health == 10

    rocket.pos = Point(0, 8)
    cmanager.update()
    assert ship.health == 10

    rocket.pos = Point(0, 9)
    cmanager.update()
    assert ship.health == 0
