"""MainMenuState-related input and event handlers."""

from xoinvader import application
from xoinvader.gui import (
    TextCallbackWidget, TextWidget, MenuItemWidget, PopUpNotificationWidget
)
from xoinvader.handlers import EventHandler
from xoinvader.keys import KEY
from xoinvader.state import State
from xoinvader.utils import Point


class MainMenuState(State):

    def __init__(self, owner):
        super(MainMenuState, self).__init__(owner)
        self._screen = owner.screen
        self._owner = owner
        self._actor = None  # Should be some of Menu instances?

        self.add(TextWidget(Point(4, 4), "Whoooch"))
        self._items = [
            MenuItemWidget(Point(10, 10), "First menu item"),
            MenuItemWidget(Point(10, 11), "Second menu item")
        ]
        self._items[0].select()
        self.add(self._items)

        self._events = EventHandler(self, {
            KEY.ESCAPE: lambda: application.get_current().trigger_state("InGameState"),
            KEY.R: application.get_current().stop,
            KEY.N: lambda: self.notify("This is test notification"),
        })

    def notify(self, text, pos=Point(15, 15)):
        widget = PopUpNotificationWidget(
            pos, text or "ololo")
        widget._callback = lambda: self.remove(widget)
        self.add(widget)

    def events(self):
        self._events.handle()


class GameOverState(State):

    def __init__(self, owner):
        super(GameOverState, self).__init__(owner)
        self._screen = owner.screen
        self._actor = None

        self._score = "Your score: {0}"

        self._objects = [
            TextWidget(Point(4, 4), "Your soul completely lost this time"),
            TextCallbackWidget(Point(4, 5), self.score_callback),
            MenuItemWidget(Point(10, 10), "I agree"),
            MenuItemWidget(Point(10, 11), "No, I want more")
        ]
        self._objects[2].select()
        self._events = EventHandler(self, {
            KEY.ESCAPE: application.get_current().stop,
            # KEY.ENTER: exit_game_command,
        })

    def score_callback(self):
        return self._score

    def trigger(self, score):
        """Trigger the state and pass the score info to it.

        :param int score: last player score
        """

        self._score = self._score.format(score)

    def events(self):
        self._events.handle()
