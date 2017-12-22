"""Provides abstract game state."""


class State(object):
    """Represents game state skeleton.

    .. warning:: implement actor base class

    :param owner: state's owner
    :type owner: `xoinvader.application.Application`
    """

    def __init__(self, owner):
        self._owner = owner
        self._actor = None
        self._screen = None

        # TODO:
        self._music = None

    def postinit(self):
        """Do all instantiations that require prepared State object."""

        pass

    def trigger(self, *args, **kwargs):
        """Common way to get useful information for triggered state."""

        pass

    @property
    def owner(self):
        """State's owner.

        :getter: yes
        :setter: no
        :type: :class:`xoinvader.application.Application`
        """
        return self._owner

    @property
    def actor(self):
        """Controllable object.

        :getter: yes
        :setter: no
        :type: object
        """
        return self._actor

    @property
    def screen(self):
        """Screen for rendering state's objects.

        :getter: yes
        :setter: no
        :type: `curses.Window`
        """
        return self._screen

    def events(self):
        "Event handler, calls by `Application.loop` method."
        raise NotImplementedError

    def update(self):
        "Update handler, calls by `Application.loop` method."
        raise NotImplementedError

    def render(self):
        "Render handler, calls by `Application.loop` method."
        raise NotImplementedError
