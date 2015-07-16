from xoinvader.keys import *


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

class ToMainMenuCommand(Command):
    def execute(self, actor):
        actor.owner.state = "MainMenuState"


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


