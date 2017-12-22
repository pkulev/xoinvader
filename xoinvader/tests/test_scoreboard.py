"""Tests for xoinvader.scoreboard module."""

from operator import itemgetter
import os

import pytest

from xoinvader import scoreboard
from xoinvader.tests.common import PREFIX


SCOREBOARD_DEFAULTS = os.path.join(PREFIX, "scoreboard_defaults")
"""Contains scoreboard stub."""

SCOREBOARD_EMPTY = os.path.join(PREFIX, "scoreboard_empty")
"""Empty scoreboard file."""

SCOREBOARD_NONEXISTENT = os.path.join(PREFIX, "scoreboard_nonexistent")
"""No such file."""


# pylint: disable=redefined-outer-name
@pytest.fixture()
def mock_scorepath(monkeypatch):
    """Fixture to mock Settings.path.scoreboard entry and revert it back."""

    def inner(path):
        """Inner routine.

        :param str path: new path to set
        """

        mocked = scoreboard.Settings.fullcopy()
        mocked.path.scoreboard = path
        monkeypatch.setattr(scoreboard, "Settings", mocked)

    return inner


def test_ensure(tmpdir, mock_scorepath):
    """xoinvader.scoreboard.ensure()."""

    datadir = tmpdir.mkdir("data")
    scorefile = datadir.join("scoreboard")
    # Check that file doesn't exist
    assert not scorefile.check()

    mock_scorepath(str(scorefile))

    scoreboard.ensure()
    # scoreboard.ensure() creates placeholder
    assert scorefile.check()
    assert list(scoreboard.items()) == scoreboard.DEFAULTS
    scoreboard.add("test", 9000)  # modify to destinguish hash of default file
    scorehash = scorefile.computehash()

    # Second checks that file wasn't recreated
    scoreboard.ensure()
    assert scorehash == scorefile.computehash()

    # scoreboard.ensure() also must create directory for the scoreboard file
    datadir.remove()
    assert not scorefile.check()
    scoreboard.ensure()
    assert scorefile.check()


@pytest.mark.parametrize(("path", "expected"), (
    (SCOREBOARD_EMPTY, []),
    (SCOREBOARD_NONEXISTENT, []),
    (SCOREBOARD_DEFAULTS, scoreboard.DEFAULTS),
))
def test_items(path, expected, mock_scorepath):
    """xoinvader.scoreboard.items()."""

    mock_scorepath(path)
    assert list(scoreboard.items()) == expected


def test_add(tmpdir, mock_scorepath):
    """xoinvader.scoreboard.add()."""

    mock_scorepath(str(tmpdir.mkdir("data").join("scoreboard")))
    scoreboard.add("test", 1000)
    assert ("test", 1000) in list(scoreboard.items())

    scoreboard.add("test", 2000)
    items = list(scoreboard.items())
    assert ("test", 1000) in items
    assert ("test", 2000) in items


def test_lowest(mock_scorepath):
    """xoinvader.scoreboard.lowest()."""

    mock_scorepath(SCOREBOARD_DEFAULTS)
    assert scoreboard.lowest() == min(scoreboard.DEFAULTS,
                                      key=itemgetter(1))[1]

    mock_scorepath(SCOREBOARD_EMPTY)
    assert scoreboard.lowest() == 0


def test_highest(mock_scorepath):
    """xoinvader.scoreboard.highest()."""

    mock_scorepath(SCOREBOARD_DEFAULTS)
    assert scoreboard.highest() == max(scoreboard.DEFAULTS,
                                       key=itemgetter(1))[1]

    mock_scorepath(SCOREBOARD_EMPTY)
    assert scoreboard.highest() == 0
