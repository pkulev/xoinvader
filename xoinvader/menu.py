"""MainMenuState-related input and event handlers."""

from eaf.state import State

from xoinvader.gui import (
    MenuItemContainer,
    MenuItemWidget,
    PopUpNotificationWidget,
    TextCallbackWidget,
    TextWidget,
)
from xoinvader.handlers import EventHandler
from xoinvader.keys import KEY
from xoinvader.utils import Point


class PauseMenuState(State):
    def __init__(self, app):
        super().__init__(app)

        self.add(TextWidget(Point(4, 4), "Pause"))
        self._items = MenuItemContainer(
            [
                MenuItemWidget(
                    Point(10, 10),
                    "Continue",
                    template=("=> ", ""),
                    action=lambda: app.current().trigger_state("InGameState"),
                ),
                MenuItemWidget(
                    Point(10, 11),
                    "Quit",
                    template=("=> ", ""),
                    action=app.current().stop,
                ),
            ]
        )
        self._items.select(0)
        self.add(self._items)

        self._events = EventHandler(
            self,
            {
                KEY.ESCAPE: lambda: app.current().trigger_state("InGameState"),
                KEY.SPACE: self._items.do_action,
                KEY.W: self._items.prev,
                KEY.S: self._items.next,
                KEY.N: lambda: self.notify("This is test notification"),
            },
        )

    def notify(self, text, pos=Point(15, 15)):
        self.add(
            PopUpNotificationWidget(
                pos, text, callback=lambda w: self.remove(w)
            )
        )

    def events(self):
        self._events.handle()


class GameOverState(State):
    def __init__(self, app):
        super().__init__(app)

        self._score = "Your score: {0}"

        self.add(
            TextWidget(Point(4, 4), "I was too tired and scared to continue...")
        )
        self.add(TextCallbackWidget(Point(4, 5), self.score_callback))

        self._items = MenuItemContainer(
            [
                MenuItemWidget(
                    Point(10, 10),
                    "I must to continue my revenge!",
                    action=lambda: app.current().trigger_reinit("InGameState"),
                ),
                MenuItemWidget(
                    Point(10, 11),
                    "No! I want to go home!",
                    action=app.current().stop,
                ),
            ]
        )
        self.add(self._items)
        self._items.select(0)

        self._events = EventHandler(
            self,
            {
                KEY.SPACE: self._items.do_action,
                KEY.W: self._items.prev,
                KEY.S: self._items.next,
            },
        )

    def score_callback(self):
        return self._score

    def trigger(self, score):
        """Trigger the state and pass the score info to it.

        :param int score: last player score
        """

        self._score = self._score.format(score)

    def events(self):
        self._events.handle()
