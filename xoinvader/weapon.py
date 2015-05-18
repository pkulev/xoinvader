"""Game weapon classes."""

from abc import ABCMeta, abstractmethod


from xoinvader.render import Renderable
from xoinvader.utils import Point, Surface, Timer
from xoinvader.common import Settings, get_json_config
from xoinvader.sound import Mixer


CONFIG = get_json_config(Settings.path.config.weapons)
INFINITE = "infinite"


class IWeapon(object, metaclass=ABCMeta):
    """Interface for weapon game entities."""
    @abstractmethod
    def make_shot(self, pos):
        """Make shot, if can't - raise ValueError."""
        pass

    @abstractmethod
    def update(self):
        """Update coords list."""
        pass


def _load_from_config(weapon, config):
    """Loads main parameters and returns kwargs for passing to Weapon."""
    section = weapon.__name__
    params = ("ammo", "max_ammo", "cooldown", "damage", "radius", "dy")
    return {var : config[section].get(var) for var in params}


class Weapon(IWeapon, Renderable):
    """Main weapon class that implements main methods and behaviour."""
    def __init__(self, ammo, max_ammo, cooldown, damage, radius, dy):
        self._type     = self.__class__.__name__
        self._image    = None
        self._ammo     = ammo
        self._max_ammo = max_ammo
        self._cooldown = cooldown
        self._damage   = damage
        self._radius   = radius
        self._dy       = dy
        self._current_cooldown = self._cooldown

        self.ready = True
        self._timer = Timer(self._cooldown, self._reload)
        self._coords = []
        self._loud = True

        Mixer.register(self._type, Settings.path.sound.weapon[self._type])

    def _reload(self):
        """Calls by timer when weapon is ready to fire."""
        # TODO: Play sound
        self.ready = True
        self._timer.stop()
        self._timer.reset()

    def make_shot(self, pos):
        """Check load and ammo, perform shot if ready."""
        if not self.ready:
            return

        if self._ammo == INFINITE:
            self._coords.append(pos)
        elif self._ammo > 0:
            self._coords.append(pos)
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
            Mixer.play(self._type)

    def get_render_data(self):
        """Callback for Renderer."""
        return (self._coords, self._image.get_image())

    def remove_obsolete(self, pos):
        """Callback for Renderer."""
        self._coords.remove(pos)

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

    def loadPercentage(self):
        """Return weapon load percentage."""
        if self._ammo and self.ready:
            return 100.0
        return self._timer.getElapsed() * 100.0 / self._cooldown

    def update(self):
        """Update coords."""
        if self.ready and not self._coords:
            return

        new_coords = []
        for i in self._coords:
            new_coords.append(Point(x=i.x, y=i.y - self._dy))
        self._coords = new_coords[:]
        self._timer.update()


import curses
class Blaster(Weapon):
    """Basic player's weapon. Low damage, fast cooldown."""
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, CONFIG))
        self._image = Surface([["^"]], style=[[curses.A_BOLD]])


class EBlaster(Weapon):
    """Basic enemy blaster. Almost identical to Blaster."""
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, CONFIG))
        self._image = Surface([[":"]])


class Laser(Weapon):
    """Basic player's laser. Medium damage, medium cooldown."""
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, CONFIG))
        self._image = Surface([["|"]], style=[[curses.A_BOLD]])


class UM(Weapon):
    """Player's unguided missile. High damage, slow cooldown."""
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, CONFIG))
        self._image = Surface([["^"],
                               ["|"],
                               ["*"]], style=[[curses.A_BOLD] for _ in range(3)])
