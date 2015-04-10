from abc import ABCMeta, abstractmethod

from xoinvader.utils import Point, Surface
from xoinvader.common import Settings, get_json_config


CONFIG = get_json_config(Settings.path.config.weapons)


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
    return {var : config[section].get(var) for var in params}


class Weapon(IWeapon):
    def __init__(self, ammo, max_ammo, cooldown, damage, radius, dy):
        self._type     = "__basic__"
        self._image    = None
        self._ammo     = ammo
        self._max_ammo = max_ammo
        self._cooldown = cooldown
        self._damage   = damage
        self._radius   = radius
        self._dy       = dy
        self._current_cooldown = self._cooldown

        self.ready = True
        self._coords = []

    def _prepare_weapon(self):
        #play sound
        self.ready = True
        self._current_cooldown = self._cooldown

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
        self._current_cooldown = 0

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
        return self._current_cooldown

    @property
    def type(self):
        return self.__class__.__name__

    def update(self):
        new_coords = []
        for i in self._coords:
            new_coords.append(Point(x=i.x, y=i.y - self._dy))
        self._coords = new_coords[:]
        self._current_cooldown += 1
        if self._current_cooldown >= self._cooldown:
            self._prepare_weapon()


import curses
class Blaster(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, CONFIG))
        self._image = Surface([["^"]], style=[[curses.A_BOLD]])


class EBlaster(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, CONFIG))
        self._image = Surface([[":"]])


class Laser(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, CONFIG))
        self._image = Surface([["|"]], style=[[curses.A_BOLD]])


class UM(Weapon):
    def __init__(self):
        super().__init__(**_load_from_config(self.__class__, CONFIG))
        self._image = Surface([["^"],
                               ["|"],
                               ["*"]], style = [[curses.A_BOLD] for _ in range(3)])
