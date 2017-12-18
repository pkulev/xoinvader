"""InGameState-specific input/event handlers and commands."""

import curses
import logging
import weakref

from xoinvader import application
from xoinvader.background import Background
from xoinvader.collision import CollisionManager
from xoinvader.common import Settings
from xoinvader.curses_utils import Style
from xoinvader.gui import TextCallbackWidget, TextWidget, WeaponWidget, Bar
from xoinvader.handlers import Handler
from xoinvader.keys import K_A, K_D, K_E, K_F, K_R, K_SPACE, K_ESCAPE, K_Q
from xoinvader.level import Level
from xoinvader.render import render_objects
from xoinvader.ship import GenericXEnemy, PlayerShip
from xoinvader.state import State
from xoinvader.utils import Point, dotdict


LOG = logging.getLogger(__name__)


# pylint: disable=missing-docstring
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


# pylint: disable=protected-access
def switch_actor_command(actor):
    actor._actor, actor._owner.enemy = actor._owner.enemy, actor._actor


def to_mainmenu_command(actor):
    actor.owner.state = "MainMenuState"


# pylint: disable=too-few-public-methods
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


# pylint: disable=invalid-name
class TestLevel(Level):
    def __init__(self, state_object_adder, speed):
        super(TestLevel, self).__init__(speed)
        self._state_add = state_object_adder

        self._player_ship = PlayerShip(
            Settings.layout.field.player, Settings.layout.field.edge)
        self._state_add(self._player_ship)
        self._enemies = weakref.WeakSet()

        self.add_event(1, self.spawn4)
        self.add_event(100, lambda: None)
        self.add_event(200, self.del4)

        self.bg = Background(Settings.path.level1bg, speed=10, loop=True)
        self.bg.start(True)
        self._state_add(self.bg)

    @staticmethod
    def get_keyframes(y_offset, x_start, direction):
        """Generate keyframe list.

        :param int y_offset: y of top left corner of image
        :param int x_start: x level of left corner of image
        :param int direction: direction of moving: -1 is left, 1 is right
        """

        def new_x(d):
            return x_start - d * direction

        return [
            (0, Point(x_start, y_offset)),
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

        self._enemies = weakref.WeakSet([e1, e2, e3, e4])
        self._state_add(list(self._enemies))

    def del4(self):
        for enemy in self._enemies:
            enemy.destroy()


class InGameState(State):

    # TODO FIXME: collision manager looks like collision system
    #             belonging to State. Idea is to create some sort of
    #             mechanism for registering/deregistering/accesing
    #             theese systems via GameObject's current State.
    # ATTENTION: Here I met a problem of initialization of this state.
    #            1) here in init we created collision manager (now moved here)
    #            2) initialization of TestLevel created first game object
    #            (PlayerShip) that have collider
    #            3) Collider needs to be registered in CollisionManager that
    #            already was created, BUT! Collider.__init__ can't have
    #            access to current state because several frames above current
    #            control flow resides in State.__init__ and State does not
    #            fully instantiated yet and could not be accessed via
    #            application.state.
    #            One approach that I see here is to create optional postinit
    #            method and create objects that want access to state there.
    # NOTE: I think that here we must extrude systems with such behaviour and
    #       create them before state initialization, maybe here in classfields.
    collision = CollisionManager()

    def __init__(self, owner):
        LOG.info("Instantiating InGame state")
        super(InGameState, self).__init__(owner)
        self._objects = []
        self._screen = self._owner.screen

    def postinit(self):
        """Deferred initialization.

        Prepare GameObjects that require created and registered State object.
        """

        LOG.debug("Registering renderable entities")

        self.level = TestLevel(self.add, speed=1)
        self._actor = self.level._player_ship

        # TODO: [scoring]
        self.score = 0

        self._events = InGameEventHandler(self)

        self.add(self._create_gui())
        self.level.start()

    def add_player_score(self, amount):
        """Add player score.

        :param int amount: scores to add
        """

        self.score += amount

    def get_player_score_string(self):
        """Callback for TextCallbackWidget.

        :return str: score string
        """

        return "Score: {0}".format(self.score)

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
        LOG.debug("%s", obj)

        # TODO: Because we don't have common GameObject interface
        # This is temporary smellcode
        for item in obj:
            if item.compound:
                subitems = item.get_renderable_objects()
                LOG.debug("Subitems: %s", subitems)
                self._objects.extend(subitems)

    def remove(self, obj):
        """Remove GameObject from State's list of objects.

        Removed objects should be collected by GC.

        :param object obj: GameObject
        """

        LOG.debug("%s", obj)

        try:
            if obj.compound:
                for subobj in obj.get_renderable_objects():
                    self._objects.remove(subobj)
                    del subobj
            self._objects.remove(obj)
        except ValueError:
            LOG.exception("Object %s is not in State's object list.", obj)
        finally:
            del obj

        # TODO: [collider-destruction]
        #       Remove this after collider instant destruction.
        #       Now colliders in weakref set garbage-collected with noticeable
        #       delay. In future we need to drop weakrefs and manually manage
        #       objects.
        LOG.debug("Colliders: %s", len(self.collision._colliders))
        LOG.debug("Collisions: %s", len(self.collision._collisions))
        LOG.debug("Objects in state: %s", len(self._objects))

    def _create_gui(self):
        """Create user interface."""

        comp = dotdict(
            whatever=lambda val: 0.0 <= val <= 100.0,
            high=lambda val: 70.0 <= val <= 100.0,
            normal=lambda val: 35.0 <= val < 70.0,
            low=lambda val: 0.0 <= val < 35.0,
        )

        return [
            Bar(
                pos=Settings.layout.gui.bar.health, prefix="Hull: ",
                general_style=curses.A_BOLD, stylemap={
                    comp.high: Style().gui["dp_ok"],
                    comp.normal: Style().gui["dp_middle"],
                    comp.low: Style().gui["dp_critical"]
                }, callback=self._actor.get_hull_percentage),
            Bar(
                pos=Settings.layout.gui.bar.shield, prefix="Shield: ",
                general_style=curses.A_BOLD, stylemap={
                    comp.high: Style().gui["sh_ok"],
                    comp.normal: Style().gui["sh_mid"],
                    comp.low: Style().gui["dp_critical"]
                }, callback=self._actor.get_shield_percentage),
            Bar(
                pos=Settings.layout.gui.bar.weapon,
                stylemap={
                    comp.whatever: Style().gui["dp_ok"]
                }, callback=self._actor.get_weapon_percentage),
            WeaponWidget(
                Settings.layout.gui.info.weapon,
                self.actor.get_weapon_info)
        ] + [
            TextCallbackWidget(Point(2, 0), self.get_player_score_string),
            TextWidget(
                Point(Settings.layout.field.edge.x // 2 - 4, 0),
                "XOInvader", curses.A_BOLD)
        ]

    def events(self):
        self._events.handle()

    def update(self):
        self.collision.update()
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
