"""Test xoinvader.handlers module."""

import pytest

from xoinvader import handlers


class ScreenMock(object):
    """Screen mock."""

    key = "test-key"

    def getch(self):
        """Mocked method to emit pressed key."""

        return self.key

    def mocked_event_queue(self):  # pylint: disable=no-self-use
        """Mocked method to emit wrong event."""

        return [("bad-event", "test")]


class OwnerMock:  # pylint: disable=too-few-public-methods
    """Owner mock to provide access to screen and actor for handler."""

    screen = ScreenMock()
    actor = "actor"


def test_event_handler():
    """Test xoinvader.handlers.EventHandler."""

    events = handlers.EventHandler(OwnerMock())

    assert isinstance(events.owner, OwnerMock)
    assert isinstance(events.screen, ScreenMock)
    assert events.actor == OwnerMock.actor

    assert events.get_input() == ScreenMock.key
    assert events.event_queue() == [("KEY_PRESS", ScreenMock.key)]

    assert not events.handle()

    fired = []
    events = handlers.EventHandler(OwnerMock(), {
        ScreenMock.key: lambda: fired.append(ScreenMock.key)
    })

    events.handle()
    assert fired == [ScreenMock.key]


def test_event_handler_negative(monkeypatch):
    """Negatively test xoinvader.handlers.EventHandler."""

    monkeypatch.setattr(handlers.EventHandler, "event_queue",
                        ScreenMock.mocked_event_queue)

    events = handlers.EventHandler(OwnerMock())
    with pytest.raises(ValueError):
        events.handle()
