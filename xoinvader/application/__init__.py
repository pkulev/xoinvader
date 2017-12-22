"""Base class for game application.

Only one application can exist in one interpreter instance.
"""

from tornado import ioloop

from xoinvader.constants import DEFAULT_FPS, DRIVER_NCURSES, DRIVER_SDL
from xoinvader.common import Settings


class ApplicationNotInitializedError(Exception):
    """Raise when try to get not initialized application."""

    def __init__(self):
        super(ApplicationNotInitializedError, self).__init__(
            "Application not initialized.")


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


class Application(object):
    """Base application class for backend-specific application classes.

    Provides state primitive mechanism and some useful getters/setters.
    """

    __CURRENT_APPLICATION = None
    """Instance of the current application."""

    def __init__(self):
        Application.__CURRENT_APPLICATION = self

        self._state = None
        self._states = {}
        self._screen = None
        self._fps = DEFAULT_FPS
        self._ioloop = ioloop.IOLoop.instance()

        self._pc = ioloop.PeriodicCallback(self.tick, 30, self._ioloop)
        self._pc.start()

    def __del__(self):
        Application.__CURRENT_APPLICATION = None

    def tick(self):
        """Callback to execute at every frame."""

        self._state.events()
        self._state.update()
        self._state.render()

    @classmethod
    def current(cls):
        """Return the current application if exists, raise otherwise."""

        if cls.__CURRENT_APPLICATION:
            return cls.__CURRENT_APPLICATION
        else:
            raise ApplicationNotInitializedError()

    @property
    def state(self):
        """Current state.

        :getter: Return current state
        :setter: Set current state
        :type: :class:`xoinvader.state.State`
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

    def deregister_state(self, name):
        """Remove existing state.

        :param str name: name of state
        """

        state = self._states.pop(name)
        del state

    def trigger_state(self, state, *args, **kwargs):
        """Change current state and pass args and kwargs to it.

        :param str state: state name
        """

        self.state = state
        self.state.trigger(*args, **kwargs)

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
