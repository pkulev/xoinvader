"""
    Module for handling settings.
"""


def dotdict(*args, **kwargs):
    return Settings(*args, **kwargs)


class Settings(dict):
    """Container for storing all game settings."""
    
    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
        self._wrap_nested()

    def _wrap_nested(self):
        """Wrap nested dicts for deep dot access."""
        for key, value in self.items():
            if type(value) == dict:
                self[key] = Settings(value)

    def __getattr__(self, name):
        return self[name]

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__