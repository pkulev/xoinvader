"""
    Module for common shared objects.
"""

from os.path import dirname

import xoinvader
from xoinvader.settings import Settings as Entry


__all__ = ["Settings"]

_ROOT = dirname(xoinvader.__file__)
_CONFIG = _ROOT + "/config"


DEFAUT_XOI_SETTINGS = dict(
    path=dict(
        config=dict(
            ships=_CONFIG + "/ships.cfg",
            weapons=_CONFIG + "/weapons.cfg"),
        res=None)
)

Settings = Entry(True, DEFAUT_XOI_SETTINGS)
