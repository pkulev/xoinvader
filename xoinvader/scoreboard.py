"""Scoreboard routines.

Scoreboard file is CSV of username,score rows.
If file doesn't exist it will be recreated from default stub.
"""

import operator
import os
import csv

from xoinvader.common import Settings


def items():
    """Return all scorefile entries.

    :return [(str, int)]: (username, score) pairs
    """

    return _load()


def add(username, score):
    """Add new entry to scoreboard file, sorted by score.

    :param str username: username
    :param int score: user score
    """

    scores = items()
    scores.append((username, int(score)))
    scores.sort(key=operator.itemgetter(1))

    _save(scores)


def lowest():
    """Return lowest result in game.

    :return int: lowest score
    """

    scores = items()
    if scores:
        return min(scores, key=operator.itemgetter(1))[1]
    else:
        return 0


def highest():
    """Return highest result in game.

    :return int: highest score
    """

    scores = items()
    if scores:
        return max(scores, key=operator.itemgetter(1))[1]
    else:
        return 0


def _load():
    """Load scores from scorefile.

    :return [(str, int)]: scores
    """

    scores = []

    try:
        with open(Settings.path.scoreboard) as scorefile:
            for entry in csv.reader(scorefile):
                try:
                    name, score = entry
                    scores.append((name, int(score)))
                except ValueError:
                    # probably CSV is corrupted, skip failure entries
                    pass
    except IOError:
        pass

    return scores


def _save(scores):
    """Save scores to scorefile.

    :param [(str, int)] scores: scores to save
    """

    dirname = os.path.dirname(Settings.path.scoreboard)

    if not os.path.isdir(dirname):
        os.mkdir(dirname)

    with open(Settings.path.scoreboard, "w") as scorefile:
        csv.writer(scorefile).writerows(scores)
