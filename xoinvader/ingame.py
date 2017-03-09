"""InGameState-specific input/event handlers and commands."""


import curses
import logging

from xoinvader.background import Background
from xoinvader.collision import CollisionManager
from xoinvader.common import Settings
from xoinvader.curses_utils import Style
from xoinvader.gui import TextWidget, WeaponWidget, Bar
from xoinvader.handlers import Handler
from xoinvader.keys import K_A, K_D, K_E, K_F, K_R, K_SPACE, K_ESCAPE, K_Q
from xoinvader.level import Level
from xoinvader.render import render_objects
from xoinvader.ship import GenericXEnemy, Playership
from xoinvader.state import State
from xoinvader.utils import Point


LOG = logging.getLogger(__name__)


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
            K_A: move_left_command,
            K_D: move_right_command,
            K_E: next_weapon_command,
            K_Q: prev_weapon_command,
            K_R: take_damage_command,
            K_F: switch_actor_command,
            K_SPACE: toggle_fire_command,
            K_ESCAPE: to_mainmenu_command
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


class TestLevel(Level):
    def __init__(self, state_object_adder, speed):
        super(TestLevel, self).__init__(speed)
        self._state_add = state_object_adder

        self._player_ship = Playership(
            Settings.layout.field.player, Settings.layout.field.edge)
        self._state_add(self._player_ship)

        self.add_event(1, self.spawn4)
        self.add_event(100, lambda: None)

        self.bg = Background(Settings.path.level1bg, speed=10, loop=True)
        self.bg.start(True)
        self._state_add(self.bg)

    @staticmethod
    def get_keyframes(y_offset, x_start, direction):
        """Generate keyframe list.

        :param int y_offset: y of top left corner of image
        :param int x_start: x level of left corner of image
        :param int direction: -1 or 1, depending of direction of moving: left or
        right
        """

        def new_x(d):
            return x_start - d * direction

        return [
            (0,   Point(x_start,   y_offset)),
            (4.0, Point(x_start, y_offset + 20)),
            (7.0, Point(new_x(30), y_offset + 10)),
        ]

    def spawn4(self):
        right_side = Settings.layout.field.edge.x

        e1 = GenericXEnemy(
            Point(10, 1),
            Settings.layout.field.edge)
        e2 = GenericXEnemy(
            Point(25, 1),
            Settings.layout.field.edge)

        e3 = GenericXEnemy(
            Point(right_side - 10, 1),
            Settings.layout.field.edge)
        e4 = GenericXEnemy(
            Point(right_side - 25, 1),
            Settings.layout.field.edge)

        e1.add_animation(
            "", e1, "_pos", self.get_keyframes(1, 10, 1), interp=True)
        e2.add_animation(
            "", e2, "_pos", self.get_keyframes(1, 20, 1), interp=True)

        e3.add_animation(
            "", e3, "_pos",
            self.get_keyframes(1, right_side - 10, -1), interp=True)
        e4.add_animation(
            "", e4, "_pos",
            self.get_keyframes(1, right_side - 20, -1), interp=True)

        self._state_add(e1)
        self._state_add(e2)
        self._state_add(e3)
        self._state_add(e4)


class InGameState(State):

    def __init__(self, owner):
        LOG.info("Instantiating InGame state")
        super(InGameState, self).__init__(owner)
        self._objects = []
        self._collision_manager = CollisionManager()
        self._screen = self._owner.screen

        LOG.debug("Registering renderable entities")

        self.level = TestLevel(self.add, speed=1)
        self._actor = self.level._player_ship

        self._events = InGameEventHandler(self)

        self.add(self._create_gui())
        self.level.start()

    # TODO: [object-system]
    #  * implement GameObject common class for using in states
    #  * generalize interaction with game objects and move `add` to base class
    # ATTENTION: renderables that added by another objects in runtime will not
    #  render at the screen, because they must register in state via this func
    #  as others. This is temporary decision as attempt to create playable game
    #  due to deadline.
    def add(self, obj):
        """Add GameObject to State's list of objects.

        Adding via this method means that objects will be
        updated and rendered in main IOLoop.

        :param object obj: GameObject
        """

        obj = obj if isinstance(obj, (list, tuple)) else [obj]
        self._objects.extend(obj)

        # TODO: Because we don't have common GameObject interface
        # This is temporary smellcode
        try:
            for item in obj:
                if item.compound:
                    self._objects.extend(item.get_renderable_objects())
        except AttributeError:
            pass

    def _create_gui(self):
        """Create user intarface."""
        whatever = lambda val: 0.0 <= val <= 100.0
        high = lambda val: 70.0 <= val <= 100.0
        normal = lambda val: 35.0 <= val < 70.0
        low = lambda val: 0.0 <= val < 35.0

        return [
            Bar(pos=Settings.layout.gui.bar.health, prefix="Hull: ",
                general_style=curses.A_BOLD, stylemap={
                    high: Style().gui["dp_ok"],
                    normal: Style().gui["dp_middle"],
                    low: Style().gui["dp_critical"]
                }, callback=self._actor.get_hull_percentage),
            Bar(pos=Settings.layout.gui.bar.shield, prefix="Shield: ",
                general_style=curses.A_BOLD, stylemap={
                    high: Style().gui["sh_ok"],
                    normal: Style().gui["sh_mid"],
                    low: Style().gui["dp_critical"]
                }, callback=self._actor.get_shield_percentage),
            Bar(pos=Settings.layout.gui.bar.weapon,
                stylemap={
                    whatever: Style().gui["dp_ok"]
                }, callback=self._actor.get_weapon_percentage),
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
        self._collision_manager.update()
        self.level.update()
        if not self.level.running:
            self.level.start()

        for obj in self._objects:
            obj.update()

    def render(self):
        self._screen.erase()
        self._screen.border(0)

        render_objects(self._objects, self._screen)
        self._screen.refresh()
