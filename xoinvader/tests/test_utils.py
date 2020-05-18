"""Test xoinvader.utils module."""

import pytest

from xoinvader.utils import (
    setup_logger,
    dotdict,
    isclose,
    InfiniteList,
    Point,
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


@pytest.mark.parametrize(
    ("left", "right", "kwargs", "expected"),
    (
        (0.0, 0.0, {}, True),
        (1.0, 0.0, {}, False),
        (0.1, 0.0, {}, False),
        (0.1, 0.0, {"abs_tol": 0.1}, True),
        (0.1, 0.0, {"rel_tol": 0.1}, False),
    ),
)
def test_isclose(left, right, kwargs, expected):
    """xoinvader.utils.isclose"""
    assert isclose(left, right, **kwargs) is expected


def test_infinite_list_operations():

    # Test one element behaviour
    data = "test1"
    inf_list = InfiniteList([data])

    assert len(inf_list) == 1
    assert inf_list[0] == data
    assert inf_list.select(0) == data
    assert inf_list.current() == data
    assert inf_list.next() == data
    assert inf_list.prev() == data

    # TODO: Test many elements behaviour


def test_infinite_list_operations_negative():

    # Test empty InfiniteList behaviour
    inf_list = InfiniteList()
    for func in [
        inf_list.current,
        inf_list.next,
        inf_list.prev,
    ]:
        with pytest.raises(IndexError):
            func()

    # Negative tests for one element behaviour

    inf_list.append("test")

    with pytest.raises(IndexError):
        inf_list.select(-1)
    with pytest.raises(IndexError):
        inf_list.select(1)

    # TODO: test many elements behaviour


def test_timer_get_elapsed():
    timer = Timer(5.0, lambda: True)
    timer.start()
    while timer.running:
        assert timer.get_elapsed() >= 0.0
        timer.update(13)
        assert timer.get_elapsed() >= 0.0
