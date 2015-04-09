"""
    Module for common shared objects.
"""

from os.path import dirname

import xoinvader
from xoinvader.settings import Settings as Entry


__all__ = ["Settings"]

_ROOT = dirname(xoinvader.__file__)
_CONFIG = _ROOT + "/config"


__DEFAUT_XOI_SETTINGS__ = Entry(
    path=Entry(
        config=Entry(
            ships=_CONFIG + "/ships.cfg",
            weapons=_CONFIG + "/weapons.cfg"),
        res=None)
)

Settings = Entry(__DEFAUT_XOI_SETTINGS__)
