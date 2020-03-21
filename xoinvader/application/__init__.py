"""Xoinvader application routines."""

from eaf.app import Application


# TODO: drop backward compatibility
def get_current():
    """Current application getter.

    :return: current application object
    """

    return Application.current()


from .ncurses_app import CursesApplication


