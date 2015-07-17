"""InGameState-specific input/event handlers and commands."""

import curses

from xoinvader.keys import *
from xoinvader.state import State
from xoinvader.common import Settings
from xoinvader.handlers import Command, Handler


class MoveLeftCommand(Command):
    def execute(self, actor):
        actor.move_left()

class MoveRightCommand(Command):
    def execute(self, actor):
        actor.move_right()

class NextWeaponCommand(Command):
    def execute(self, actor):
        actor.next_weapon()

class PrevWeaponCommand(Command):
    def execute(self, actor):
        actor.prev_weapon()

class ToggleFireCommand(Command):
    def execute(self, actor):
        actor.toggle_fire()

class TakeDamageCommand(Command):
    def execute(self, actor):
        actor.take_damage(5)

class ToMainMenuCommand(Command):
    def execute(self, actor):
        actor.owner.state = "MainMenuState"


class InGameInputHandler(Handler):
    def __init__(self, owner):
        super(InGameInputHandler, self).__init__(owner)

        self._command_map = {
            K_A : MoveLeftCommand(),
            K_D : MoveRightCommand(),
            K_E : NextWeaponCommand(),
            K_Q : PrevWeaponCommand(),
            K_R : TakeDamageCommand(),
            K_SPACE : ToggleFireCommand(),
            K_ESCAPE : ToMainMenuCommand()
        }

    def handle(self):
        key = self._screen.getch()
        cmd = self._command_map.get(key, None)
        if cmd:
            if isinstance(cmd, ToMainMenuCommand):
                cmd.execute(self._owner)
            else:
                cmd.execute(self._actor)


class InGameEventHandler(Handler):
    def __init__(self, owner):
        super(InGameEventHandler, self).__init__(owner)

        self._input_handler = InGameInputHandler(owner)

    def handle(self):
        self._input_handler.handle()
        # Some other event logic


class InGameState(State):
    def __init__(self, owner):
        super(InGameState, self).__init__(owner)
        self._objects = []
        self._screen = self._owner.screen
        self._actor = self._owner.actor
        self.add_object(self._actor)

        self._events = InGameEventHandler(self)

    def add_object(self, obj):
        self._objects.append(obj)

    def handle_event(self, event):
        raise NotImplementedError

    def events(self):
        # for event in xoinvader.messageBus.get():
        self._events.handle()

    def update(self):
        for obj in self._objects:
            obj.update()

    def render(self):
        self._screen.erase()
        self._screen.border(0)
        self._screen.addstr(0, 2, "Score: %s " % 0)
        self._screen.addstr(0, Settings.layout.field.edge.x // 2 - 4,
                "XOinvader", curses.A_BOLD)

        Settings.renderer.render_all(self._screen)
        self._screen.refresh()
