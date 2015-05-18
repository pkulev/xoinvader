"""
    Module for common shared objects.
"""
import json
from os.path import dirname

import xoinvader
from xoinvader.settings import Settings as Entry
from xoinvader.utils import Point


def get_json_config(path):
    """Return Settings object made from json."""
    with open(path) as fd:
        config = Entry(json.load(fd))
    return config


__all__ = ["Settings"]

WIDTH = 90
HEIGHT = 34

_ROOT = dirname(xoinvader.__file__)
_CONFIG = _ROOT + "/config"
_RES = _ROOT + "/res"
_SND = _RES + "/snd"

DEFAUT_XOI_SETTINGS = dict(
    layout=dict(
        field=dict(
            border=Point(x=WIDTH, y=HEIGHT),
            player=Point(x=WIDTH // 2, y=HEIGHT - 1),
            edge=Point(x=WIDTH, y=HEIGHT - 1)),

        gui=dict(
            bar=dict(
                health=Point(x=2, y=HEIGHT - 1),
                shield=Point(x=22, y=HEIGHT - 1),
                weapon=Point(x=WIDTH - 18, y=HEIGHT - 1)),
            info=dict(
                weapon=Point(x=44, y=HEIGHT - 1)))),
    path=dict(
        config=dict(
            ships=_CONFIG + "/ships.json",
            weapons=_CONFIG + "/weapons.json"),
        sound=dict(
            weapon=dict(
                Blaster=_SND + "/basic_blaster.ogg",
                Laser=_SND + "/basic_laser.ogg",
                EBlaster=_SND + "/basic_eblaster.ogg",
                UM=_SND + "/basic_um.ogg"),
            ship=dict(
                Playership=(dict(
                    engine=_SND + "/playership_engine.ogg"))))),
    color=dict(
        general=dict(
            normal=None),
        gui=None,
        weapon=None)
)

Settings = Entry(DEFAUT_XOI_SETTINGS)
