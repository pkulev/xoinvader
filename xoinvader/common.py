"""
    Module for common shared objects.
"""

# DEPRECATED
class _Settings(object):
    """Container for storing all game settings"""

    def __init__(self):
        self._settings = {}

    def __getattr__(self, name):
        return self._settings[name]

    def __setattr__(self, name, value):
        #self._settings[name] = value
        super(Settings, self).__setattr__(name, value)

__DEFAUT_XOI_SETTINGS__ = dict(
    path = dict(config = None, res = None)
)

class Settings(dict):
    """Container for storing all game settings"""
    def __getattr__(self, name):
        return self[name]

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
