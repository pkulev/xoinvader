"""Test xoinvader.handlers module."""

import pytest

from xoinvader import handlers


class EventQueueMock:
    """Event queue mock."""

    key = "test-key"

    def getch(self):
        """Mocked method to emit pressed key."""

        return self.key

    def mocked_event_queue(self):  # pylint: disable=no-self-use
        """Mocked method to emit wrong event."""

        return [("bad-event", "test")]


class OwnerMock:  # pylint: disable=too-few-public-methods
    """Owner mock to provide access to app and event queue for handler."""

    @property
    def app(cls):
        return cls

    @property
    def event_queue(cls):
        return EventQueueMock()


def test_event_handler():
    """Test xoinvader.handlers.EventHandler."""

    events = handlers.EventHandler(OwnerMock())

    assert isinstance(events.owner, OwnerMock)
    assert isinstance(events._event_queue, EventQueueMock)

    assert events.get_input() == EventQueueMock.key
    assert events.event_queue() == [("KEY_PRESS", EventQueueMock.key)]

    assert not events.handle()

    fired = []
    events = handlers.EventHandler(
        OwnerMock(),
        {EventQueueMock.key: lambda: fired.append(EventQueueMock.key)},
    )

    events.handle()
    assert fired == [EventQueueMock.key]


def test_event_handler_negative(monkeypatch):
    """Negatively test xoinvader.handlers.EventHandler."""

    monkeypatch.setattr(
        handlers.EventHandler, "event_queue", EventQueueMock.mocked_event_queue
    )

    events = handlers.EventHandler(OwnerMock())
    with pytest.raises(ValueError):
        events.handle()
