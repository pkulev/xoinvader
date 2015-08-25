"""xoinvader.application.Application unit test."""

import time
import unittest

from xoinvader.application import Application


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


class TestApplication(unittest.TestCase):
    """Unit test."""

    def test_application_properties(self):
        """Test general property behaviour."""

        # Empty object
        app = Application()
        self.assertRaises(AttributeError, lambda: app.state)
        self.assertRaises(AttributeError, app.loop)
        self.assertIs(app.running, False)

        # One element
        app.register_state(StateMock)
        self.assertEqual(len(app._states), 1)
        self.assertEqual(app.state, StateMock.__name__)

        def set_state():
            """Change state."""
            app.state = "test"
        self.assertRaises(KeyError, set_state)

        # Many elements
        app.register_state(AnotherStateMock)
        self.assertEqual(len(app._states), 2)
        # Ensure that Application._state hasn't changed
        self.assertEqual(app.state, StateMock.__name__)

        app.state = AnotherStateMock.__name__
        self.assertEqual(app.state, AnotherStateMock.__name__)

    def test_application_loop(self):
        """Test main loop behaviour."""
        def check_running_is_true():
            """Assert running."""
            self.assertIs(app.running, True)

        app = Application()
        app._mspf = 16
        state_mock = StateMock

        state_mock.on_events = check_running_is_true
        app.register_state(StateMock)
        self.assertIs(app.running, False)
        app.loop()
        self.assertIs(app.running, False)

        #TODO: test slow loop execution
        #TODO: implement logging

    def test_application_startup_args(self):
        """Test startup_args."""
        app = Application({"no_sound": True})
        self.assertRaises(KeyError, Application, {"test": "arg"})
