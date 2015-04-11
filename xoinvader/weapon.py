from abc import ABCMeta, abstractmethod
from configparser import SafeConfigParser, ExtendedInterpolation

from xoinvader.utils import Point, Surface, Timer
from xoinvader.common import Settings


config_file = Settings.path.config.weapons
config = SafeConfigParser(allow_no_value=True,
                          interpolation=ExtendedInterpolation())
config.read(config_file)
LOG = open("weapon.log", "w")

class IWeapon(object, metaclass=ABCMeta):
    @abstractmethod
    def make_shot(self):
        """Make shot, if can't - raise Value Error"""
        pass

    @abstractmethod
    def update(self):
        """update coords list"""
        pass


def _load_from_config(weapon, config):
    section = weapon.__name__
    params = ("ammo", "max_ammo", "cooldown", "damage", "radius", "dy")
    return {var : config.get(section, var) for var in params}


class Weapon(IWeapon):
    def __init__(self, ammo, max_ammo, cooldown, damage, radius, dy):
        self._type     = "__basic__"
        self._image    = None
        self._ammo     = int(ammo) if ammo.isdigit() else ammo
        self._max_ammo = int(max_ammo) if max_ammo.isdigit() else max_ammo
        self._cooldown = float(cooldown)
        self._damage   = int(damage)
        self._radius   = int(radius)
        self._dy       = int(dy)

        #Experimental
        self.ready = True
        self._timer = Timer(self._cooldown, self._reload)
        self._coords = []

    def _reload(self):
        """Calls by timer when weapon is ready to fire."""
        # TODO: Play sound
        self._timer.reset()
        self.ready = True

    def make_shot(self, pos):
        if not self.ready:
            return

        if self._ammo == "infinite":
            self._coords.append(pos)
        elif self._ammo > 0:
            self._coords.append(pos)
            self._ammo -= 1
        if self._ammo == 0: raise ValueError("No ammo!")

        self.ready = False
        self._timer.start()

    def get_render_data(self):
        return (self._coords, self._image.get_image())

    def remove_obsolete(self, pos):
        self._coords.remove(pos)

    @property
    def ammo(self):
        return 999 if self._ammo == "infinite" else self._ammo

    @property
    def max_ammo(self):
        return 999 if self._max_ammo == "infinite" else self._max_ammo

    @property
    def cooldown(self):
        return self._cooldown

    @property
    def current_cooldown(self):
        return self.cooldown if self.ready else round(self._timer.getCurrentTime())

    @property
    def type(self):
        return self.__class__.__name__

    def update(self):
        if self.ready and not self._coords:
            return
        
        new_coords = []
        for i in self._coords:
            new_coords.append(Point(x=i.x, y=i.y - self._dy))
        self._coords = new_coords[:]
        self._timer.update()
        LOG.write(str(self.__class__.__name__) + " : " + "  --  ".join([str(i) for i in [self.current_cooldown, self._cooldown]]) + "\n")


import curses
class Blaster(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, config))
        self._image = Surface([["^"]], style=[[curses.A_BOLD]])


class EBlaster(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, config))
        self._image = Surface([[":"]])


class Laser(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, config))
        self._image = Surface([["|"]], style=[[curses.A_BOLD]])


class UM(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, config))
        self._image = Surface([["^"],
                               ["|"],
                               ["*"]], style = [[curses.A_BOLD] for _ in range(3)])
