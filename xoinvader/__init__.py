"""
    xoinvader
    ~~~~~~~~~

    XO Invader is an ASCII ncurses-based top-down space shooter.

    :copyright: (c) 2016 by Pavel Kulyov.
    :license: GPL, see LICENSE for more details.
"""

from .common import update_system_settings


class XOInitializationError(Exception):
    pass


def init(settings=None):
    """Do engine initialization first.

    :param dict settings:
    """

    # TODO: config-management: update this stub
    try:
        if settings:
            update_system_settings(settings)
    except Exception as exc:
        print(dir(exc))
        raise XOInitializationError(exc)

