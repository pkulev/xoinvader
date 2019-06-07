"""
    xoinvader
    ~~~~~~~~~

    XO Invader is an ASCII ncurses-based top-down space shooter.

    :copyright: (c) 2017 by Pavel Kulyov.
    :license: MIT, see LICENSE for more details.
"""

import locale

from .common import Settings
from .common import update_system_settings as _update_system_settings
from .utils import setup_logger


__version__ = "0.1.2"


class XOInitializationError(Exception):
    """Basic initialization exception."""
    pass


def setup_locale(settings):
    """Setup locale settings.

    :param dict settings:

    :return dict: updated settings
    """

    locale.setlocale(locale.LC_ALL, "")
    encoding = locale.getpreferredencoding()
    settings["encoding"] = encoding
    return settings


def init(settings=None):
    """Do engine initialization first.

    :param dict settings:
    """

    if settings is None:
        settings = {}

    try:
        settings = setup_locale(settings)
        log = setup_logger(
            "xoinvader", settings.get("debug", Settings.system.debug))
    except Exception as exc:
        raise XOInitializationError(exc)

    log.debug("Updating engine settings")

    # TODO: config-management: update this stub
    try:
        if settings:
            _update_system_settings(settings)
    except Exception as exc:
        log.exception(exc)
        raise XOInitializationError(exc)


__all__ = ["Settings"]
