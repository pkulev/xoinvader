"""InGameState-specific input/event handlers and commands."""

import curses

from xoinvader.gui import TextWidget, WeaponWidget, Bar
from xoinvader.keys import *
from xoinvader.ship import GenericXEnemy, Playership
from xoinvader.state import State
from xoinvader.utils import Point
from xoinvader.common import Settings
from xoinvader.render import render_objects
from xoinvader.handlers import Handler
from xoinvader.curses_utils import style


def move_left_command(actor):
    actor.move_left()


def move_right_command(actor):
    actor.move_right()


def next_weapon_command(actor):
    actor.next_weapon()


def prev_weapon_command(actor):
    actor.prev_weapon()


def toggle_fire_command(actor):
    actor.toggle_fire()


def take_damage_command(actor):
    actor.take_damage(5)

def switch_actor_command(actor):
    actor._actor, actor._owner.enemy = actor._owner.enemy, actor._actor

def to_mainmenu_command(actor):
    actor.owner.state = "MainMenuState"


class InGameInputHandler(Handler):
    def __init__(self, owner):
        super(InGameInputHandler, self).__init__(owner)

        self._command_map = {
            K_A : move_left_command,
            K_D : move_right_command,
            K_E : next_weapon_command,
            K_Q : prev_weapon_command,
            K_R : take_damage_command,
            K_F : switch_actor_command,
            K_SPACE : toggle_fire_command,
            K_ESCAPE : to_mainmenu_command
        }

    def handle(self):
        key = self._screen.getch()
        command = self._command_map.get(key)
        if command:
            if command is to_mainmenu_command:
                command(self._owner)
            elif command is switch_actor_command:
                command(self)
            else:
                command(self._actor)


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

        self._objects.append(self._actor)

        self._events = InGameEventHandler(self)


        self._objects.extend(self._create_gui())

        self.enemy = GenericXEnemy(Point(x=15, y=3), Settings.layout.field.edge,
                Settings)

        self._objects.append(self.enemy)

    def _create_gui(self):
        return [
            Bar(pos=Settings.layout.gui.bar.health, prefix="Hull: ",
                general_style=curses.A_BOLD, stylemap={
                    lambda val: 70.0 <= val <= 100.0 : style.gui["dp_ok"],
                    lambda val: 35.0 <= val < 70.0 : style.gui["dp_middle"],
                    lambda val: 0.0 <= val < 35.0 : style.gui["dp_critical"]
                }, callback=self._actor.getHullPercentage),
            Bar(pos=Settings.layout.gui.bar.shield, prefix="Shield: ",
                general_style=curses.A_BOLD, stylemap={
                    lambda val: 70.0 <= val <= 100.0 : style.gui["sh_ok"],
                    lambda val: 35.0 <= val < 70.0 : style.gui["sh_mid"],
                    lambda val: 0.0 <= val < 35.0 : style.gui["dp_critical"]
                }, callback=self._actor.getShieldPercentage),
            Bar(pos=Settings.layout.gui.bar.weapon,
                stylemap={
                    lambda val: 0.0 <= val <= 100.0 : style.gui["dp_ok"]
                }, callback=self._actor.getWeaponPercentage),
            WeaponWidget(Settings.layout.gui.info.weapon,
                         self.actor.get_weapon_info)
        ] + [
            TextWidget(Point(2, 0), "Score: %s" % 0),
            TextWidget(Point(Settings.layout.field.edge.x // 2 - 4, 0),
                       "XOInvader", curses.A_BOLD)
        ]

    def events(self):
        self._events.handle()

    def update(self):
        for obj in self._objects:
            obj.update()

    def render(self):
        self._screen.erase()
        self._screen.border(0)

        # FIXME:
        # crutch to render shells
        # TODO:
        # ObjectManager with compound objects support.
        Settings.renderer.render_all(self._screen)
        render_objects(self._objects, self._screen)
        self._screen.refresh()
