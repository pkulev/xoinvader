from utils import Point, Surface


class Weapon1(object):
    def __init__(self, ammo=None, mapping=None):
        self._type = "__basic__"
        self._image = None
        self._max_ammo = None
        self._ammo = ammo

class Blaster(Weapon1):
    def __init__(self, ammo=None, mapping=None):
        super().__init__(ammo, mapping)
        with open("log", "w") as l: l.write(str(self._ammo))


class Weapon(object):
    def __init__(self, w_type=None, image=None, max_ammo=None, ammo=None, cooldown=None, damage=None, radius=None, dy=None):
        self._type = w_type
        self._image = image
        self._max_ammo = max_ammo
        self._ammo = ammo
        self._cooldown = cooldown
        self._damage = damage
        self._radius = radius
        self._dy = dy

        self._coords = []


    def __call__(self, w_type):
        weapons = {"Blaster": Weapon(w_type=w_type, image="^", max_ammo=-1, ammo=-1, cooldown=1, damage=1, radius=0, dy=-1),
                   "Laser"  : Weapon(w_type=w_type, image="|", max_ammo=50, ammo=50, cooldown=5, damage=2, radius=-1,dy=-1),
                   "UM"     : Weapon(w_type=w_type, image="*", max_ammo=15, ammo=15, cooldown=7, damage=5, radius=2, dy=-1),
            }
        return weapons[w_type]


    def make_shot(self, pos):
        if self._ammo == -1 or self._ammo > 0:
            self._coords.append(Point(x=pos.x, y=pos.y - 1))
        if self._ammo > 0: self._ammo -= 1
        if self._ammo == 0: raise ValueError("No ammo!")


    @property
    def ammo(self):
        return 999 if self._ammo == -1 else self._ammo


    @property
    def max_ammo(self):
        return 999 if self._ammo == -1 else self._max_ammo


    @property
    def type(self):
        return self._type


    def get_data(self):
        return (self._image, self._coords)


    def update(self):
        new_coords = []
        for i in self._coords:
            if i.y + self._dy > 0:
                new_coords.append(Point(x=i.x, y=i.y + self._dy))
        self._coords = new_coords[:]

if __name__ == "__main__":
    w = Blaster(5)

