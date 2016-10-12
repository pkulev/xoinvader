"""
    Module for handling settings.
"""


class dotdict(dict):  # pylint: disable=invalid-name
    """Container for dot elements access."""

    def __init__(self, *args, **kwargs):
        super(dotdict, self).__init__(*args, **kwargs)
        self.__dict__ = self
        self._wrap_nested()

    def _wrap_nested(self):
        """Wrap nested dicts for deep dot access."""
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = dotdict(value)
