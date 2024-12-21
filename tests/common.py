"""Test related utilites."""

from eaf.state import State


PREFIX = "tests/fixtures/"
"""Test fixture data prefix."""


# pylint: disable=missing-docstring
class StateMock(State):
    """Mock State interface."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self.loop_count = 1

        def noop() -> None:
            pass

        # Hooks for loop testing
        self.on_events = noop
        self.on_update = noop
        self.on_render = noop

    def events(self) -> None:
        self.on_events()

    def update(self) -> None:
        self.on_update()

    def render(self) -> None:
        self.on_render()
        if self.loop_count <= 0:
            self.app.stop()

        self.loop_count -= 1


class AnotherStateMock(StateMock):
    """Class for test with two instances."""
