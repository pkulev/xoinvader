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

from abc import ABCMeta, abstractmethod

class IWeapon(object):
    __metaclass__ = ABCMeta
    def __init__(self, ammo):
        self.__image = None
        self.__damage = None
        self.__max_ammo = None
        self.__ammo = ammo
        self.__delay = None

        self.__coords = []

        self.update = None
        self.render = None

    @abstractmethod
    def make_shot(self):
        raise NotImplemented

    @property
    def image(self):
        return self.__image

    #TEMP:
    #until good colision detection code is implemented
    @property
    def coords(self):
        return self.__coords[:]


class IWeaponUpdateBehaviour(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        pass

    @abstractmethod
    def update(self):
        raise NotImplemented


class IWeaponRenderBehaviour(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        pass

    @abstractmethod
    def render(self):
        raise NotImplemented


class Blaster(IWeapon):
    def __init__(self, border, ammo):
        IWeapon.__init__(self, ammo)
        self.__image = "^"
        self.__dy = 1
        self.__max_ammo = 100
        self.__delay = 1
        self.__radius = 0
        self.__damage = 1

        #!!!!
        self.__border = border
        #!!!!
        self.__coords = []

    def make_shot(self, pos):
        self.__coords.append(pos)

    def update(self):
        for i in range(len(self.__coords) - 1):
            if self.__coords[i].y == self.border.y - 1:
                self.__coords.remove(i)
            else:
                self.__coords[i] = Point(self.__coords[i].x, self.__coords[i].y + self.__dy)


class Spaceship(object):
    def __init__(self, border):
        self.__image = "<i>"
        self.__dx = 1
        self.__border = border
        self.__pos = Point(self.__border.x // 2 - len(self.__image), self.__border.y - 1)
        self.__fire = False
        self.__weapon = Blaster(self.__border, 50)

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

        if self.__fire:
            self.__weapon.make_shoot()

    @property
    def image(self):
        return self.__image

    @property
    def pos(self):
        return self.__pos


class App(object):
    def __init__(self):
        #self.screen = curses.initscr()
        curses.initscr()
        self.border = Point(x=80, y=24)
        self.field  = Point(x=self.border.x, y=self.border.y-1)
        self.screen = curses.newwin(self.border.y, self.border.x, 0, 0)
        self.screen.keypad(1)
        self.screen.nodelay(1)
        curses.noecho()
        #curses.cbreak()
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
        for c in self.spaceship.weapon.coords:
            self.screen.addstr(c.y, c.x, self.spaceship.weapon.image)

        self.screen.refresh()
        time.sleep(0.03)

    def loop(self):
        while True:
            self.events()
            self.update()
            try:
                self.render()
            except:
                self.deinit()
                sys.exit(1)
def main():
    app = App()
    app.loop()

if __name__ == "__main__":
    main()
