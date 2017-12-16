"""Game weapon classes."""


from xoinvader.charge import (
    BasicPlasmaCannon, EBasicPlasmaCannon,
    BasicLaserCharge, BasicUnguidedMissile
)
from xoinvader.common import Settings, get_json_config
from xoinvader.render import Renderable
from xoinvader.sound import Mixer
from xoinvader.utils import Point, Surface, Timer


CONFIG = get_json_config(Settings.path.config.weapons)
INFINITE = "infinite"


# TODO: think about composition
# pylint: disable=too-many-instance-attributes,too-many-arguments
class Weapon(Renderable):
    """Main weapon class that implements main methods and behaviour.

    Callbacks for rendering: get_render_data(), remove_obsolete(pos).
    """

    allowed_charges = []
    default_charge = None

    def __init__(self, ammo, max_ammo, cooldown):
        self._type = self.__class__.__name__
        self._image = Surface([" "])  # stub for now, to render nothing
        self._current_charge = self.default_charge
        self._ammo = ammo
        self._max_ammo = max_ammo
        self._cooldown = cooldown
        self._current_cooldown = self._cooldown

        self.ready = True
        self._timer = Timer(self._cooldown, self._reload)
        self._pos = Point()  # stub for now, to render nothing as weapon
        self._loud = True

        Mixer().register(self._type, Settings.path.sound.weapon[self._type])

    def _reload(self):
        """Calls by timer when weapon is ready to fire."""

        # TODO: Play sound
        self.ready = True
        self._timer.stop()
        self._timer.reset()

    def make_shot(self, pos):
        """Check load and ammo, perform shot if ready.

        :param xoinvader.utils.Point pos: position of fire
        :raise ValueError: when no ammo
        """

        if not self.ready:
            return

        if self._ammo == INFINITE:
            self._current_charge(pos)  # pylint: disable=not-callable
        elif self._ammo > 0:
            self._current_charge(pos)  # pylint: disable=not-callable
            self._ammo -= 1

        if self._ammo == 0:
            # No need to measure time.
            # TODO: don't raise exception:
            #       if no ammo - notify player once and
            #       repeat on fire key pressed again.
            self._timer.stop()
            raise ValueError("No ammo!")

        self.ready = False
        self._timer.start()
        if self._loud:
            Mixer().play(self._type)

    def get_render_data(self):
        return ([self._pos], self._image.get_image())

    @property
    def ammo(self):
        """Return actual ammo."""
        return 999 if self._ammo == INFINITE else self._ammo

    @property
    def max_ammo(self):
        """Return maximal ammo."""
        return 999 if self._max_ammo == INFINITE else self._max_ammo

    @property
    def type(self):
        """Return weapon type."""
        return self._type

    def load_percentage(self):
        """Return weapon load percentage."""

        if self._ammo and self.ready:
            return 100.0
        return self._timer.get_elapsed() * 100.0 / self._cooldown

    def update(self):
        """Update weapon timer."""

        if self.ready:
            return

        self._timer.update()


class Blaster(Weapon):
    """Basic player's weapon. Low damage, fast cooldown."""

    allowed_charges = [BasicPlasmaCannon]
    default_charge = BasicPlasmaCannon

    def __init__(self):
        super(Blaster, self).__init__(**CONFIG[self.__class__.__name__])


class EBlaster(Weapon):
    """Basic enemy blaster. Almost identical to Blaster."""

    allowed_charges = [EBasicPlasmaCannon]
    default_charge = EBasicPlasmaCannon

    def __init__(self):
        super(EBlaster, self).__init__(**CONFIG[self.__class__.__name__])


class Laser(Weapon):
    """Basic player's laser. Medium damage, medium cooldown."""

    allowed_charges = [BasicLaserCharge]
    default_charge = BasicLaserCharge

    def __init__(self):
        super(Laser, self).__init__(**CONFIG[self.__class__.__name__])


class UM(Weapon):
    """Player's unguided missile. High damage, slow cooldown."""

    allowed_charges = [BasicUnguidedMissile]
    default_charge = BasicUnguidedMissile

    def __init__(self):
        super(UM, self).__init__(**CONFIG[self.__class__.__name__])
