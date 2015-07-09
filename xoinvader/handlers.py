import os
import sys

from xoinvader.curses_utils import deinit_curses


KEY = "KEY"
K_Q = ord("q")
K_E = ord("e")
K_A = ord("a")
K_D = ord("d")
K_R = ord("r")
K_SPACE = ord(" ")
K_ESCAPE = 27


class Command(object):
    def execute(self, actor):
        pass

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

class ExitGameCommand(Command):
    def execute(self, actor):
        deinit_curses(actor)
        sys.exit(os.EX_OK)


class InputHandler(object):
    def __init__(self):
        self._button_map = {
            K_A : MoveLeftCommand(),
            K_D : MoveRightCommand(),
            K_E : NextWeaponCommand(),
            K_Q : PrevWeaponCommand(),
            K_SPACE : ToggleFireCommand(),
            K_ESCAPE : ExitGameCommand()
        }

    def handle(self, input):
        return self._button_map.get(input, None)


class EventHandler(object):
    def __init__(self, screen, actor):
        self.input_handler = InputHandler()
        self._screen = screen
        self._actor = actor

    def handle(self):
        key = self._screen.getch()
        cmd = self.input_handler.handle(key)
        if cmd:
            cmd.execute(self._screen if isinstance(cmd, ExitGameCommand)
                        else self._actor)
