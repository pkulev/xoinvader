"""
    Module for common shared objects.
"""


class Settings(object):
    """Container for storing all game settings"""

    def __init__(self):
        self._settings = {}

    def __getattr__(self, name):
        return self._settings[name]

    def __setattr_(self, name, value):
        self._settings[name] = value
