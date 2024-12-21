"""Game weapon charge classes.

Attention: Next statement related only to GameObject entities.
           There're situations where two GameObject modules need to import
           each other. In such cases do it via importing `xoinvader.registry`
           in functions (not at import time).
"""


import curses
import logging

from xo1 import Renderable, Surface

from xoinvader import app
from xoinvader.collision import Collider
from xoinvader.common import Settings, get_config
from xoinvader.utils import Point


CONFIG = get_config().charge
LOG = logging.getLogger(__name__)


# TODO: [components]: move some variables to default GameObject components
# pylint: disable=too-many-arguments,too-many-instance-attributes
class WeaponCharge(Renderable):
    """Weapon charge representation.

    Separate renderable object that updates and renders as others
    in main loop. Must register/deregister itself via state's
    add/remove methods.
    """

    def __init__(self, pos: Point, image, damage=0, radius=0, dx=0, dy=0) -> None:

        super().__init__(pos)

        self._image = image

        # TODO: move out from constructor
        app.current().state.add(self)

        self._damage = damage
        self._radius = radius
        # TODO: [object-movement]
        # Generalize update to support dx
        self._dx = dx
        self._dy = dy

        self._destroy = False

        # Common collider for any shape charge
        self._collider = Collider.simple(self)

    @property
    def pos(self):
        return self._pos

    @property
    def damage(self):
        return self._damage

    def out_of_border(self):
        border = Settings.layout.field.border
        pos = self._pos[int]

        return (
            pos.x > self._image.width + border.x
            or pos.x + self._image.width < 0
            or int(pos.y) > self._image.height + border.y
            or int(pos.y) + self._image.height < 0
        )

    def update(self, dt) -> None:
        """Update coords."""

        self._pos += Point(self._dx, self._dy) * dt / 1000

        if self.out_of_border():
            self.destroy()

    def destroy(self) -> None:
        """Self-destroying routine."""

        if not self._destroy:
            LOG.debug("Destroying charge %s", self)
            self._destroy = True
            app.current().state.collision.remove(self._collider)
            app.current().state.remove(self)


# TODO: Implement hitscan behaviour
# pylint: disable=useless-super-delegation
class Hitscan(WeaponCharge):
    """Hitscan weapon charge hits target immediately.

    Can pierce enemies?
    """

    def __init__(self, pos, image, **kwargs) -> None:
        super().__init__(pos, image, **kwargs)


class Projectile(WeaponCharge):
    """Projectile weapon has generic physics of movement."""

    def __init__(self, pos, image, **kwargs) -> None:
        super().__init__(pos, image, **kwargs)


# TODO: write template documentation for charges and weapons
class BasicPlasmaCannon(Projectile):
    """Small damage, no radius."""

    def __init__(self, pos) -> None:
        super().__init__(
            pos,
            Surface(["^"], color=[[curses.A_BOLD]]),
            **CONFIG[self.__class__.__name__]
        )


class EBasicPlasmaCannon(Projectile):
    """Enemy plasma cannon."""

    def __init__(self, pos) -> None:
        super().__init__(
            pos,
            Surface([":"], color=[[curses.A_BOLD]]),
            **CONFIG[self.__class__.__name__]
        )


class BasicLaserCharge(Projectile):
    """Laser. Quite fast but cannot pierce enemies."""

    def __init__(self, pos) -> None:
        super().__init__(
            pos,
            Surface(["|"], color=[[curses.A_BOLD]]),
            **CONFIG[self.__class__.__name__]
        )


class BasicUnguidedMissile(Projectile):
    """Unguided missile with medium damage and small radius."""

    def __init__(self, pos) -> None:
        # fmt: off
        super().__init__(
            pos,
            Surface([
                "^",
                "|",
                "*",
            ], color=[[curses.A_BOLD] for _ in range(3)]),
            **CONFIG[self.__class__.__name__]
        )
        # fmt: on
