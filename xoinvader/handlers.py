"""Base handler class."""

from abc import ABCMeta, abstractmethod

import six


@six.add_metaclass(ABCMeta)
class Handler(object):
    """Base game handler.

    Provides accessing to main State's fields and handle function stub.

    :param :class:`xoinvader.state.State` owner: handler's owner
    """

    def __init__(self, owner):
        self._owner = owner
        self._actor = owner.actor

    @property
    def actor(self):
        """Controllable object.

        :getter: yes
        :setter: no
        :type: object
        """

        return self._actor

    @property
    def owner(self):
        """Handler's owner.

        :getter: yes
        :setter: no
        :type: :class:`xoinvader.state.State`
        """

        return self._owner

    @abstractmethod
    def handle(self):
        """Handle event."""

        pass  # pragma: no cover


# TODO: event-handling: now this is prototype that must be reworked in future
# TODO: remove owner link if it's not needed anymore
class EventHandler(Handler):
    """Base game event handler.

    Handles events using the event queue.
    Provides command mapping manipulations via the default handle() method.
    You must instantiate this class only after application being initialized.
    Application instance has event queue object, that will be used here.

    :param :class:`xoinvader.state.State` owner: handler's owner state
    :param dict command_map: key->command mapping
    """

    def __init__(self, owner, command_map=None):
        super(EventHandler, self).__init__(owner)

        self._command_map = command_map or {}
        # TODO: implement proper queue object
        self._event_queue = owner.app.event_queue

    # TODO: event-handling: I think we need some global event bus in whole
    #       application.
    def event_queue(self):
        """Event queue stub."""

        return [("KEY_PRESS", self.get_input())]

    # TODO: event-handling: abstract getting input from curses
    def get_input(self):
        """Get input from keyboard."""

        return self._event_queue.getch()

    def handle(self):
        """Handle input event."""

        for event in self.event_queue():
            if event[0] == "KEY_PRESS":
                command = self._command_map.get(event[1])
                if callable(command):
                    command()
            else:
                raise ValueError("Unknown event type: {0}".format(event[0]))
