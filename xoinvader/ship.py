"""Enemy and player ships."""

import logging

from xoinvader import app
from xoinvader import collision
from xoinvader.animation import AnimationManager
from xoinvader.render import Renderable
from xoinvader.weapon import Blaster, Laser, UM, EBlaster
from xoinvader.utils import Point, Surface, InfiniteList
from xoinvader.collision import Collider
from xoinvader.common import Settings, get_config


LOG = logging.getLogger(__name__)

# pylint: disable=missing-docstring
CONFIG = get_config().ship


# Think about composition
class Ship(Renderable):
    """Base class for all ships. Contains basic ship logic."""

    compound = True

    def __init__(self, pos):
        self._type = self.__class__.__name__
        self._image = None

        self._pos = pos

        self._dx = None
        self._fire = False
        self._weapon = None
        self._weapons = InfiniteList()
        self._wbay = None
        self._direction = 0

        self._max_hull = None
        self._max_shield = None
        self._hull = None
        self._shield = None

        # Set to True means that object in destroying phase
        # and will ignore remove_obsolete signal
        self._destroy = False

        self._collider = None

        # first initialization
        self._load_config(CONFIG[self._type])

    def _load_config(self, config):
        """Load config from mapping."""

        if not config:
            raise ValueError

        self._dx = int(config.dx)
        self._hull = int(config.hull)
        self._shield = int(config.shield)
        self._max_hull = int(config.max_hull)
        self._max_shield = int(config.max_shield)

    @property
    def pos(self):
        return self._pos

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value == 0:
            self._direction = 0
        else:
            self._direction = 1 if value > 0 else -1

    @property
    def max_hull(self):
        return self._max_hull

    @property
    def max_shield(self):
        return self._max_shield

    def get_hull_percentage(self):
        """Return hull percentage."""
        return self._hull * 100.0 / self._max_hull

    def get_shield_percentage(self):
        """Return shield percentage."""
        return self._shield * 100.0 / self._max_shield

    def get_weapon_percentage(self):
        """Return weapon load percentage."""
        return self._weapon.load_percentage()

    def get_render_data(self):
        """Callback for rendering."""
        return [self._pos], self._image.get_image()

    def get_renderable_objects(self):
        """CORP stub."""
        return self._weapons

    def move_left(self):
        """Change direction."""
        self._direction = -1

    def move_right(self):
        """Change direction."""
        self._direction = 1

    def toggle_fire(self):
        """Toggle current weapon fire mode."""
        self._fire = not self._fire

    def next_weapon(self):
        """Select next weapon."""
        self._weapon = self._weapons.next()

    def prev_weapon(self):
        """Select previous weapon."""
        self._weapon = self._weapons.prev()

    def add_weapon(self, weapon):
        """Add new weapon."""

        self._weapons.append(weapon)
        self._weapon = weapon

    def update_position(self, dt):
        """Update ship position.

        Allows to go behind field borders.
        """

        self._pos.x += self._direction * self._dx * dt
        self._direction = 0

    def update(self, dt):
        """Update ship object's state."""

        self.update_position(dt)

        for weapon in self._weapons:
            weapon.update(dt)

        if self._fire:
            try:
                # FIXME: [fix-in-place-coercing]
                #        Coercing Point in-place smells badly
                #        (needed now because animation can set float pos to
                #        enemy ships), we need to add type ensurance mechanism
                #        to cast automatically maybe.
                self._weapon.make_shot(self._pos[int] + self._wbay)
            except ValueError:
                self.next_weapon()

        self.refresh_shield()

    def destroy(self):
        """Self-destroying routine."""

        LOG.debug("Destroying ship %s", self)

        if not self._destroy:
            self._destroy = True
            app.current().state.collision.remove(self._collider)
            app.current().state.remove(self)

    def remove_obsolete(self, pos):
        border = Settings.layout.field.border
        pos = self._pos[int]
        if (
            pos.x > self._image.width + border.x
            or pos.x + self._image.width < 0
            or int(pos.y) > self._image.height + border.y
            or int(pos.y) + self._image.height < 0
        ) and not self._destroy:
            self.destroy()

    def take_damage(self, damage):
        """Calculate and apply damage to shield and hull."""

        if self._shield < damage:
            rest_damage = damage - self._shield
            self._shield = 0
            self._hull -= rest_damage
        else:
            self._shield -= damage
        if self._hull < 0:
            self._hull = 0

    def refresh_shield(self, amount=1):
        """Refresh shield."""

        if self._shield == self._max_shield:
            return

        if self._shield + amount > self._max_shield:
            self._shield = self._max_shield
        else:
            self._shield += amount


