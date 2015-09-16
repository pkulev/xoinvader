"""Base class for game application."""

import os
import time

from xoinvader.common import Settings
# TODO: Think about protocol between Application and SettingsManager


class Application(object):
    """Base class for game applications.

    :param startup_args: arguments for passing to game settings
    :type startup_args: dict
    """

    def __init__(self, startup_args=None):
        self._state = None
        self._states = {}
        # ms per frame
        self._mspf = None
        self._running = False

        if startup_args:
            self._update_settings(startup_args)

    def _update_settings(self, args):
        """Update system settings from startup arguments.

        :param args: arguments
        :type args: dict
        """
        for arg, val in args.items():
            if arg in Settings.system:
                Settings.system[arg] = val
            else:
                raise KeyError("No such argument: '%s'." % arg)

    @property
    def running(self):
        """Is game running or not.

        :getter: get application status
        :type: boolean
        """
        return self._running

    @property
    def state(self):
        """Current state.

        :getter: Return current state
        :setter: Set current state
        :type: string
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

    def stop(self):
        """Stop application."""
        self._running = False

    def loop(self):
        """Start main application loop.

        :return: execution status code
        :rtype: integer
        """
        if self._state:
            self._running = True
        else:
            raise AttributeError("There is no avalable state.")

        while self._running:
            start_time = time.perf_counter()

            self._state.events()
            self._state.update()
            self._state.render()

            finish_time = time.perf_counter()
            delta = finish_time - start_time
            if delta <= self._mspf:
                time.sleep((self._mspf - delta) / 1000.0)
            else:
                # TODO: Log FPS drawdowns.
                pass

        return os.EX_OK
