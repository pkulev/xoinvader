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

class TestCommand(Command):
    def exectute(self, actor):
        actor._owner.state = "MainMenuState"

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

class _InputHandler(object):
    def __init__(self):
        self._button_map = {}

    def handle(self, input):
        raise NotImplementedError

class InputHandler(_InputHandler):
    def __init__(self):
        self._button_map = {
            K_A : MoveLeftCommand(),
            K_D : MoveRightCommand(),
            K_E : NextWeaponCommand(),
            K_Q : PrevWeaponCommand(),
            K_R : TakeDamageCommand(),
            K_SPACE : ToggleFireCommand(),
            K_ESCAPE : ExitGameCommand()
        }

    def handle(self, input):
        return self._button_map.get(input, None)


class EventHandler(object):
    def __init__(self, owner):
        self.input_handler = InputHandler()
        self._owner = owner
        self._screen = self._owner.screen
        self._actor = self._owner.actor

    def handle(self):
        key = self._screen.getch()
        cmd = self.input_handler.handle(key)
#        if cmd:
#            cmd.execute(self._screen if isinstance(cmd, ExitGameCommand)
#else self._actor)
        if cmd:
            if isinstance(cmd, ExitGameCommand):
                cmd.execute(self._screen)
            elif isinstance(cmd, TestCommand):
                cmd.execute(self._owner._owner)
            else:
                cmd.execute(self._actor)
