from utils import Point


class WeaponBay(object):

    def __init__(self, light=None, medium=None, heavy=None):

        self.__pylons = {"light": light if light else None,
                         "medium": medium if medium else None,
                         "heavy": heavy if heavy else None}

        self.__cwg = self.__pylons.light

    #pos is the center pos?
    def cwg_fire(self, pos):
        for weapon in self.__cwg:
            if weapon.ammo == "inf" or self.weapon.ammo > 0:
                weapon.make_shot(pos)


    def add_weapon(self, weapon, pylon):
        self.__pylons.add(weapon, pylon)



class Weapon(object):
    def __init__(self, w_type=None, image=None, max_ammo=None, ammo=None, cooldown=None, damage=None, radius=None, dy=None):
        self.__type = w_type
        self.__image = image
        self.__max_ammo = max_ammo
        self.__ammo = ammo
        self.__cooldown = cooldown
        self.__damage = damage
        self.__radius = radius
        self.__dy = dy

        self.__coords = []


    def __call__(self, w_type):
        weapons = {"Blaster": Weapon(w_type=w_type, image="^", max_ammo=-1, ammo=-1, cooldown=1, damage=1, radius=0, dy=-1),
                   "Laser"  : Weapon(w_type=w_type, image="|", max_ammo=50, ammo=50, cooldown=5, damage=2, radius=-1,dy=-1),
                   "UM"     : Weapon(w_type=w_type, image="*", max_ammo=15, ammo=15, cooldown=7, damage=5, radius=2, dy=-1),
            }
        return weapons[w_type]


    def make_shot(self, pos):
        if self.__ammo == -1 or self.__ammo > 0:
            self.__coords.append(Point(x=pos.x, y=pos.y - 1))
        if self.__ammo > 0: self.__ammo -= 1
        if self.__ammo == 0: raise ValueError("No ammo!")


    @property
    def ammo(self):
        return 999 if self.__ammo == -1 else self.__ammo


    @property
    def max_ammo(self):
        return 999 if self.__ammo == -1 else self.__ammo


    @property
    def type(self):
        return self.__type


    def get_data(self):
        return (self.__image, self.__coords)


    def update(self):
        new_coords = []
        for i in self.__coords:
            if i.y + self.__dy > 0:
                new_coords.append(Point(x=i.x, y=i.y + self.__dy))
        self.__coords = new_coords[:]


