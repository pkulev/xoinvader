"""MainMenuState-related input and event handlers."""

from xoinvader.gui import (
    TextCallbackWidget, TextWidget, MenuItemWidget, PopUpNotificationWidget
)
from xoinvader.keys import K_ENTER, K_ESCAPE, K_R, K_N
from xoinvader.state import State
from xoinvader.utils import Point
from xoinvader.render import render_objects
from xoinvader.handlers import Handler


# pylint: disable=missing-docstring
def exit_game_command(actor):
    actor.owner.stop()


def to_ingame_command(actor):
    actor.owner.state = "InGameState"


def show_popup(actor):
    actor.notify("some_text")


# pylint: disable=too-few-public-methods
class MainMenuInputHandler(Handler):

    def __init__(self, owner):
        super(MainMenuInputHandler, self).__init__(owner)

        self._command_map = {
            K_ESCAPE: to_ingame_command,
            K_R: exit_game_command,
            K_N: show_popup
        }

    def handle(self):
        key = self._screen.getch()
        command = self._command_map.get(key)
        if command:
            if command in [exit_game_command, to_ingame_command, show_popup]:
                command(self._owner)
            else:
                command(self._actor)


# pylint: disable=too-few-public-methods
class MainMenuEventHandler(Handler):

    def __init__(self, owner):
        super(MainMenuEventHandler, self).__init__(owner)

        self._input_handler = MainMenuInputHandler(owner)

    def handle(self):
        self._input_handler.handle()
        # Some other event stuff


# Compound renderable object
# Contains renderables as InGame state contains.
# Or PlayerShip object contains weapons.
class Menu(object):
    """
    Represents menu.

    Keeps MenuItemWidget : owner.method mapping.
    Actor of any game menu state.
    """

    def __init__(self, items=None):
        self._items = items if items else list()

    def move_up(self):
        pass

    def move_down(self):
        pass


# recursion?
class SubMenu(Menu):
    pass


class MainMenuState(State):

    def __init__(self, owner):
        super(MainMenuState, self).__init__(owner)
        self._screen = owner.screen
        self._actor = None  # Should be some of Menu instances?

        self._objects = [
            TextWidget(Point(4, 4), "Whoooch"),
            MenuItemWidget(Point(10, 10), "First menu item"),
            MenuItemWidget(Point(10, 11), "Second menu item")
        ]
        self._objects[1].select()

        self._current_menu = None
        self._events = MainMenuEventHandler(self)

    def notify(self, text, pos=Point(15, 15)):
        self._objects.append(
            PopUpNotificationWidget(
                pos, text or "ololo",
                callback=self._objects.remove))

#   def register_menu_item(self, caption, item_action_list):
    def events(self):
        self._events.handle()

    def update(self):
        for o in self._objects:
            o.update()

    def render(self):
        self._screen.erase()
        self._screen.border(0)
        # render_objects(self._actor.get_objects, self._screen)
        render_objects(self._objects, self._screen)


# pylint: disable=too-few-public-methods
class GameOverInputHandler(Handler):

    def __init__(self, owner):
        super(GameOverInputHandler, self).__init__(owner)

        self._command_map = {
            K_ESCAPE: exit_game_command,
            K_ENTER: exit_game_command,
        }

    def handle(self):
        key = self._screen.getch()
        command = self._command_map.get(key)
        if command:
            if command in [exit_game_command, to_ingame_command, show_popup]:
                command(self._owner)
            else:
                command(self._actor)


# pylint: disable=too-few-public-methods
class GameOverEventHandler(Handler):

    def __init__(self, owner):
        super(GameOverEventHandler, self).__init__(owner)

        self._input_handler = GameOverInputHandler(owner)

    def handle(self):
        self._input_handler.handle()
        # Some other event stuff


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
        self._events = GameOverEventHandler(self)

    def score_callback(self):
        return self._score

    def trigger(self, score):
        """Trigger the state and pass the score info to it.

        :param int score: last player score
        """

        self._score = self._score.format(score)

    def events(self):
        self._events.handle()

    def update(self):
        for o in self._objects:
            o.update()

    def render(self):
        self._screen.erase()
        self._screen.border(0)
        render_objects(self._objects, self._screen)
