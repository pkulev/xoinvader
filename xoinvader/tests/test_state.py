"""Tests for xoinvader.state module."""


import pytest

from xoinvader.state import State


def test_state(mock_application):
    """Test xoinvader.state.State base class."""

    app = mock_application()
    state = State(app)

    assert state.app is app
    assert state.actor is None
    assert state._renderer is app.renderer

    assert not state.postinit()
    assert not state.trigger()


    with pytest.raises(NotImplementedError):
        state.events()

    assert not state.update()
    assert not state.render()

    assert state._objects == []
    # TODO: add tests for add and remove
