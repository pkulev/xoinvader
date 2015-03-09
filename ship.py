import configparser

from render import Renderable
from weapon import Blaster, Laser, UM, EBlaster
from utils import Point, Surface, InfList

config_file = "ships.cfg"
CONFIG = configparser.SafeConfigParser(allow_no_value=True,
        interpolation=configparser.ExtendedInterpolation())
CONFIG.read(config_file)


class Ship(Renderable):
    def __init__(self, pos, border, settings):
        self._image = None

        self._pos = pos
        self._border = border
        self._settings = settings

        self._dx = None
        self._fire = False
        self._weapon = None

        self._max_hull = None
        self._max_shield = None
        self._hull = None
        self._shield = None

        #first initialization
        self.load_config(CONFIG)


    def load_config(self, config=CONFIG):
        if not config:
            raise ValueErrorException

        def get_value(field):
            return config.get(self.__class__.__name__, field)

        self._dx = int(get_value("dx"))
        self._max_hull = int(get_value("max_hull"))
        self._max_shield = int(get_value("max_shield"))
        self._hull = int(get_value("hull"))
        self._shield = int(get_value("shield"))

        
    def move_left(self):
        self._dx = -1


    def move_right(self):
        self._dx = 1

    def add_weapon(self, weapon):
        self._weapon = weapon
        self._settings.renderer.add_object(self._weapon)


    def update(self):
        if self._pos.x == self._border.x - self._image.width - 1 and self._dx > 0:
            self._pos.x = self._border.x - self._image.width - 1
        elif self._pos.x == 1 and self._dx < 0:
            self._pos.x = 0


        self._weapon.update()

        if self._fire:
            self._weapon.make_shot(Point(x=self._pos.x + 1, y=self._pos.y))


    def get_render_data(self):
        return ([self._pos], self._image.get_image())
    

class GenericXEnemy(Ship):
    def __init__(self, pos, border, settings):
        super().__init__(pos, border, settings)
        self._image = Surface([['x', '^', 'x'],
                               [' ', 'X', ' '],
                               [' ', '*', ' ']])

        self._weapon = EBlaster()
        self._settings.renderer.add_object(self._weapon)
        self._fire = True

class Playership(Ship):

    def __init__(self, pos, border, settings):
        super().__init__(pos, border, settings)

        self._image = Surface([[' ',' ','O',' ',' '],
                               ['<','=','H','=','>'],
                               [' ','*',' ','*',' ']])

        self._pos = Point(x=pos.x - self._image.width // 2,
                          y=pos.y - self._image.height)
        self._border = border
        self._settings = settings

        self._fire = False
        self._weapons = InfList([Blaster(), Laser(), UM()])
        for weapon in self._weapons: self._settings.renderer.add_object(weapon)
        self._weapon = self._weapons.current()
        self._wbay = Point(x=self._image.width // 2, y=-1)

    def move_left(self):
        self._dx = -1

    def move_right(self):
        self._dx = 1

    def toggle_fire(self):
        self._fire = not self._fire

    def next_weapon(self):
        self._weapon = self._weapons.next()

    def prev_weapon(self):
        self._weapon = self._weapons.prev()

    def update(self):
        if self._pos.x == self._border.x - self._image.width - 1 and self._dx > 0:
            self._pos.x = 0
        elif self._pos.x == 1 and self._dx < 0:
            self._pos.x = self._border.x - self._image.width

        self._pos.x += self._dx
        self._dx = 0

        for weapon in self._weapons:
            weapon.update()
        if self._fire:
            try:
                self._weapon.make_shot(Point(x=self._pos.x + self._wbay.x,
                                             y=self._pos.y + self._wbay.y))
            except ValueError as e:
                self.next_weapon()

        self.refresh_shield()


    def get_weapon_info(self):
        return "Weapon: {w} | [{c}/{m}]".format(w=self._weapon.type,
                                                c=self._weapon.ammo,
                                                m=self._weapon.max_ammo)


    @property
    def max_hull(self):
        return self._max_hull


    @property
    def max_shield(self):
        return self._max_shield

    def get_full_hinfo(self):
        return self._hull, self._max_hull

    def get_full_sinfo(self):
        return self._shield, self._max_shield

    def get_full_winfo(self):
        return self._weapon.ammo, self._weapon.max_ammo

    def get_full_wcinfo(self):
        return self._weapon.current_cooldown, self._weapon.cooldown


    def get_render_data(self):
        return [self._pos], self._image.get_image()


    def get_renderable_objects(self):
        return self._weapons


    def take_damage(self, damage):
        if self._shield < damage:
            rest_damage = damage - self._shield
            self._shield = 0
            self._hull -= rest_damage
        else:
            self._shield -= damage
        if self._hull < 0:
            self._hull = 0


    def refresh_shield(self, amount=None):
        if self._shield == self._max_shield:
            return

        a = amount if amount else 1
        if self._shield + a > self._max_shield:
            self._shield = self._max_shield
        else:
            self._shield += a