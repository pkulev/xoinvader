"""Tests for xoinvader.scoreboard module."""

from operator import itemgetter
import os

import pytest

from xoinvader import scoreboard
from xoinvader.tests.common import PREFIX


SCOREBOARD_DATA = [
    ("most", 1700),
    ("most", 1440),
    ("most", 0),
]
"""Scoreboard test data."""

SCOREBOARD_VALID = os.path.join(PREFIX, "scoreboard_valid")
"""Contains scoreboard valid data."""

SCOREBOARD_EMPTY = os.path.join(PREFIX, "scoreboard_empty")
"""Empty scoreboard file."""

SCOREBOARD_NONEXISTENT = os.path.join(PREFIX, "scoreboard_nonexistent")
"""No such file."""

SCOREBOARD_CORRUPTED = os.path.join(PREFIX, "scoreboard_corrupted")
"""Corrupted, but recoverable scoreboard file."""


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


@pytest.mark.parametrize(("path", "expected"), (
    (SCOREBOARD_EMPTY, []),
    (SCOREBOARD_NONEXISTENT, []),
    (SCOREBOARD_CORRUPTED, SCOREBOARD_DATA),
    (SCOREBOARD_VALID, SCOREBOARD_DATA),
))
def test_items(path, expected, mock_scorepath):
    """xoinvader.scoreboard.items()."""

    mock_scorepath(path)
    assert scoreboard.items() == expected
    assert scoreboard._load() == expected


def test_add(tmpdir, mock_scorepath):
    """xoinvader.scoreboard.add()."""

    mock_scorepath(str(tmpdir.mkdir("data").join("scoreboard")))
    scoreboard.add("test", 1000)
    assert ("test", 1000) in scoreboard.items()

    scoreboard.add("test", 2000)
    items = scoreboard.items()
    assert ("test", 1000) in items
    assert ("test", 2000) in items


def test_lowest(mock_scorepath):
    """xoinvader.scoreboard.lowest()."""

    mock_scorepath(SCOREBOARD_VALID)
    assert scoreboard.lowest() == min(SCOREBOARD_DATA,
                                      key=itemgetter(1))[1]

    mock_scorepath(SCOREBOARD_EMPTY)
    assert scoreboard.lowest() == 0


def test_highest(mock_scorepath):
    """xoinvader.scoreboard.highest()."""

    mock_scorepath(SCOREBOARD_VALID)
    assert scoreboard.highest() == max(SCOREBOARD_DATA,
                                       key=itemgetter(1))[1]

    mock_scorepath(SCOREBOARD_EMPTY)
    assert scoreboard.highest() == 0


def test__save(tmpdir, mock_scorepath):
    """xoinvader.scoreboard._save()."""

    datadir = tmpdir.mkdir("data")
    scorefile = datadir.join("scoreboard")
    # Check that file doesn't exist
    assert not scorefile.check()

    mock_scorepath(str(scorefile))

    scoreboard._save(SCOREBOARD_DATA)
    assert scorefile.check()
    assert scoreboard.items() == SCOREBOARD_DATA

    # scoreboard._save() also must create directory for the scoreboard file
    datadir.remove()
    assert not scorefile.check()
    scoreboard._save(SCOREBOARD_DATA)
    assert scorefile.check()
