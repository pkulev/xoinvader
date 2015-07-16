""" Provides abstract game state. """


class State(object):
    def __init__(self, owner):
        self._owner = owner
        self._background = None
        self._music = None

    def events(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError
