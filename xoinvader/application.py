"""Base class for game application."""


import os
import time

import pygame

import xoinvader.curses_utils
from xoinvader.constants import DEFAULT_FPS, SECOND_MILLISECONDS
from xoinvader.common import Settings, update_system_settings


# TODO: implement proper choosing by env
def get_application():
    """Application class getter.

    :return: application class based on environment
    """
    return CursesApplication


class Application(object):
    """Base application class for backend-specific application classes.

    Provides state primitive mechanism and some useful getters/setters.
    """

    def __init__(self, startup_args=None):
        self._state = None
        self._states = {}
        self._screen = None
        self._fps = DEFAULT_FPS
        self._running = False

        if startup_args:
            update_system_settings(startup_args)

    @property
    def state(self):
        """Current state.

        :getter: Return current state
        :setter: Set current state
        :type: str
        """
        if self._state:
            return self._state.__class__.__name__
        else:
            raise AttributeError("There is no available state.")

    @state.setter
    def state(self, name):
        if name in self._states:
            self._state = self._states[name]
        else:
            raise KeyError("No such state: '{0}'.".format(name))

    def register_state(self, state):
        """Add new state and initiate it with owner.

        :param state: state class to register
        :type state: :class:`xoinvader.state.State`
        """
        name = state.__name__
        self._states[name] = state(self)
        if len(self._states) == 1:
            self._state = self._states[name]

    @property
    def fps(self):
        """Frames per second.

        :getter: yes
        :setter: yes
        :type: int
        """
        return self._fps

    @fps.setter
    def fps(self, val):
        self._fps = int(val)

    @property
    def running(self):
        """Is game running or not.

        :getter: get application status
        :type: bool
        """
        return self._running

    @property
    def screen(self):
        """Application's screen Surface.

        :getter: yes
        :setter: no
        :type: class::`curses.Window` or class::`pygame.display.Surface`
        """
        return self._screen

    def stop(self):
        """Stop application."""
        self._running = False


class CursesApplication(Application):
    """Curses powered application class, default fallback backend.

    :param dict startup_args: arguments for passing to game settings
    """

    def __init__(self, startup_args=None):
        super(CursesApplication, self).__init__()

        self._screen = xoinvader.curses_utils.create_window(
            ncols=Settings.layout.field.border.x,
            nlines=Settings.layout.field.border.y)

    def set_caption(self, caption, icontitle=None):
        """Set window caption.

        :param caption: window caption
        :type caption: str

        :param icontitle: short title
        :type icontitle: str
        """
        # Maybe we can update text via terminal API
        pass

    # TODO: implement
    # def _tick(self):
    #     """Update clock."""
    #     self._clock.tick(self._fps)

    def loop(self):
        """Start main application loop.

        :return: execution status code
        :rtype: int
        """
        if self._state:
            self._running = True
        else:
            raise AttributeError("There is no avalable state.")

        ms_per_frame = 1 / self._fps * 1000.0

        while self._running:
            start_ms = time.perf_counter()
            self._state.events()
            self._state.update()
            self._state.render()

            finish_ms = time.perf_counter()
            current_frame_ms = finish_ms - start_ms
            next_s = (ms_per_frame - current_frame_ms) / SECOND_MILLISECONDS

            # TODO: log or warn user
            if current_frame_ms <= ms_per_frame:
                time.sleep(next_s)

        return os.EX_OK


class PygameApplication(Application):
    """Pygame powered application backend.

    :param resolution: surface resolution
    :type resolution: (int, int)

    :param flags: collection of additional options
    :type flags: int (bitmask)

    :param depth: number of bits to use for color
    :type depth: int
    """

    def __init__(self, resolution=(0, 0), flags=0, depth=0):
        super(PygameApplication, self).__init__()

        self._screen = pygame.display.set_mode(resolution, flags, depth)

        self._clock = pygame.time.Clock()

    @staticmethod
    def set_caption(caption, icontitle=""):
        """Set window caption.

        :param caption: window caption
        :type caption: str

        :param icontitle: short title
        :type icontitle: str
        """
        pygame.display.set_caption(caption, icontitle)

    def _tick(self):
        """Update clock."""
        self._clock.tick(self._fps)

    def loop(self):
        """Start main application loop.

        :return: execution status code
        :rtype: int
        """
        if self._state:
            self._running = True
        else:
            raise AttributeError("There is no avalable state.")

        while self._running:
            self._state.events()
            self._state.update()
            self._state.render()

            pygame.display.update()
            self._tick()

        pygame.quit()
        return os.EX_OK
