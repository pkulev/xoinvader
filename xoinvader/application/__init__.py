"""Xoinvader application routines."""

from eaf.app import Application

from xoinvader.constants import DRIVER_NCURSES, DRIVER_SDL
from xoinvader.common import Settings


# TODO: drop backward compatibility
def get_current():
    """Current application getter.

    :return: current application object
    """

    return Application.current()


# TODO: implement proper choosing by env
def get_application_class():
    """Application class getter.

    :return: application class based on environment
    """

    driver_map = {
        DRIVER_NCURSES: get_ncurses_application,
        DRIVER_SDL: get_pygame_application,
    }

    return driver_map[Settings.system.video_driver]()


def get_ncurses_application():
    """Incapsulate ncurses-related stuff.

    :return: CursesApplication class
    """

    from .ncurses_app import CursesApplication

    return CursesApplication


def get_pygame_application():
    """Incapsulate pygame-related stuff.

    :return: PygameApplication class
    """

    from .pygame_app import PygameApplication

    return PygameApplication
