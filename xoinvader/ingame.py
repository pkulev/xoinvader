"""InGameState-specific input/event handlers and commands."""

import curses

from xoinvader.gui import WeaponWidget, Bar
from xoinvader.keys import *
from xoinvader.ship import GenericXEnemy, Playership
from xoinvader.state import State
from xoinvader.utils import Point
from xoinvader.common import Settings
from xoinvader.settings import dotdict
from xoinvader.handlers import Command, Handler
from xoinvader.curses_utils import style


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

        self._actor = Playership(Settings.layout.field.player,
                Settings.layout.field.edge, Settings)

        self.add_object(self._actor)
        Settings.renderer.add_object(self.actor)

        self._events = InGameEventHandler(self)

        # GUI style mapping
        self.gui = dotdict(
                hull=Bar(pos=Settings.layout.gui.bar.health, prefix="Hull: ",
                  stylemap={
                      lambda val: 70.0 <= val <= 100.0 : style.gui["dp_ok"],
                      lambda val: 35.0 <= val < 70.0 : style.gui["dp_middle"],
                      lambda val: 0.0 <= val < 35.0 : style.gui["dp_critical"]
                  }),
            shield=Bar(pos=Settings.layout.gui.bar.shield, prefix="Shield: ",
                    stylemap={
                        lambda val: 70.0 <= val <= 100.0 : style.gui["sh_ok"],
                        lambda val: 35.0 <= val < 70.0 : style.gui["sh_mid"],
                        lambda val: 0.0 <= val < 35.0 : style.gui["dp_critical"]
                    }),
            weapon=Bar(pos=Settings.layout.gui.bar.weapon,
                    stylemap={
                        lambda val: 0.0 <= val <= 100.0 : style.gui["dp_ok"]
                    }),
            weapon_info=WeaponWidget(Settings.layout.gui.info.weapon,
                                  self.actor.get_weapon_info)
        )

        for gui_object in self.gui.values():
            Settings.renderer.add_object(gui_object)

        self.enemy = GenericXEnemy(Point(x=15, y=3), Settings.layout.field.edge,
                Settings)

        Settings.renderer.add_object(self.enemy)

    def add_object(self, obj):
        self._objects.append(obj)

    def handle_event(self, event):
        raise NotImplementedError

    def _update_gui(self):
        self.gui.hull.update(self.actor.getHullPercentage())
        self.gui.shield.update(self.actor.getShieldPercentage())
        self.gui.weapon.update(self.actor.getWeaponPercentage())
        self.gui.weapon_info.update()

    def events(self):
        # for event in xoinvader.messageBus.get():
        self._events.handle()

    def update(self):
        for obj in self._objects:
            obj.update()
        self.enemy.update()
        self._update_gui()

    def render(self):
        self._screen.erase()
        self._screen.border(0)
        self._screen.addstr(0, 2, "Score: %s " % 0)
        self._screen.addstr(0, Settings.layout.field.edge.x // 2 - 4,
                "XOinvader", curses.A_BOLD)

        Settings.renderer.render_all(self._screen)
        self._screen.refresh()
