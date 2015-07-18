"""Provides abstract game state."""


class State(object):
    """
    Represents game state skeleton.

    Every game state have:
    :actor : controllable object;
    :owner : owner of state, instance of Application;
    :screen : screen, where state draws it's objects.
    """

    def __init__(self, owner):
        self._owner = owner
        self._actor = None
        self._screen = None

        # TODO:
        self._music = None

    @property
    def owner(self):
        return self._owner

    @property
    def actor(self):
        return self._actor

    @property
    def screen(self):
        return self._screen

    def events(self):
        "Event handler, calls by Application.loop method."
        raise NotImplementedError

    def update(self):
        "Update handler, calls by Application.loop method."
        raise NotImplementedError

    def render(self):
        "Render handler, calls by Application.loop method."
        raise NotImplementedError
