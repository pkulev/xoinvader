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


__all__ = ["Settings"]

WIDTH = 90
HEIGHT = 34

_ROOT = pathlib.Path(dirname(xoinvader.__file__))
_CONFIG = _ROOT / "config"

DEFAULT_XOI_SETTINGS = dict(
    layout=dict(
        field=dict(
            border=Point(x=WIDTH, y=HEIGHT),
            camera=Point(x=WIDTH - 1, y=HEIGHT - 1),
            player=Point(x=WIDTH // 2, y=HEIGHT - 1),
            edge=Point(x=WIDTH, y=HEIGHT - 1),
        ),
        gui=dict(
            bar=dict(
                health=Point(x=2, y=HEIGHT - 1),
                shield=Point(x=22, y=HEIGHT - 1),
                weapon=Point(x=WIDTH - 18, y=HEIGHT - 1),
            ),
            info=dict(weapon=Point(x=44, y=HEIGHT - 1)),
        ),
    ),
    path=rootify(_ROOT, get_json_config(_CONFIG / "path.json")),
    system=dict(debug=False, encoding=constants.UTF_8,),
)

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
