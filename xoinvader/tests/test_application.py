"""xoinvader.application.Application unit test."""

import pytest

from xoinvader import constants
from xoinvader.common import Settings
import xoinvader.curses_utils
from xoinvader.application import get_application, Application
from xoinvader.application.ncurses_app import CursesApplication

from xoinvader.tests.common import StateMock, AnotherStateMock


def test_application():
    """xoinvader.application.Application"""

    app = Application()
    assert pytest.raises(AttributeError, lambda: app.state)
    assert pytest.raises(AttributeError, app.start)
    assert app.screen is None
    app.fps = 40
    assert app.fps == 40

    # One element
    app.register_state(StateMock)
    assert len(app._states) == 1
    assert app.state == StateMock.__name__

    assert pytest.raises(KeyError, lambda: setattr(app, "state", "test"))

    # Many elements
    app.register_state(AnotherStateMock)
    assert len(app.states) == 2
    # Ensure that Application._state hasn't changed
    assert app.state == StateMock.__name__

    app.state = AnotherStateMock.__name__
    assert app.state == AnotherStateMock.__name__


def test_curses_application(monkeypatch):
    """xoinvader.application.CursesApplication"""
    monkeypatch.setattr(
        xoinvader.curses_utils, "create_window",
        lambda *args, **kwargs: True)
    monkeypatch.setattr(
        xoinvader.curses_utils, "deinit_curses",
        lambda *args, **kwargs: True)

    assert CursesApplication == get_application()
    app = CursesApplication()

    assert app.set_caption("test") is None
    assert _test_application_loop(app)


def test_pygame_application(monkeypatch):
    """xoinvader.application.PygameApplication"""

    pygame = pytest.importorskip("pygame")

    from xoinvader.application.pygame_app import PygameApplication

    monkeypatch.setattr(pygame, "init", lambda: (0, 6))
    monkeypatch.setattr(pygame, "quit", lambda: True)
    monkeypatch.setattr(pygame.display, "set_mode", lambda *a: True)
    monkeypatch.setattr(pygame.display, "update", lambda: True)
    monkeypatch.setattr(pygame.key, "set_repeat", lambda *a: True)

    Settings.system.video_driver = constants.DRIVER_SDL

    # Empty object
    assert PygameApplication == get_application()
    app = PygameApplication((800, 600), 0, 32)
    app.set_caption("test")
    assert app.screen is not None
    assert pytest.raises(ValueError, lambda: setattr(app, "fps", "thirty"))
    assert pytest.raises(AttributeError, lambda: app.state)

    assert _test_application_loop(app)


def _test_application_loop(app):
    """Test main loop behaviour."""

    assert pytest.raises(AttributeError, app.start)
    app.register_state(StateMock)
    assert app.start() is None

    app.register_state(AnotherStateMock)
    app.state = AnotherStateMock.__name__
    assert app.start() is None
    assert app.stop() is None
    return True
