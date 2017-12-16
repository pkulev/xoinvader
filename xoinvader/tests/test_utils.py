"""Test xoinvader.utils module."""

import pytest

from xoinvader.utils import (
    setup_logger,
    dotdict,
    isclose,
    InfiniteList,
    Point,
    Surface,
    Timer,
)


# pylint: disable=invalid-name,protected-access,missing-docstring
def test_setup_logger():
    logger = setup_logger("test", True)
    assert logger


def test_dotdict_setattr():
    settings = dotdict()
    settings.test_entry = 42
    assert settings["test_entry"] == 42
    assert settings.test_entry == 42

    settings["test_entry_2"] = 42
    assert settings.test_entry == 42

    assert pytest.raises(AttributeError, lambda: settings.bad_key)


@pytest.mark.parametrize(("left", "right", "kwargs", "expected"), (
    (0.0, 0.0, {}, True),
    (1.0, 0.0, {}, False),
    (0.1, 0.0, {}, False),
    (0.1, 0.0, {"abs_tol": 0.1}, True),
    (0.1, 0.0, {"rel_tol": 0.1}, False),
))
def test_isclose(left, right, kwargs, expected):
    """xoinvader.utils.isclose"""
    assert isclose(left, right, **kwargs) is expected


def test_point_operations():
    ax, ay, az = 10, 10, 10
    bx, by, bz = 20, 20, 20
    a = Point(ax, ay, az)
    b = Point(bx, by, bz)

    assert a.x == ax
    assert a.y == ay
    assert a.z == az
    assert b.x == bx
    assert b.y == by
    assert b.z == bz

    assert repr(a) == "Point(x={0}, y={1}, z={2})".format(
        a.x, a.y, a.z)

    assert a + b == Point(ax + bx, ay + by, az + bz)
    assert a - b == Point(ax - bx, ay - by, az - bz)
    assert a + 5 == Point(ax + 5, ay + 5, az + 5)
    assert a - 5 == Point(ax - 5, ay - 5, az - 5)
    assert a * 5 == Point(ax * 5, ay * 5, az * 5)
    assert a / 5 == Point(ax / 5, ay / 5, az / 5)

    with pytest.raises(ValueError):
        assert a + "a"
    with pytest.raises(ValueError):
        assert a - "a"
    with pytest.raises(ValueError):
        assert a * "a"
    with pytest.raises(ValueError):
        assert a / "a"
    with pytest.raises(ValueError):
        assert a == "a"

    a.x = bx
    a.y = by
    a.z = bz

    assert a.x == bx
    assert a.y == by
    assert a.z == bz

    b.x = -bx
    b.y = -by
    b.z = -bz

    assert a + b == Point(0, 0, 0)
    assert a + Point(-50, -50, -50) == Point(-30, -30, -30)

    assert Point(1.9, 1.9)[int] == Point(1, 1, 0)


def test_infinite_list_operations():
    # Test empty InfiniteList behaviour

    inf_list = InfiniteList()
    for func in [inf_list.current, inf_list.next, inf_list.prev]:
        with pytest.raises(IndexError):
            func()

    # Test one element behaviour
    data = "test1"
    inf_list = InfiniteList([data])

    assert len(inf_list) == 1
    assert inf_list[0] == data
    assert inf_list.current() == data
    assert inf_list.next() == data
    assert inf_list.prev() == data

    # Test many elements behaviour


_image = [
    [" ", "O", " "],
    ["x", "X", "x"]]


def test_surface_attributes():
    surface = Surface(_image)
    assert surface.height == len(_image)
    assert surface.width == len(_image[0])
    assert surface.raw == _image


def test_image_generator():
    surface = Surface(_image)
    image_gen = surface.get_image()
    for lpos, image, style in image_gen:
        assert _image[lpos.y][lpos.x] == image
        assert style is None


@pytest.mark.slow
def test_timer_get_elapsed():
    timer = Timer(5.0, lambda: True)
    timer.start()
    while timer.running:
        assert timer.get_elapsed() >= 0.0
        timer.update()
        assert timer.get_elapsed() >= 0.0
