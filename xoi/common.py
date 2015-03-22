"""
    Module for common shared objects.
"""

class Settings(object):
    def __init__(self):
        self._settings = {}

    def __getattr__(self, name):
        return self._settings[name]

    def __setattr_(self, name, value):
        self._settings[name] = value
