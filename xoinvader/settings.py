"""
    Module for handling settings.
"""


class Settings(dict):
    """Container for storing all game settings."""
    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
    def __getattr__(self, name):
        return self[name]

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
