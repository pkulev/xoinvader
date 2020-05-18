"""XOInvader styles."""

from eaf.meta import Singleton


class Style(metaclass=Singleton):
    """Container for style mappings."""

    def __init__(self):
        self._style = {
            "gui": {},
            "obj": {},
        }

    def init_styles(self, palette):
        """Initialize styles."""

        self.gui["normal"] = palette.ui_norm
        self.gui["yellow"] = palette.ui_yellow
        self.gui["dp_blank"] = palette.dp_blank
        self.gui["dp_ok"] = palette.dp_ok
        self.gui["dp_middle"] = palette.dp_middle
        self.gui["dp_critical"] = palette.dp_critical
        self.gui["sh_ok"] = palette.sh_ok
        self.gui["sh_mid"] = palette.sh_mid

    def __getattr__(self, name):
        return self._style[name]