class GenericXEnemy(Ship):
    """Generic X enemy class."""

    def __init__(self, pos):
        super(GenericXEnemy, self).__init__(pos)
        # fmt: off
        self._image = Surface([
            "x^x",
            " X ",
            " * ",
        ])
        # fmt: on

        self._collider = Collider.simple(self)

        self.add_weapon(EBlaster())
        self._fire = True
        self._wbay = Point(x=self._image.width // 2, y=1)

        self._animgr = AnimationManager()

    # TODO: rethink this method
    #       Problem of emerging such methods is more complex problem
    #       of creating and configuring GameObjects.
    def add_animation(self, *args, **kwargs):
        self._animgr.add(*args, **kwargs)

    def update(self, dt):
        if self._hull <= 0:
            # TODO: [scoring]
            #       * Parametrize scores, move them to ships.conf
            #       * implement better scoring mechanism
            app.current().state.add_player_score(10)
            self.destroy()
            return

        self._animgr.update(dt)

        super(GenericXEnemy, self).update(dt)

    @collision.register("GenericXEnemy", "BasicPlasmaCannon")
    @collision.register("GenericXEnemy", "BasicLaserCharge")
    @collision.register("GenericXEnemy", "BasicUnguidedMissile")
    def collide(self, other, rect):
        self.take_damage(other.damage)
        other.destroy()


class PlayerShip(Ship):
    """PlayerShip class. Contains additional methods for HUD.

    :param :class:`xoinvader.utils.Point` pos: left top corner
    """

    def __init__(self, pos):
        super(PlayerShip, self).__init__(pos)

        # fmt: off
        self._image = Surface([
            "  O  ",
            "<=H=>",
            " * * ",
        ])
        # fmt: on

        self._pos = Point(
            x=pos.x - self._image.width // 2, y=pos.y - self._image.height
        )

        self._collider = Collider.simple(self)

        self._fire = False
        self._weapons = InfiniteList([Blaster(), Laser(), UM()])
        self._weapon = self._weapons.current()
        self._wbay = Point(x=self._image.width // 2, y=-1)

    def update_position(self, dt):
        """Update player ship position.

        Prohibits moving out behind the border.
        """

        border = Settings.layout.field.camera
        right = self._pos.x + self._image.width

        if right >= border.x - 1 and self._direction > 0:
            self._pos.x = border.x - self._image.width

        elif self._pos.x <= 1 and self._direction < 0:
            self._pos.x = 1

        else:
            # NOTE: Converting float to int reduces ship teleportation because
            #       we have no pixels.
            self._pos.x += int(self._direction * self._dx * dt / 1000)

        self._direction = 0

    def update(self, dt):
        if self._hull <= 0:
            app.current().trigger_state(
                "GameOverState", score=app.current().state.score
            )

        super(PlayerShip, self).update(dt)

    def get_weapon_info(self):
        """Return information about current weapon."""

        return "Weapon: {w} | [{c}/{m}]".format(
            w=self._weapon.type, c=self._weapon.ammo, m=self._weapon.max_ammo
        )

    @collision.register("PlayerShip", "EBasicPlasmaCannon")
    def collide(self, other, rect):
        self.take_damage(other.damage)
        other.destroy()
