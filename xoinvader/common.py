"""
    Module for common shared objects.
"""
import json
from os.path import dirname

import xoinvader
from xoinvader.settings import Settings as Entry


def get_json_config(path):
    with open(path) as fd:
        config = Entry(json.load(fd))
    return config


__all__ = ["Settings"]

_ROOT = dirname(xoinvader.__file__)
_CONFIG = _ROOT + "/config"


DEFAUT_XOI_SETTINGS = dict(
    path=dict(
        config=dict(
            ships=_CONFIG + "/ships.json",
            weapons=_CONFIG + "/weapons.json"),
        res=None)
)

Settings = Entry(DEFAUT_XOI_SETTINGS)
