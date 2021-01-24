"""Module for common shared objects."""

import json
import pathlib
from os.path import dirname

import toml

import xoinvader
from xoinvader import constants
from xoinvader.utils import dotdict, Point


def get_json_config(path):
    """Return Settings object made from json.

    :param str path: path to config

    :return xoinvader.utils.dotdict: parsed config
    """

    with open(path) as fd:
        config = dotdict(json.load(fd))
    return config


def get_toml_config(path: str) -> dotdict:
    """Return Settings object made from toml."""

    with open(path) as fd:
        config = dotdict(toml.load(fd))
    return config


def get_config():
    """Return xoinvader configuration."""

    return get_toml_config(_CONFIG / "xoinvader.toml")


def rootify(root, config):
    """Append paths in dict to root.

    :param str root: common root
    :param dict config:

    :return dict: rootified config
    """

    for key, path in config.items():
        if isinstance(path, dict):
            rootify(root, path)
        else:
            config[key] = root / path
    return config


def update_resized(new_x: int, new_y: int):
    """Calculate new borders and stuff and populate config with new values."""

    Settings.layout.field.border = Point(x=new_x, y=new_y)
    Settings.layout.field.camera = Point(x=new_x - 1, y=new_y - 1)
    Settings.layout.field.player = Point(x=new_x // 2, y=new_y - 1)
    Settings.layout.field.edge = Point(x=new_x, y=new_y - 1)

    Settings.layout.gui.bar.health = Point(x=2, y=new_y - 1)
    Settings.layout.gui.bar.shield = Point(x=22, y=new_y - 1)
    Settings.layout.gui.bar.weapon = Point(x=new_x - 18, y=new_y - 1)
    Settings.layout.gui.info.weapon = Point(x=new_x - 47, y=new_y - 1)


__all__ = ["Settings"]

WIDTH = 130
HEIGHT = 40


_ROOT = pathlib.Path(dirname(xoinvader.__file__))
_CONFIG = _ROOT / "config"

DEFAULT_XOI_SETTINGS = {
    "layout": {
        "field": {
            "border": Point(x=WIDTH, y=HEIGHT),
            "camera": Point(x=WIDTH - 1, y=HEIGHT - 1),
            "player": Point(x=WIDTH // 2, y=HEIGHT - 1),
            "edge": Point(x=WIDTH, y=HEIGHT - 1),
        },
        "gui": {
            "bar": {
                "health": Point(x=2, y=HEIGHT - 1),
                "shield": Point(x=22, y=HEIGHT - 1),
                "weapon": Point(x=WIDTH - 18, y=HEIGHT - 1),
            },
            "info": {
                "weapon": Point(x=WIDTH - 47, y=HEIGHT - 1),
            }
        }
    },
    "system": {
        "debug": False,
        "encoding": constants.UTF_8,
    },
}

Settings = dotdict(DEFAULT_XOI_SETTINGS)  # pylint: disable=invalid-name


def update_system_settings(args):
    """Update system settings from startup arguments.

    :param dict args: arguments
    """

    for arg, val in args.items():
        if arg in Settings.system:
            Settings.system[arg] = val
        else:
            raise KeyError("No such argument: '{0}'.".format(arg))
