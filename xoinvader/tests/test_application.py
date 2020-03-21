"""xoinvader.application unit tests."""

import pytest

import xoinvader.curses_utils

from xoinvader import constants
from xoinvader.application import (
    get_current,
)
from xoinvader.application.ncurses_app import CursesApplication

from xoinvader.tests.common import StateMock, AnotherStateMock


def test_curses_application(monkeypatch):
    """xoinvader.application.CursesApplication"""

    monkeypatch.setattr(
        xoinvader.curses_utils, "create_window", lambda *args, **kwargs: True
    )
    monkeypatch.setattr(
        xoinvader.curses_utils, "deinit_curses", lambda *args, **kwargs: True
    )

    app = CursesApplication()
    assert isinstance(get_current(), CursesApplication)
    assert get_current() is app

    assert app.renderer is not None
    assert app.set_caption("test") is None

    # TODO: hangs in loop
    # assert _test_application_loop(app)


def test_pygame_application(monkeypatch):
    """xoinvader.application.PygameApplication"""

    pygame = pytest.importorskip("pygame")

    from xoinvader.application.pygame_app import PygameApplication

    monkeypatch.setattr(pygame, "init", lambda: (0, 6))
    monkeypatch.setattr(pygame, "quit", lambda: True)
    monkeypatch.setattr(pygame.display, "set_mode", lambda *a: True)
    monkeypatch.setattr(pygame.display, "update", lambda: True)
    monkeypatch.setattr(pygame.key, "set_repeat", lambda *a: True)

    # Empty object
    app = PygameApplication((800, 600), 0, 32)
    assert isinstance(get_current(), PygameApplication)
    assert get_current() is app

    assert app.renderer is not None
    assert app.set_caption("test") is None

    # TODO: hangs in loop
    # assert _test_application_loop(app)


def _test_application_loop(app):
    """Test main loop behaviour."""

    app.register(StateMock)
    assert app.start() is None

    app.register(AnotherStateMock)
    app.state = AnotherStateMock.__name__
    assert app.start() is None
    assert app.stop() is None
    return True
