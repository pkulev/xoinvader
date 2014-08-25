#! /usr/bin/env python3

import sys
import time
import curses
from collections import namedtuple
from itertools import cycle


from render import Renderer, Renderable
from weapon import Blaster, Laser, UM
from utils import Point, Event, Surface, Color, Layout, InfList


KEY = "KEY"
K_Q = ord("q")
K_E = ord("e")
K_A = ord("a")
K_D = ord("d")
K_SPACE = ord(" ")
K_ESCAPE = 27


class Spaceship(Renderable):
    def __init__(self, pos, border, owner):
        self._image = Surface([[' ',' ','O',' ',' '],
                               ['<','=','H','=','>'],
                               [' ','*',' ','*',' ']])
        self._dx = 1
        self._pos = Point(x=pos.x - self._image.width // 2,
                          y=pos.y - self._image.height)
        self._border = border
        self._owner = owner

        self._fire = False
        self._weapons = InfList([Blaster(), Laser(), UM()])
        for weapon in self._weapons: self._owner.renderer.add_object(weapon)
        self._weapon = self._weapons.current()

        self._max_hull= 100
        self._max_shield = 100
        self._hull = 50
        self._shield = 50



    def move_left(self):
        self._dx = -1


    def move_right(self):
        self._dx = 1


    def toggle_fire(self):
        self._fire = not self._fire

    def fire(self):
        self._fire = True


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
                self._weapon.make_shot(Point(x=self._pos.x + self._image.width // 2,
                                             y=self._pos.y))
                self._fire = False
            except ValueError as e:
                self.next_weapon()


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


    def get_hinfo(self):
        return self._hull


    def get_sinfo(self):
        return self._shield


    def get_render_data(self):
        return [self._pos], self._image.get_image()




class Bar(Renderable):
    def __init__(self, title, pos, get_data, max_value):
        self._title = title
        self._pos = pos
        self._get_data = get_data
        self._value = self._get_data()
        self._max_value = max_value

        self._bar = "{title}: [{elements}]".format(title=self._title, elements=" "*10)
        self._image = Surface([[ch for ch in self._bar]])

        self.gui_style = curses.color_pair(Color.ui_norm) | curses.A_BOLD
        self.status_style = {"crit" : curses.color_pair(Color.dp_critical) | curses.A_BOLD,
                             "dmgd" : curses.color_pair(Color.dp_middle)   | curses.A_BOLD,
                             "good" : curses.color_pair(Color.dp_ok)       | curses.A_BOLD,
                             "blank": curses.color_pair(Color.dp_blank)}




    def _get_style(self, num):
        if num == -1:
            return self.status_style["blank"]

        if 70 <= num <= 100:
            return self.status_style["good"]
        elif 35 <= num < 70:
            return self.status_style["dmgd"]
        elif 0 <= num < 35:
            return self.status_style["crit"]

    def _generate_style_map(self):
        num = self._value * 10 // self._max_value

        elem_style = self._get_style(self._value)
        blank_style = self._get_style(-1)
        gui_style = self.gui_style

        m = []
        elem = 0
        in_bar = False
        for ch in self._bar:
            if ch == "[":
                m.append((ch, gui_style))
                in_bar = True
            elif ch == " " and in_bar:
                if elem < num:
                    m.append((ch, elem_style))
                else:
                    m.append((ch, blank_style))
                elem += 1
            elif ch == "]":
                in_bar = False
                m.append((ch, gui_style))
            else:
                m.append((ch, gui_style))

        return m


    def update(self):
        self._value = self._get_data()
        stylemap = self._generate_style_map()
        self._image = Surface([[ch[0] for ch in stylemap]], [[st[1] for st in stylemap]])


    def get_render_data(self):
        return [self._pos], self._image.get_image()


class App(object):
    def __init__(self):
        self.layout = Layout().init_layout()

        self.border = self.layout.field["border"]
        self.field  = Point(x=self.border.x, y=self.border.y-1)
        self.screen = self.create_window(x=self.border.x, y=self.border.y)
        #utils.

        self.renderer = Renderer()

        self.spaceship = Spaceship(self.layout.field["spaceship"], self.field, self)
        self.renderer.add_object(self.spaceship)

        #gui

        self.hbar = Bar("Hull",   self.layout.gui["hbar"], self.spaceship.get_hinfo, self.spaceship.max_hull)
        self.sbar = Bar("Shield", self.layout.gui["sbar"], self.spaceship.get_sinfo, self.spaceship.max_shield)
        #temp... or not?
        self.sbar.status_style["good"] = curses.color_pair(Color.sh_ok)  | curses.A_BOLD
        self.sbar.status_style["dmgd"] = curses.color_pair(Color.sh_mid) | curses.A_BOLD
        self.renderer.add_object(self.hbar)
        self.renderer.add_object(self.sbar)


    def create_window(self, x, y, a=0, b=0):
        curses.initscr()
        curses.start_color()

        #user interface
        curses.init_pair(Color.ui_norm, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(Color.ui_yellow, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        #damage panel
        curses.init_pair(Color.dp_blank, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(Color.dp_ok, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(Color.dp_middle, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(Color.dp_critical, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(Color.sh_ok, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(Color.sh_mid, curses.COLOR_WHITE, curses.COLOR_CYAN)

        #weapons
        curses.init_pair(Color.blaster, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(Color.laser, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(Color.um, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        screen = curses.newwin(y, x, a, b)
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
            self.spaceship.fire()


    def update(self):
        self.spaceship.update()
        self.hbar.update()
        self.sbar.update()


    def render(self):
        self.screen.erase()
        self.screen.border(0)
        self.screen.addstr(0, 2, "Score: {} ".format(0))
        self.screen.addstr(0, self.field.x // 2 - 4, "XOInvader", curses.A_BOLD)



        weapon_info = self.spaceship.get_weapon_info()
        self.screen.addstr(self.field.y, self.field.x - len(weapon_info) - 2, weapon_info,
                            (curses.color_pair(Color.ui_yellow) | curses.A_BOLD))


        self.renderer.render_all(self.screen)


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
