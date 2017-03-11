"""Base handler class."""


# pylint: disable=too-few-public-methods
class Command(object):
    """Base command class."""

    def execute(self, actor):
        """Execute command with actor.

        :param actor: actor
        :type: actor: object

        .. note:: Make actor base class.
        """
        raise NotImplementedError


class Handler(object):
    """
    Base game handler.

    Provides accessing to main State's fields and handle function stub.

    :param owner: handler's owner
    :type owner: :class:`xoinvader.state.State`
    """

    def __init__(self, owner):
        self._owner = owner
        self._screen = owner.screen
        self._actor = owner.actor

    def handle(self):
        """Handle event."""
        raise NotImplementedError
