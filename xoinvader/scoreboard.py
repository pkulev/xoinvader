"""Scoreboard routines.

Scoreboard file is CSV of username,score rows.
If file doesn't exist it will be recreated from default stub.
"""

import operator
import os
import csv

from xoinvader.common import Settings


DEFAULTS = [
    ("most", 1700),
    ("most", 1440),
    ("most", 0),
]
"""Default scoreboard placeholder."""


def ensure():
    """Ensure that path and file exist, create default stub if not."""

    dirname = os.path.dirname(Settings.path.scoreboard)

    if not os.path.isdir(dirname):
        os.mkdir(dirname)

    if not os.path.isfile(Settings.path.scoreboard):
        with open(Settings.path.scoreboard, "w") as scores:
            csv.writer(scores).writerows(DEFAULTS)


def items():
    """Generator, yield scoreboard entries one by one.

    :return tuple(str, int): (username, score)
    """

    ensure()
    try:
        with open(Settings.path.scoreboard) as scores:
            for name, score in csv.reader(scores):
                yield name, int(score)
    except IOError:
        raise StopIteration


def add(username, score):
    """Add new entry to scoreboard file, sorted by score.

    :param str username: username
    :param int score: user score
    """

    ensure()
    data = list(items())
    data.append((username, score))
    data.sort(key=operator.itemgetter(1))

    with open(Settings.path.scoreboard, "w") as scores:
        csv.writer(scores).writerows(data)


def lowest():
    """Return lowest result in game.

    :return int: lowest score
    """

    return min(list(items()) or [("nobody", 0)], key=operator.itemgetter(1))[1]


def highest():
    """Return highest result in game.

    :return int: highest score
    """

    return max(list(items()) or [("nobody", 0)], key=operator.itemgetter(1))[1]
