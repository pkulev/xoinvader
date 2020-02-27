"""Tests for xoinvader.state module."""


import pytest

from xoinvader.state import State


def test_state():
    """Test xoinvader.state.State base class."""

    state = State("owner")

    assert state.owner == "owner"
    assert state.actor is None
    assert state.screen is None

    assert not state.postinit()
    assert not state.trigger()


    with pytest.raises(NotImplementedError):
        state.events()

    assert not state.update()
    assert not state.render()
