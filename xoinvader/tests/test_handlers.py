"""Test xoinvader.handlers module."""


import unittest

from xoinvader.handlers import Command
from xoinvader.handlers import Handler


class OwnerMock:
    screen = "screen"
    actor = "actor"


class TestCommand(unittest.TestCase):
    def test_base_class(self):
        command = Command()
        self.assertRaises(NotImplementedError, command.execute, "actor")


class TestHandler(unittest.TestCase):
    def test_base_class(self):
        handler = Handler(OwnerMock())
        self.assertRaises(NotImplementedError, handler.handle)
