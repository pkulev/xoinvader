class Application(object):
    def __init__(self):
        self._state = None
        self._states = {}

	# Ms per frame
	self._mspf = 16

    def create_window(self):
        pass

    def exit(self):
        pass

    @state.setter
    def state(self, name):
        if name in self._states:
            self._state = self._states[name]
        else:
            raise KeyError("No such state {0}.".format(name))

    def register_state(self, state):
        """Add new state and initiate it with owner."""
	name = state.__class__.__name__
        self._states[name] = state(self)
	if len(self._states) == 1:
	    self._state = self._states[name]

    def loop(self):
        while True:
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
