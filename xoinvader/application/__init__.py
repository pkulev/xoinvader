"""Base class for game application."""

from tornado import ioloop

from xoinvader.constants import DEFAULT_FPS, DRIVER_NCURSES, DRIVER_SDL
from xoinvader.common import Settings


_CURRENT_APPLICATION = None
"""Current application instance."""


class ApplicationNotInitializedError(Exception):
    """Raise when try to get not initialized application."""

    def __init__(self):
        super(ApplicationNotInitializedError, self).__init__(
            "Application not initialized.")


def get_current():
    """Current application getter.

    :return: current application object
    """

    if _CURRENT_APPLICATION is not None:
        return _CURRENT_APPLICATION
    else:
        raise ApplicationNotInitializedError()


# TODO: implement proper choosing by env
def get_application():
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


def trigger_state(state, **kwargs):
    """Change current state and pass to it data via kwargs.

    :param str state: state name
    """

    app = get_current()
    app.state = state
    app.state.trigger(**kwargs)


class Application(object):
    """Base application class for backend-specific application classes.

    Provides state primitive mechanism and some useful getters/setters.
    """

    def __init__(self):
        global _CURRENT_APPLICATION
        _CURRENT_APPLICATION = self

        self._state = None
        self._states = {}
        self._screen = None
        self._fps = DEFAULT_FPS
        self._ioloop = ioloop.IOLoop.instance()

        self._pc = ioloop.PeriodicCallback(self.tick, 30, self._ioloop)
        self._pc.start()

    def tick(self):
        """Callback to execute at every frame."""

        self._state.events()
        self._state.update()
        self._state.render()

    @property
    def state(self):
        """Current state.

        :getter: Return current state
        :setter: Set current state
        :type: :class:`xoinvader.application.Application`
        """
        if self._state:
            return self._state
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
        state_object = state(self)
        self._states[name] = state_object
        if len(self._states) == 1:
            self._state = self._states[name]

        # NOTE: State cannot instantiate in State.__init__ objects that
        #       want access to state because there is no instance at creation
        #       moment. For such objects state can declare it's 'postinit'
        #       method.
        state_object.postinit()

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
    def screen(self):
        """Application's screen Surface.

        :getter: yes
        :setter: no
        :type: class::`curses.Window` or class::`pygame.display.Surface`
        """
        return self._screen

    def start(self):
        """Start main application loop."""

        if not self._state:
            raise AttributeError("There is no available state.")

        self._ioloop.start()

    def stop(self):
        """Stop application."""

        self._pc.stop()
        self._ioloop.add_callback(self._ioloop.stop)
