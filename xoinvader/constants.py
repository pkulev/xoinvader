"""XOInvader constants."""


DEFAULT_FPS = 60
"""Default frames per second."""


DRIVER_NCURSES = "ncurses"
"""Ncurses video driver."""

DRIVER_SDL = "pygame-sdl"
"""PyGame SDLv1 video driver."""

# TODO: driver-sdl2; RnD this
DRIVER_SDL2 = "pygame-sdl2"
"""PyGame SDLv2 video driver."""

VIDEO_DRIVERS = [
    DRIVER_NCURSES,
    DRIVER_SDL,
    # DRIVER_SDL2,
]
"""Supported video drivers."""


UTF_8 = "UTF-8"
"""UTF-8 encoding."""
