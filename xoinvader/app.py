"""XOInvader game application class."""

from xoinvader import Settings
from xoinvader.ingame import InGameState
from xoinvader.menu import PauseMenuState, GameOverState
from xoinvader.style import Style

from xo1 import Application, Palette


class XOInvader(Application):
    """XOInvader game application class."""

    def __init__(self):

        palette = Palette(
            [
                # User interface colors
                ("ui_norm", Palette.COLOR_WHITE, Palette.COLOR_BLACK),
                ("ui_yellow", Palette.COLOR_YELLOW, Palette.COLOR_BLACK),
                # Damage panel colors
                ("dp_blank", Palette.COLOR_BLACK, Palette.COLOR_BLACK),
                ("dp_ok", Palette.COLOR_GREEN, Palette.COLOR_BLACK),
                ("dp_middle", Palette.COLOR_YELLOW, Palette.COLOR_BLACK),
                ("dp_critical", Palette.COLOR_RED, Palette.COLOR_BLACK),
                ("sh_ok", Palette.COLOR_BLUE, Palette.COLOR_BLACK),
                ("sh_mid", Palette.COLOR_CYAN, Palette.COLOR_BLACK),
                # Weapon's charge colors
                ("blaster", Palette.COLOR_GREEN, Palette.COLOR_BLACK),
                ("laser", Palette.COLOR_BLACK, Palette.COLOR_RED),
                ("um", Palette.COLOR_MAGENTA, Palette.COLOR_BLACK),
                ("B", Palette.COLOR_BLACK),
                ("b", Palette.COLOR_BLUE),
                ("c", Palette.COLOR_CYAN),
                ("g", Palette.COLOR_GREEN),
                ("m", Palette.COLOR_MAGENTA),
                ("r", Palette.COLOR_RED),
                ("w", Palette.COLOR_WHITE),
                ("y", Palette.COLOR_YELLOW),
                ("d", Palette.COLOR_DEFAULT),
            ],
            attr_map={
                "B": Palette.A_BOLD,
                "b": Palette.A_BLINK,
                "n": Palette.A_NORMAL,
                "r": Palette.A_REVERSE,
            },
        )

        super().__init__(
            x=Settings.layout.field.border.x,
            y=Settings.layout.field.border.y,
            palette=palette,
            title="XOInvader",
        )

        Style().init_styles(palette)

        self.register(InGameState)
        self.register(PauseMenuState)
        self.register(GameOverState)


def current():
    return XOInvader.current()
