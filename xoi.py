#! /usr/bin/env python

import sys
import curses
from curses import KEY_ENTER
import time
from collections import namedtuple


KEY = "KEY"
K_A = ord("a")
K_D = ord("d")

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


class Spaceship(object):
    def __init__(self, border):
        self._image = "<i>"
        self._dx = 1
        self.border = border
        self._pos = Point(self.border.x // 2, self.border.y - 1)


    def events(self, event):
        if event.type == KEY:
            if event.val == K_A:
                self._dx = -1
            if event.val == K_D:
                self._dx = 1

    def update(self):
        if self._pos.x == self.border.x - len(self._image) - 1 and self._dx > 0:
            self._pos.x = 0
        elif self._pos.x == 1 and self._dx < 0:
            self._pos.x = self.border.x - len(self._image)

        self._pos.x += self._dx
        self._dx = 0

    def draw(self, screen):
        screen.addstr(self._pos.y, self._pos.x, self._image, curses.A_BOLD)



class App(object):
    def __init__(self):
        #self.screen = curses.initscr()
        curses.initscr()
        self.border = namedtuple("border", ["y", "x"])(24, 80)
        self.field  = namedtuple("field", ["y", "x"])(self.border.y-1, self.border.x)
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
        if c == 27: #Escape
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
        self.screen.addstr(0, 2, "Score: {}".format(0))
        self.screen.addstr(0, self.border.x // 2 - 4, "XOInvader", curses.A_BOLD)
        for o in self._objects:
            o.draw(self.screen)
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
