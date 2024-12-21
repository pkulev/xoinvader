"""Game pickup objects."""

import logging
import random
from typing import NoReturn

from xo1 import Renderable, Surface

from xoinvader import app, collision
from xoinvader.collision import Collider
from xoinvader.common import _ROOT, Settings, get_config


CONFIG = get_config().pickup

LOG = logging.getLogger(__name__)


class Pickup(Renderable):
    """Pickup base class."""

    def __init__(self, pos, image, dy=0, instant=True, use_amount=1, **kwargs) -> None:
        super().__init__(pos)

        self._image = Surface.from_file(_ROOT / image)
        self._dy = dy
        self._instant = instant
        self._use_amount = use_amount

        for name, value in kwargs.items():
            setattr(self, name, value)

        self._collider = Collider.simple(self)
        self._destroy = False

    @staticmethod
    def from_droptable(obj):
        droptable = CONFIG.get("droptable", {})
        table = droptable.get(obj.type)["one_of"]
        total_weight = sum(it["weight"] for it in table)
        value = random.randint(0, total_weight)
        for entry in table:
            if value < entry["weight"]:
                return eval(entry["item"])
            else:
                value -= entry["weight"]

    @classmethod
    def get_config(cls) -> dict:
        """Return object"s configuration merged with defaults."""

        override = CONFIG[cls.__name__]
        config = CONFIG.pop("defaults", {})
        config.update(override)
        return config

    @property
    def instant(self):
        return self._instant

    def apply(self, owner) -> NoReturn:
        """Apply pickup effect to owner."""

        raise NotImplementedError

    def update(self, dt) -> None:
        """Pickups are falling down til bottom border."""

        border = Settings.layout.field.camera
        self.pos.y += self._dy * dt / 1000
        if self.pos.y + self.image.height > border.y:
            self.pos.y = border.y - self.image.height

    def destroy(self) -> None:
        LOG.debug("Destroying collectible %s", self)
        if not self._destroy:
            self._destroy = True
            app.current().state.collision.remove(self._collider)
            app.current().state.remove(self)

    @collision.register("FullAmmoCratePickup", "PlayerShip")
    @collision.register("HullCratePickup", "PlayerShip")
    @collision.register("WeaponUpgradePickup", "PlayerShip")
    def collide(self, player, rect) -> None:
        self.apply(player)
        self.destroy()


class FullAmmoCratePickup(Pickup):
    """Fully replenish ammo for all mounted weapons.

    Should be rare to drop. Maybe chance have to increase if player low on ammo.
    """

    def __init__(self, pos) -> None:
        super().__init__(pos, **self.get_config())

    def apply(self, owner) -> None:
        owner.refill_all_weapons()


class HullCratePickup(Pickup):

    def __init__(self, pos) -> None:
        super().__init__(pos, **self.get_config())

    def apply(self, owner) -> None:
        owner.refill_hull(self.amount)


class WeaponUpgradePickup(Pickup):

    def __init__(self, pos) -> None:
        super().__init__(pos, **self.get_config())

    def apply(self, owner) -> None:
        owner.upgrade_weapon()
