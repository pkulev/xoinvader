"""Test xoinvader.animation module."""

from math import isclose

import pytest

from xoinvader import animation
from xoinvader.animation import Animation, AnimationManager
from xoinvader.utils import Point


# pylint: disable=invalid-name,protected-access,missing-docstring
# pylint: disable=too-few-public-methods
class GameObject(object):
    """Game object mock."""

    def __init__(self):
        self.attr = 0
        self.anim = None


def test_animation():

    with pytest.raises(ValueError):
        Animation("dummy", bind=None, attr=None, keyframes=[])

    obj = GameObject()
    keyframes = [
        (0.0, 1),
        (0.5, 2),
        (2.0, 10),
    ]
    anim = Animation(name="test", bind=obj, attr="attr", keyframes=keyframes)

    obj.anim = anim
    assert anim.name == "test"

    anim.update(100)
    assert obj.attr == 1
    anim.update(450)
    assert obj.attr == 2

    # Frame must be unchanged
    for _ in range(10):
        anim.update(100)

    assert obj.attr == 2
    anim.update(1000)  # here time is > 2
    assert obj.attr == 10
    with pytest.raises(StopIteration):
        anim.update(1)  # It's time to switch animation


def test_animation_loop():
    obj = GameObject()
    animgr = AnimationManager()
    animgr.add("test", obj, "attr", keyframes=[(0.0, 0), (1.0, 1)], loop=True)

    animgr.update(1)
    assert obj.attr == 0
    animgr.update(1000)
    assert obj.attr == 1
    animgr.update(1)
    assert obj.attr == 0
    animgr.update(500)
    assert obj.attr == 0
    animgr.update(500)
    assert obj.attr == 1


@pytest.mark.parametrize("loop", (True, False))
def test_animation_interp_loop(loop):
    obj = GameObject()
    animgr = AnimationManager()
    animgr.add(
        "test",
        obj,
        "attr",
        keyframes=[(0.0, 0), (0.4, 1)],
        interp=True,
        loop=loop,
    )

    animgr.update(100)
    assert isclose(obj.attr, 0.25, abs_tol=0.01)
    animgr.update(200)
    assert isclose(obj.attr, 0.75, abs_tol=0.01)
    animgr.update(200)
    assert obj.attr == 1
    animgr.update(200)

    # if not looped - animation stops
    # TODO: test StopIteration, now animgr suppresses it
    if loop:
        assert isclose(obj.attr, 0.5, abs_tol=0.01)
        animgr.update(13)
    else:
        assert obj.attr == 1
        animgr.update(13)


def test_animation_manager():
    obj = GameObject()
    animgr = AnimationManager()

    with pytest.raises(AttributeError):
        assert animgr.animation

    assert not animgr._animation and animgr.update(13) is None

    animgr.add("test1", bind=obj, attr="attr", keyframes=[(0.0, 1)])
    animgr.add("test2", bind=obj, attr="attr", keyframes=[(0.0, 2)])

    assert animgr.animation == "test1"

    with pytest.raises(ValueError):
        animgr.animation = "bad-animation"

    animgr.animation = "test2"
    assert animgr.animation == "test2"
    animgr.animation = "test1"

    animgr.update(13)

    assert animgr.update(13) is None


@pytest.mark.parametrize(
    ("values", "types", "expected"),
    (
        ([1, 2, 3], int, True),
        ([1, 2, "3"], (int, float), False),
        ([1, 2, 3.0], int, False),
        ([1, 2, 3.0], (int, float), True),
    ),
)
def test_same_type(values, types, expected):
    assert animation.same_type(values, types) is expected


@pytest.mark.parametrize(
    ("args", "result"),
    (
        # increasing
        ((0.0, 2.0, 0.0, 1.0, 0.0), 0.0),
        ((0.0, 2.0, 0.0, 1.0, 0.2), 0.4),
        ((0.0, 2.0, 0.0, 1.0, 1.0), 2.0),
        # decreasing
        ((2.0, 1.0, 1.0, 2.0, 1.0), 2.0),
        ((2.0, 1.0, 1.0, 2.0, 1.2), 1.8),
        ((2.0, 1.0, 1.0, 2.0, 2.0), 1.0),
        # negative value
        ((0.0, -1.0, 2.0, 3.0, 2.0), 0.0),
        ((0.0, -1.0, 2.0, 3.0, 2.5), -0.5),
        ((0.0, -1.0, 2.0, 3.0, 3.0), -1.0),
    ),
)
def test_linear_equation(args, result):
    assert animation.linear_equation(*args) == result


@pytest.mark.parametrize(
    ("args", "result"),
    (
        ([(1, 1), (2, 2), 1.5], 1.5),
        ([(1.0, 1.0), (2.0, 2.0), 1.5], 1.5),
        (
            [(1.0, Point(1, 2, 1)), (2.0, Point(2, 1, 2)), 1.5],
            Point(1.5, 1.5, 1.5),
        ),
        (
            [(1.0, Point(1.0, 2.0, 1.0)), (2.0, Point(2.0, 1.0, 2.0)), 1.5],
            Point(1.5, 1.5, 1.5),
        ),
    ),
)
def test_interpolate_positive(args, result):
    assert animation.interpolate(*args) == result


@pytest.mark.parametrize(
    ("args", "expected_error"),
    (
        ([(1.0, 1.0), (2.0, 2.0), 0.99], animation.AnimationBoundariesExceeded),
        ([(1.0, 1.0), (2.0, 2.0), 2.01], animation.AnimationBoundariesExceeded),
        ([(1.0, "a"), (2.0, "b"), 1.5], animation.InterpolationUnknownTypes),
    ),
)
def test_interpolate_negative(args, expected_error):
    with pytest.raises(expected_error):
        animation.interpolate(*args)
