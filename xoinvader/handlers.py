import os
import sys

from xoinvader.curses_utils import deinit_curses


K_Q = ord("q")
K_E = ord("e")
K_A = ord("a")
K_D = ord("d")
K_R = ord("r")
K_SPACE = ord(" ")
K_ESCAPE = 27


class Command(object):
    def execute(self, actor):
        raise NotImplementedError


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

class ExitGameCommand(Command):
    def execute(self, actor):
        deinit_curses(actor)
        sys.exit(os.EX_OK)

class ToMainMenuCommand(Command):
    def execute(self, actor):
        actor.owner.state = "MainMenuState"

class ToInGameCommand(Command):
    def execute(self, actor):
        actor.owner.state = "InGameState"


class Handler(object):
    """
    Base game handler.

    Provides almost nothing.
#    Executes corresponding to input Command.execute(actor) stored in map.

    :_owner : pointer to master State instance;
    :_screen : pointer to State's curses.Window instance;
    :_actor : pointer to State's actor instance;
#    :_command_map : maps key to Command instance.
    """
    def __init__(self, owner):
        self._owner = owner
        self._screen = owner.screen
        self._actor = owner.actor

#        self._command_map = {}

    def handle(self):
        raise NotImplementedError


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
            if isinstance(cmd, ExitGameCommand):
                cmd.execute(self._screen)
            elif isinstance(cmd, ToMainMenuCommand):
                cmd.execute(self._owner)
            else:
                cmd.execute(self._actor)


class MainMenuInputHandler(Handler):
    def __init__(self, owner):
        super(MainMenuInputHandler, self).__init__(owner)

        self._command_map = {
            K_ESCAPE : ToInGameCommand(),
            K_R : ExitGameCommand()
        }

    def handle(self):
        key = self._screen.getch()
        cmd = self._command_map.get(key, None)
        if cmd:
            if isinstance(cmd, ExitGameCommand):
                cmd.execute(self._screen)
            elif isinstance(cmd, ToInGameCommand):
                cmd.execute(self._owner)
            else:
                cmd.execute(self._actor)


class EventHandler(Handler):
    def __init__(self, owner):
        super(EventHandler, self).__init__(owner)

        self.input_handler = None

    def handle(self):
        raise NotImplementedError


class InGameEventHandler(Handler):
    def __init__(self, owner):
        super(InGameEventHandler, self).__init__(owner)

        self._input_handler = InGameInputHandler(owner)

    def handle(self):
        self._input_handler.handle()
        # Some other event logic

class MainMenuEventHandler(Handler):
    def __init__(self, owner):
        super(MainMenuEventHandler, self).__init__(owner)

        self._input_handler = MainMenuInputHandler(owner)

    def handle(self):
        self._input_handler.handle()
        # Some other event stuff
