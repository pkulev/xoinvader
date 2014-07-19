#! /usr/bin/env python

import sys
import time
import curses
from collections import namedtuple


KEY = "KEY"
K_A = ord("a")
K_D = ord("d")
K_SPACE = ord(" ")
K_ESCAPE = 27
#fix freezes [issue#1]
KEYS = [K_A, K_D, K_SPACE, K_ESCAPE]


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val


Event = namedtuple("Event", ["type", "val"])

class WeaponBay(object):
    class __Pylons(object):
        """Aircraft weapon pylons data structure"""
        def __init__(self, l, m, h):
            self.light = l
            self.medium = m
            self.h = h

        def get_all(self, struct=tuple):
            return struct(l, m, h)

        def add(self, pylon, weapon):
            pass

    def __init__(self, light, medium, heavy):
        self.__pylons = __Pylons(light, medium, heavy)
        self.__cwg = self.__pylons.light

    #pos is the center pos?
    def cwg_fire(self, pos):
        for weapon in self.__cwg:
            if weapon.ammo == "inf" or self.weapon.ammo > 0:
                weapon.make_shot(pos)

    def add_weapon(self, weapon, pylon):
        self.__pylons.add(weapon, pylon)

class Weapon(object):
    def __init__(self, image=None, max_ammo=None, ammo=None, cooldown=None, damage=None, radius=None, dy=None):
        self.__image = image
        self.__max_ammo = max_ammo
        self.__ammo = ammo
        self.__cooldown = cooldown
        self.__damage = damage
        self.__radius = radius
        self.__dy = dy

        self.__coords = []


    def __call__(self, w_type):
        weapons = {"Blaster": Weapon(image="^", max_ammo=-1, ammo=-1, cooldown=1, damage=1, radius=0, dy=-1),
                   "Laser"  : Weapon(image="|", max_ammo=50, ammo=50, cooldown=5, damage=2, radius=-1,dy=-1),
                   "UM"     : Weapon(image="*", max_ammo=15, ammo=15, cooldown=7, damage=5, radius=2, dy=-1),
            }
        return weapons[w_type]


    def make_shot(self, pos):
        self.__coords.append(Point(x=pos.x, y=pos.y - 1))

    @property
    def ammo(self):
        return self.__ammo

    def get_data(self):
        return (self.__image, self.__coords)

    def update(self):
        new_coords = []
        for i in self.__coords:
            if i.y + self.__dy > 0:
                new_coords.append(Point(x=i.x, y=i.y + self.__dy))
        self.__coords = new_coords[:]



class Spaceship(object):
    def __init__(self, border):
        self.__image = "<i>"
        self.__dx = 1
        self.__border = border
        self.__pos = Point(self.__border.x // 2 - len(self.__image), self.__border.y - 1)
        self.__fire = False
        self.__weapon = Weapon()("Blaster")

        #self.__weapon_bay = WeaponBay()
        #self.__weapon_bay.add_weapon(wp)
        #self.__weapon_bay.remove_veapon(wp)


    def move_left(self):
        self.__dx = -1


    def move_right(self):
        self.__dx = 1

    def toggle_fire(self):
        self.__fire = not self.__fire


    def update(self):
        if self.__pos.x == self.__border.x - len(self.__image) - 1 and self.__dx > 0:
            self.__pos.x = 0
        elif self.__pos.x == 1 and self.__dx < 0:
            self.__pos.x = self.__border.x - len(self.__image)

        self.__pos.x += self.__dx
        self.__dx = 0

        self.__weapon.update()
        if self.__fire:
            self.__weapon.make_shot(Point(x=self.__pos.x + 1, y=self.__pos.y))

    @property
    def image(self):
        return self.__image

    @property
    def pos(self):
        return self.__pos


class App(object):
    def __init__(self):
        curses.initscr()
        self.border = Point(x=80, y=24)
        self.field  = Point(x=self.border.x, y=self.border.y-1)
        self.screen = curses.newwin(self.border.y, self.border.x, 0, 0)
        self.screen.keypad(1)
        self.screen.nodelay(1)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.spaceship = Spaceship(self.field)
        self._objects = []
        self._objects.append(self.spaceship)

    def deinit(self):
        self.screen.nodelay(0)
        self.screen.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()


    def events(self):
        c = self.screen.getch()
        if c == K_ESCAPE:
            self.deinit()
            sys.exit(1)
        elif c == K_A:
            self.spaceship.move_left()
        elif c == K_D:
            self.spaceship.move_right()
        elif c == K_SPACE:
            self.spaceship.toggle_fire()


    def update(self):
        self.spaceship.update()


    def render(self):
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(0, 2, "Score: {} ".format(0))
        self.screen.addstr(0, self.border.x // 2 - 4, "XOInvader", curses.A_BOLD)

        #Render spaceship
        self.screen.addstr(self.spaceship.pos.y, self.spaceship.pos.x,
                           self.spaceship.image, curses.A_BOLD)

        #Render cannons
        image, coords = self.spaceship._Spaceship__weapon.get_data()
        for pos in coords:
            self.screen.addstr(pos.y, pos.x, image)

        self.screen.refresh()
        time.sleep(0.03)

    def loop(self):
        while True:
            self.events()
            self.update()
            self.render()

def main():
    app = App()
    app.loop()

if __name__ == "__main__":
    main()
