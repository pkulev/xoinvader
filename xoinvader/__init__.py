"""
    xoinvader
    ~~~~~~~~~

    XO Invader is an ASCII ncurses-based top-down space shooter.

    :copyright: (c) 2017 by Pavel Kulyov.
    :license: MIT, see LICENSE for more details.
"""

from .common import Settings
from .common import update_system_settings as _update_system_settings


__version__ = "0.1.1"


class XOInitializationError(Exception):
    """Basic initialization exception."""
    pass


def init(settings=None):
    """Do engine initialization first.

    :param dict settings:
    """

    # TODO: config-management: update this stub
    try:
        if settings:
            _update_system_settings(settings)
    except Exception as exc:
        print(dir(exc))
        raise XOInitializationError(exc)


__all__ = ["Settings"]
