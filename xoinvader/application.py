"""Base class for game application."""


import os
import sys

import pygame

import xoinvader.curses_utils
import xoinvader.pygame_utils
from xoinvader.constants import DEFAULT_FPS
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
        """Setter."""
        if name in self._states:
            self._state = self._states[name]
        else:
            raise KeyError("No such state: '{0}'.".format(name))

    @property
    def states(self):
        """State names to State classes mapping.

        :getter: yes
        :setter: no
        :type: dict
        """
        return self._states

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
        """Setter."""
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

    def on_destroy(self):
        """Overload this to do something on destroy."""
        pass

    def destroy(self, exit_code=os.EX_OK):
        """Aggressively destroy application and exit with given exit code.

        Normally Application lets the loop finish current iteration and
        after it deinits graphic backend and returns EX_OK. In this case
        Application deinits backend immidiately and exits with given exit code.

        :param integer exit_code: exit code for exit with
        """
        self.stop()
        self.on_destroy()
        sys.exit(exit_code)


class CursesApplication(Application):
    """Curses powered application class, default fallback backend.

    :param dict startup_args: arguments for passing to game settings
    """

    def __init__(self, startup_args=None):
        super(CursesApplication, self).__init__()

        self._screen = xoinvader.curses_utils.create_window(
            ncols=Settings.layout.field.border.x,
            nlines=Settings.layout.field.border.y)

        self._clock = xoinvader.curses_utils.get_clock()

    def set_caption(self, caption, icontitle=None):
        """Set window caption.

        :param caption: window caption
        :type caption: str

        :param icontitle: short title
        :type icontitle: str
        """
        # Maybe we can update text via terminal API
        pass

    def stop(self):
        """Stop the loop."""
        xoinvader.curses_utils.deinit_curses(self._screen)
        super(CursesApplication, self).stop()

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

            self._tick()

        return os.EX_OK

    def _tick(self):
        """Update clock."""
        self._clock.tick(self._fps)


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
        self._clock = xoinvader.pygame_utils.get_clock()

    def set_caption(self, caption, icontitle=""):
        """Set window caption.

        :param caption: window caption
        :type caption: str

        :param icontitle: short title
        :type icontitle: str
        """
        if self._screen:
            pygame.display.set_caption(caption, icontitle)

    def _tick(self):
        """Update clock."""
        self._clock.tick(self._fps)

    def on_destroy(self):
        """Deinit pygame."""
        pygame.quit()

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
