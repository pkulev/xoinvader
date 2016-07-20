"""xoinvader.application.Application unit test."""


import time

import pygame
import pytest

import xoinvader.curses_utils
from xoinvader.application import (
    Application, CursesApplication, PygameApplication, get_application
)


class StateMock(object):
    """Mocks State interface."""
    on_event = lambda: None

    def __init__(self, owner):
        self.owner = owner
        self.one_loop_passed = False

    def events(self):
        """Event stub."""
        StateMock.on_event()
        time.sleep(0.5)

    def update(self):
        """Update stub."""
        time.sleep(0.5)

    def render(self):
        """Render stub."""
        time.sleep(0.5)
        if self.one_loop_passed:
            self.owner.stop()
        else:
            self.one_loop_passed = True


class AnotherStateMock(StateMock):
    """YAS."""
    pass


# TODO: add new cases after func implementation
def test_get_application():
    """xoinvader.application.get_application"""
    assert CursesApplication == get_application()


def test_application():
    """xoinvader.application.Application"""

    app = Application(startup_args={"no_sound": True})
    assert pytest.raises(AttributeError, lambda: app.state)
    assert app.screen is None
    assert app.running is False
    app.fps = 40
    assert app.fps == 40

    # One element
    app.register_state(StateMock)
    assert len(app._states) ==  1
    assert app.state == StateMock.__name__

    assert pytest.raises(KeyError, lambda: app.__setattr__("state", "test"))

    # Many elements
    app.register_state(AnotherStateMock)
    assert len(app._states) == 2
    # Ensure that Application._state hasn't changed
    assert app.state == StateMock.__name__

    app.state = AnotherStateMock.__name__
    assert app.state == AnotherStateMock.__name__


def test_curses_application(monkeypatch):
    """xoinvader.application.CursesApplication"""
    monkeypatch.setattr(
        xoinvader.curses_utils, "create_window",
        lambda *args, **kwargs: True)

    app = CursesApplication()

    assert app.set_caption("test") is None
    assert _test_application_loop(app)


def test_pygame_application():
    """xoinvader.application.PygameApplication"""

    # Empty object
    app = PygameApplication((800, 600), 0, 32)
    app.set_caption("test")
    assert pygame.display.get_caption()[0] == "test"
    assert app.screen is not None
    assert pytest.raises(ValueError, lambda: app.__setattr__("fps", "thirty"))
    assert pytest.raises(AttributeError, lambda: app.state)
    assert app.running is False

    assert _test_application_loop(app)


def _test_application_loop(app):
    """Test main loop behaviour."""

    def check_running_is_true():
        """Assert running."""
        assert app.running is True

    assert pytest.raises(AttributeError, app.loop)
    state_mock = StateMock
    state_mock.on_events = check_running_is_true
    app.register_state(StateMock)
    assert app.running is False
    app.loop()
    assert app.running is False
    return True
