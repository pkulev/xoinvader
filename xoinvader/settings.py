"""
    Module for handling settings.
"""


class Settings(dict):
    """Container for storing all game settings."""
    
    def __init__(self, wrap_nested=False, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
        if wrap_nested:
            self._wrap_nested()

    def _wrap_nested(self):
        for key, value in self.iteritems():
            if type(value) == dict:
                self[key] = Settings(True, value)

    def __getattr__(self, name):
        return self[name]

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
