#! /usr/bin/env python

import sys
import curses
from curses import KEY_ENTER
import time
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

def Weapon(w_class, w_ammo=-1, w_time=-1):
    from abc import ABCMeta
    class AbstractWeapon(object, metaclass=ABCMeta):
        def __init__(self, image, damage, ammo, delay, radius):
            self.__type == None

            self.__image = image
            self.__damage = damage
            self.__ammo = ammo
            self.__delay = delay

            self.__coords = []

            #Behaviour
            self.update = None
            self.render = None


        @property
        def image(self):
            return self.__image


        #TODO:
        def __iter__(self):
            return (c for c in self._coords)

        @classmethod
        def create_weapon(cls, w_type, behaviour=None):
            weapons = {
                    "Blaster": cls(image="^", damage=1, ammo=-1, delay= 5, radius=0),
                    "Laser"  : cls(image="|", damage=2, ammo=10, delay=10, radius=0),
                    "NCRC"   : cls(image="*", damage=5, ammo= 5, delay=15, radius=2),
                    }
            try:
                weapon = weapons[w_type]
                weapon.__type = w_type
                weapon.behaviour = None

            except KeyError as e:
                print("No such weapon type! Error: {}".format(str(e))); return None
            except:
                print("Unhandled exception! Error: {}".format(str(e))); return None

        def update(self):
            pass

        def render(self, screen):
            pass

        create_weapon = lambda w_class, *args, **kwargs: w_class(*args, **kwargs)

    weapons = {
            "Laser" : None,
            "Blaster" : None,
            "Rocket" : None,
            }
    if not weapons.has_key(w_class):
        raise KeyError("No such weapon class")
    return weapons[w_class]

class Spaceship(object):
    def __init__(self, border):
        self.__image = "<i>"
        self.__dx = 1
        self.__border = border
        self.__pos = Point(self.__border.x // 2, self.__border.y - 1)
        self.__fire = False
        #self.__weapon = Weapon(type="Laser", ammo=-1)

    def events(self, event):
        if event.type == KEY:
            if event.val == K_A:
                self.__dx = -1
            if event.val == K_D:
                self.__dx = 1
            if event.val == K_SPACE:
                self.__fire = True if self.__fire else False

    def update(self):
        if self.__pos.x == self.__border.x - len(self.__image) - 1 and self.__dx > 0:
            self.__pos.x = 0
        elif self.__pos.x == 1 and self.__dx < 0:
            self.__pos.x = self.__border.x - len(self.__image)

        self.__pos.x += self.__dx
        self.__dx = 0

        if self.__fire:
            pass


    def draw(self, screen):
        screen.addstr(self.__pos.y, self.__pos.x, self.__image, curses.A_BOLD)



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
        else:
            for o in self._objects:
                o.events(Event(type="KEY", val=c))

    def update(self):
        for o in self._objects:
            o.update()

    def render(self):
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(0, 2, "Score: {} ".format(0))
        self.screen.addstr(0, self.border.x // 2 - 4, "XOInvader", curses.A_BOLD)
        for o in self._objects:
            o.draw(self.screen)
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
