class Command(object):
    def execute(self, actor):
        raise NotImplementedError


class Handler(object):
    """
    Base game handler.

    Provides accessing to main State's fields and handle function stub.

    :_owner : pointer to master State instance;
    :_screen : pointer to State's curses.Window instance;
    :_actor : pointer to State's actor instance;
    """
    def __init__(self, owner):
        self._owner = owner
        self._screen = owner.screen
        self._actor = owner.actor

    def handle(self):
        raise NotImplementedError
