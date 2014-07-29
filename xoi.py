#! /usr/bin/env python3

import sys
import time
import curses
from collections import namedtuple


from render import Renderer
from weapon import Weapon
from utils import Point, Event, Surface


KEY = "KEY"
K_Q = ord("q")
K_E = ord("e")
K_A = ord("a")
K_D = ord("d")
K_SPACE = ord(" ")
K_ESCAPE = 27


class Spaceship(object):
    def __init__(self, border):
        self.__image = Surface([[' ','O',' '],
                                ['/','H','\\'],
                                [' ','*',' ']])
        self.__dx = 1
        self.__border = border
        self.__pos = Point(self.__border.x // 2 - self.__image.width // 2,
                           self.__border.y - self.__image.height)
        self.__fire = False
        self.__weapons = [Weapon()("Blaster"), Weapon()("Laser"), Weapon()("UM")]
        self.__weapon = self.__weapons[0]
        self.__hull = 100
        self.__shield = 100

        self.h_bar = Bar(self.__hull, 100, title="Hull")
        self.s_bar = Bar(self.__shield, 100, title="Shield")


    def move_left(self):
        self.__dx = -1


    def move_right(self):
        self.__dx = 1

    def toggle_fire(self):
        self.__fire = not self.__fire

    def next_weapon(self):
        ind = self.__weapons.index(self.__weapon)
        if ind < len(self.__weapons) - 1:
            self.__weapon = self.__weapons[ind+1]
        else:
            self.__weapon = self.__weapons[0]



    def prev_weapon(self):
        ind = self.__weapons.index(self.__weapon)
        if ind == 0:
            self.__weapon = self.__weapons[len(self.__weapons) - 1]
        else:
            self.__weapon = self.__weapons[ind - 1]


    def update(self):
        if self.__pos.x == self.__border.x - self.__image.width - 1 and self.__dx > 0:
            self.__pos.x = 0
        elif self.__pos.x == 1 and self.__dx < 0:
            self.__pos.x = self.__border.x - self.__image.width

        self.__pos.x += self.__dx
        self.__dx = 0

        self.__weapon.update()
        if self.__fire:
            try:
                self.__weapon.make_shot(Point(x=self.__pos.x + 1, y=self.__pos.y))
            except ValueError as e:
                self.next_weapon()


        #!!!!
        self.h_bar.update_value(self.__hull)
        self.s_bar.update_value(self.__shield)

    @property
    def image(self):
        return self.__image

    @property
    def pos(self):
        return self.__pos


    def get_weapon_info(self):
        return "Weapon: {w} | [{c}/{m}]".format(w=self.__weapon.type,
                                                c=self.__weapon.ammo,
                                                m=self.__weapon.max_ammo)

    def get_health_info(self):
        return (self.__hull, self.__shield)


    def get_render_data(self):
        return self.__pos, self.__image.get_image()


LOW = 3
MEDIUM = 4
HIGH = 5
BLANK = 6

class Bar(object):
    def __init__(self, value, max_value, title=None):
        self.__title = title + ": " if title else None
        self.__value = value
        self.__max_value = max_value
        self.__elems = 0 if self.__value <= 0 else round(self.__value * 10 / self.__max_value)
        self.__start = "["
        self.__end = "]"
        self.__elem = " "
        self.__style = curses.A_BOLD



    def update_value(self, val):
        self.__value = 0 if val < 0 else val



    def render(self, screen, pos):
        if self.__title:
            screen.addstr(pos.y, pos.x, self.__title, self.__style)
            pos.x += len(self.__title)

        screen.addstr(pos.y, pos.x, self.__start, self.__style)
        for i in range(1, self.__elems + 1):
            pos.x += 1
            if i in (1, 2, 3): #RED
                screen.addstr(pos.y, pos.x, self.__elem, curses.color_pair(LOW) | self.__style)
            elif i in (4,5,6):
                screen.addstr(pos.y, pos.x, self.__elem, curses.color_pair(MEDIUM) | self.__style)
            else:
                screen.addstr(pos.y, pos.x, self.__elem, curses.color_pair(HIGH) | self.__style)
        pos.x += 1
        screen.addstr(pos.y, pos.x, self.__end, self.__style)

        return Point(x=pos.x, y=pos.y)


class App(object):
    def __init__(self):

        self.border = Point(x=80, y=24)
        self.field  = Point(x=self.border.x, y=self.border.y-1)
        self.screen = self.create_window(x=self.border.x, y=self.border.y)

        self.renderer = Renderer()

        self.spaceship = Spaceship(self.field)
        self.renderer.add_object(self.spaceship)


    def create_window(self, x, y, a=0, b=0):
        curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_RED)
        curses.init_pair(LOW, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(MEDIUM, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(HIGH, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(BLANK, curses.COLOR_BLACK, curses.COLOR_BLACK)
        screen = curses.newwin(y, x, 0, 0)
        screen.keypad(1)
        screen.nodelay(1)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        return screen


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
        elif c == K_E:
            self.spaceship.next_weapon()
        elif c == K_Q:
            self.spaceship.prev_weapon()
        elif c == K_SPACE:
            self.spaceship.toggle_fire()


    def update(self):
        self.spaceship.update()


    def render(self):
        self.screen.erase()
        self.screen.border(0)
        self.screen.addstr(0, 2, "Score: {} ".format(0))
        self.screen.addstr(0, self.border.x // 2 - 4, "XOInvader", curses.A_BOLD)



        weapon_info = self.spaceship.get_weapon_info()
        self.screen.addstr(self.border.y - 1, self.border.x - len(weapon_info) - 2, weapon_info,
                            (curses.color_pair(1) | curses.A_BOLD))



        #!!!!
        hull, shield = self.spaceship.get_health_info()
        end = self.spaceship.h_bar.render(self.screen, Point(y=self.border.y - 1, x=2))
        self.spaceship.s_bar.render(self.screen, Point(y=end.y, x=end.x + 2))



        self.renderer.render_all(self.screen)


        #Render cannons
        image, coords = self.spaceship._Spaceship__weapon.get_data()
        for pos in coords:
            self.screen.addstr(pos.y, pos.x, image, curses.color_pair(2) | curses.A_BOLD)

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
