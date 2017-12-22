"""Test related utilites."""

from xoinvader.state import State


PREFIX = "xoinvader/tests/fixtures/"
"""Test fixture data prefix."""


# pylint: disable=missing-docstring
class StateMock(State):
    """Mock State interface."""

    def __init__(self, owner):
        super(StateMock, self).__init__(owner)
        self.loop_count = 1

        def nop():
            pass

        # Hooks for loop testing
        self.on_events = nop
        self.on_update = nop
        self.on_render = nop

    def events(self):
        self.on_events()

    def update(self):
        self.on_update()

    def render(self):
        self.on_render()
        if self.loop_count <= 0:
            self.owner.stop()

        self.loop_count -= 1


class AnotherStateMock(StateMock):
    """Class for test with two instances."""
    pass
