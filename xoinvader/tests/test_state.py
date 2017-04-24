"""Tests for xoinvader.state module."""


import pytest

from xoinvader.state import State


def test_state():
    """Test xoinvader.state.State base class."""

    state = State("owner")

    assert state.owner == "owner"
    assert state.actor is None
    assert state.screen is None

    with pytest.raises(NotImplementedError):
        state.events()
    with pytest.raises(NotImplementedError):
        state.update()
    with pytest.raises(NotImplementedError):
        state.render()
