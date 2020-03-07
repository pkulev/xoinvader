"""Test related utilites."""

from xoinvader.state import State


PREFIX = "xoinvader/tests/fixtures/"
"""Test fixture data prefix."""


# pylint: disable=missing-docstring
class StateMock(State):
    """Mock State interface."""

    def __init__(self, app):
        super(StateMock, self).__init__(app)
        self.loop_count = 1

        def noop():
            pass

        # Hooks for loop testing
        self.on_events = noop
        self.on_update = noop
        self.on_render = noop

    def events(self):
        self.on_events()

    def update(self):
        self.on_update()

    def render(self):
        self.on_render()
        if self.loop_count <= 0:
            self.app.stop()

        self.loop_count -= 1


class AnotherStateMock(StateMock):
    """Class for test with two instances."""
