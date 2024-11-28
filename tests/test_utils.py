"""Test xoinvader.utils module."""

import pytest

from xoinvader.utils import (
    InfiniteList,
    Point,
    clamp,
    dotdict,
    setup_logger,
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
    ("val", "min_val", "max_val", "expected"),
    (
        (-10, -5, 5, -5),
        (-10, -10, -8, -10),
        (-10, -5, -2, -5),
        (0, -1, 1, 0),
        (20, 0, 100, 20),
        (120, 0, 100, 100),
    ),
)
def test_clamp(val, min_val, max_val, expected):
    """xoinvader.utils.clamp"""

    assert clamp(val, min_val, max_val) == expected


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
