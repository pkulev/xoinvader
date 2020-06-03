"""Enemy and player ships."""

import logging
import random

from xo1 import Surface, Renderable

from xoinvader import app
from xoinvader import collision
from xoinvader.animation import AnimationManager
from xoinvader.pickup import Pickup
from xoinvader.weapon import Blaster, Laser, UM, EBlaster, Weapon
from xoinvader.utils import clamp, Point, InfiniteList
from xoinvader.collision import Collider
from xoinvader.common import Settings, get_config, _ROOT


LOG = logging.getLogger(__name__)

# pylint: disable=missing-docstring
CONFIG = get_config().ship


# Think about composition
class Ship(Renderable):
    """Base class for all ships. Contains basic ship logic."""

    compound = True

    def __init__(self, pos: Point):

        super().__init__(pos)

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

        self._destroy = False
        self._collider = None

        # first initialization
        self._apply_config(CONFIG[self.type])

    def _apply_config(self, config):
        """Apply values from object's configuration."""

        if not config:
            raise ValueError

        self._dx = int(config.dx)
        self._hull = int(config.hull)
        self._shield = int(config.shield)
        self._max_hull = int(config.max_hull)
        self._max_shield = int(config.max_shield)

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

    def add_weapon(self, weapon: Weapon, autoselect: bool = True):
        """Add new weapon and optionally select it."""

        self._weapons.append(weapon)
        if autoselect:
            self._weapon = weapon

    def update_position(self, dt: int):
        """Update ship position.

        Allows to go behind field borders.
        """

        self._pos.x += self._direction * self._dx * dt
        self._direction = 0

    def update(self, dt: int):
        """Update ship object's state."""

        self.update_position(dt)

        if self.out_of_border():
            self.destroy()

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

        if not self._destroy:
            LOG.debug("Destroying ship %s", self)

            self._destroy = True
            if self._destroyed_by_player:
                self._maybe_drop_something()
            app.current().state.collision.remove(self._collider)
            app.current().state.remove(self)

    def out_of_border(self) -> bool:
        border = Settings.layout.field.border
        pos = self._pos[int]
        return (
            pos.x > self._image.width + border.x
            or pos.x + self._image.width < 0
            or int(pos.y) > self._image.height + border.y
            or int(pos.y) + self._image.height < 0
        )

    def take_damage(self, damage: int):
        """Calculate and apply damage to shield and hull."""

        # shield absorbs all damage
        if self._shield >= damage:
            self._shield -= damage
            return

        # shield fully discharged
        damage = clamp(damage - self._shield, 0, damage)
        self._shield = 0

        # hull takes all rest damage
        self._hull = clamp(self._hull - damage, 0, self._hull)

    def refresh_shield(self, amount: int = 1):
        """Refresh shield."""

        if self._shield == self._max_shield:
            return

        self._shield = clamp(self._shield + amount, 0, self._max_shield)

    def collect(self, collectible):
        """Collect bonus or power-up and apply it now or later.

        :param xoinvader.Collectible collectible:
        """

        if collectible.instantaneous:
            collectible.apply(self)
        else:
            raise Exception("_collectibles not implemented")

    def refill_hull(self, amount: int = 0):
        """Refill hull."""

        self._hull = clamp(self._hull + amount, 0, self._max_hull)

    def refill_all_weapons(self, percent: int):
        """Refill all mounted weapons with provided persentage."""

        for weapon in self.weapons:
            self.refill_weapon(weapon, percent * weapon.max_ammo / 100)

    def refill_weapon(self, weapon: Weapon, amount: int):
        """Refill provided or current weapon."""

        if not weapon:
            weapon = self._weapon

        weapon.refill(amount)


class GenericXEnemy(Ship):
    """Generic X enemy class."""

    def __init__(self, pos):
        super(GenericXEnemy, self).__init__(pos)
        self._image = Surface.from_file(_ROOT / (CONFIG[self.type]["image"]))

        self._collider = Collider.simple(self)

        self._fire = True
        self._wbay = Point(x=self._image.width // 2, y=1)
        self.add_weapon(EBlaster(self._wbay))

        self._destroyed_by_player = False

        self._animgr = AnimationManager()

    # TODO: rethink this method
    #       Problem of emerging such methods is more complex problem
    #       of creating and configuring GameObjects.
    def add_animation(self, *args, **kwargs):
        self._animgr.add(*args, **kwargs)

    def _maybe_drop_something(self):
        drop_chance = 0.4
        if 1 - random.random() > drop_chance:
            return

        drop = Pickup.from_droptable(self)
        if drop is not None:
            app.current().state.add(drop(self.pos))

    def take_damage(self, amount: int):
        """Naive wrapper to distinguish destroy by player and out of boundary."""

        super().take_damage(amount)
        if self._hull <= 0:
            self._destroyed_by_player = True

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
    """PlayerShip class."""

    def __init__(self, pos):
        super(PlayerShip, self).__init__(pos)
        self.image = Surface.from_file(_ROOT / (CONFIG[self.type]["image"]))

        # FIXME: Center the ship where it's created
        self._pos = Point(
            x=pos.x - self._image.width // 2, y=pos.y - self._image.height
        )

        self._collider = Collider.simple(self)

        self._fire = False
        self._wbay = Point(x=self._image.width // 2, y=-1)
        self._weapons = InfiniteList([
            Blaster(self._wbay),
            Laser(self._wbay),
            UM(self._wbay),
        ])
        self._weapon = self._weapons.current()

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
