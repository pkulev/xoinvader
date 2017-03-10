"""Test xoinvader.handlers module."""

import pytest

from xoinvader.handlers import Command
from xoinvader.handlers import Handler


# pylint: disable=missing-docstring,too-few-public-methods
class OwnerMock:
    screen = "screen"
    actor = "actor"


def test_command():
    command = Command()
    with pytest.raises(NotImplementedError):
        command.execute("actor")


def test_handler():
    handler = Handler(OwnerMock())
    with pytest.raises(NotImplementedError):
        handler.handle()
