"""Tests for xoinvader.state module."""


import unittest

from xoinvader.state import State


class TestState(unittest.TestCase):
    """xoinvader.state.State"""

    def test_base_class(self):
        """base_class"""
        state = State("owner")

        self.assertEqual(state.owner, "owner")
        self.assertEqual(state.actor, None)
        self.assertEqual(state.screen, None)

        self.assertRaises(NotImplementedError, state.events)
        self.assertRaises(NotImplementedError, state.update)
        self.assertRaises(NotImplementedError, state.render)
