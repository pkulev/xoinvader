"""Scoreboard routines.

Scoreboard file is CSV of username,score rows.
If file doesn't exist it will be recreated from default stub.
"""

import csv
import operator
import os

from xoinvader.common import _ROOT, get_config


SCOREBOARD_FILE = _ROOT / get_config().scoreboard


def items() -> list[tuple[str, int]]:
    """Return all scorefile entries.

    :return: (username, score) pairs
    """

    return _load()


def add(username: str, score: int) -> None:
    """Add new entry to scoreboard file, sorted by score.

    :param username: username
    :param score: user score
    """

    scores = items()
    scores.append((username, int(score)))
    scores.sort(key=operator.itemgetter(1))

    _save(scores)


def lowest() -> None:
    """Return lowest result in game.

    :return int: lowest score
    """

    scores = items()
    if scores:
        return min(scores, key=operator.itemgetter(1))[1]
    else:
        return 0


def highest() -> int:
    """Return highest result in game.

    :return int: highest score
    """

    scores = items()
    if scores:
        return max(scores, key=operator.itemgetter(1))[1]
    else:
        return 0


def _load() -> list[tuple[str, int]]:
    """Load scores from scorefile.

    :return: scores
    """

    scores = []

    try:
        with open(SCOREBOARD_FILE) as scorefile:
            for entry in csv.reader(scorefile):
                try:
                    name, score = entry
                    scores.append((name, int(score)))
                except ValueError:
                    # probably CSV is corrupted, skip failure entries
                    pass
    except OSError:
        pass

    return scores


def _save(scores: list[tuple[str, int]]) -> None:
    """Save scores to scorefile.

    :param scores: scores to save
    """

    dirname = os.path.dirname(SCOREBOARD_FILE)

    if not os.path.isdir(dirname):
        os.mkdir(dirname)

    with open(SCOREBOARD_FILE, "w") as scorefile:
        csv.writer(scorefile).writerows(scores)
