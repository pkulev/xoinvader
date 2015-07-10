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

class InGame(State):
    def __init__(self, owner):
        super(InGame, self).__init__(owner)
        self._objects = []

    def add_object(self, obj):
        self._objects.append(obj)

    def handle_event(self, event):
        raise NotImplementedError

    def events(self):
        # for event in xoinvader.messageBus.get():
        key = self._screen.getch()
#        if 

class MainMenu(State):
    def __init__(self, owner):
	super(MainMenu, self).__init__(owner)
	self._items = {
	    "New Game": 1,
	    "Continue": 2,
	    "Exit": 3}
	self._currentMenu = None

#    def register_menu_item(self, caption, item_action_list):
    def events(self):
	key = self._screen.getch()
	if key == 27:
	    pos = self._screen.getyx()
	    self._screen.addstr(50,50, str(pos))

    def update(self):
	pass

    def render(self):
	pass
