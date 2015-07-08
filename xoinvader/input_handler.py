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
        actor.exit()


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
