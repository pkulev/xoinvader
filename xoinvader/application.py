import time


class Application(object):
    def __init__(self, startup_args={}):
        self._state = None
        self._states = {}
        self._mspf = None # ms per frame
        self._running = False

    @property
    def running(self):
        return self._running

    @property
    def state(self):
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
        """Add new state and initiate it with owner."""
        name = state.__name__
        self._states[name] = state(self)
        if len(self._states) == 1:
            self._state = self._states[name]

    def stop(self):
        self._running = False

    def loop(self):
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
                pass # Log FPS drawdowns.
