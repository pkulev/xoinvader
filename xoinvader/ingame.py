"""InGameState-specific input/event handlers and commands."""

import curses
import logging
import weakref

from eaf.state import State

from xoinvader.background import Background
from xoinvader.collision import CollisionManager
from xoinvader.common import Settings
from xoinvader.style import Style
from xoinvader.gui import TextCallbackWidget, TextWidget, WeaponWidget, Bar
from xoinvader.handlers import EventHandler
from xoinvader.keys import KEY
from xoinvader.level import Level
from xoinvader.ship import GenericXEnemy, PlayerShip
from xoinvader.utils import Point, dotdict


LOG = logging.getLogger(__name__)


# pylint: disable=invalid-name
class TestLevel(Level):
    def __init__(self, state_object_adder, speed):
        super(TestLevel, self).__init__(speed)
        self._state_add = state_object_adder

        self._player_ship = PlayerShip(Settings.layout.field.player)
        self._state_add(self._player_ship)
        self._enemies = weakref.WeakSet()

        self.add_event(1, self.spawn4)
        self.add_event(100, lambda: None)
        self.add_event(200, self.del4)

        self.bg = Background(Settings.path.level1bg, speed=10, loop=True)
        self.bg.start(filled=True)
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

        e1 = GenericXEnemy(Point(10, 1))
        e2 = GenericXEnemy(Point(25, 1))
        e3 = GenericXEnemy(Point(right_side - 10, 1))
        e4 = GenericXEnemy(Point(right_side - 25, 1))

        e1.add_animation(
            "", e1, "_pos", self.get_keyframes(1, 10, 1), interp=True
        )
        e2.add_animation(
            "", e2, "_pos", self.get_keyframes(1, 20, 1), interp=True
        )

        e3.add_animation(
            "",
            e3,
            "_pos",
            self.get_keyframes(1, right_side - 10, -1),
            interp=True,
        )
        e4.add_animation(
            "",
            e4,
            "_pos",
            self.get_keyframes(1, right_side - 20, -1),
            interp=True,
        )

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

    def postinit(self):
        """Deferred initialization.

        Prepare GameObjects that require created and registered State object.
        """

        self.level = TestLevel(self.add, speed=1)
        self.actor = self.level._player_ship

        # TODO: [scoring]
        self.score = 0

        self._events = EventHandler(
            self,
            {
                KEY.A: self.actor.move_left,
                KEY.D: self.actor.move_right,
                KEY.E: self.actor.next_weapon,
                KEY.Q: self.actor.prev_weapon,
                KEY.R: lambda: self.actor.take_damage(5),
                KEY.SPACE: self.actor.toggle_fire,
                KEY.ESCAPE: self.pause_command,
            },
        )

        self.add(self._create_gui())
        self.level.start()

    def pause_command(self):
        self.app.state = "PauseMenuState"

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
                pos=Settings.layout.gui.bar.health,
                prefix="Hull: ",
                general_style=curses.A_BOLD,
                stylemap={
                    comp.high: Style().gui["dp_ok"],
                    comp.normal: Style().gui["dp_middle"],
                    comp.low: Style().gui["dp_critical"],
                },
                callback=self.actor.get_hull_percentage,
            ),
            Bar(
                pos=Settings.layout.gui.bar.shield,
                prefix="Shield: ",
                general_style=curses.A_BOLD,
                stylemap={
                    comp.high: Style().gui["sh_ok"],
                    comp.normal: Style().gui["sh_mid"],
                    comp.low: Style().gui["dp_critical"],
                },
                callback=self.actor.get_shield_percentage,
            ),
            Bar(
                pos=Settings.layout.gui.bar.weapon,
                stylemap={comp.whatever: Style().gui["dp_ok"]},
                callback=self.actor.get_weapon_percentage,
            ),
            WeaponWidget(
                Settings.layout.gui.info.weapon, self.actor.get_weapon_info
            ),
        ] + [
            TextCallbackWidget(Point(2, 0), self.get_player_score_string),
            TextWidget(
                Point(Settings.layout.field.edge.x // 2 - 4, 0),
                "XOInvader",
                curses.A_BOLD,
            ),
        ]

    def events(self):
        self._events.handle()

    def update(self):
        self.collision.update()
        self.level.update()
        if not self.level.running:
            self.level.start()

        super().update()
