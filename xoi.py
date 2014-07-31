#! /usr/bin/env python3

import sys
import time
import curses
from collections import namedtuple


from render import Renderer
from weapon import Weapon
from utils import Point, Event, Surface, Color, Layout


KEY = "KEY"
K_Q = ord("q")
K_E = ord("e")
K_A = ord("a")
K_D = ord("d")
K_SPACE = ord(" ")
K_ESCAPE = 27


class Spaceship(object):
    def __init__(self, pos, border):
        self.__image = Surface([[' ',' ','O',' ',' '],
                                ['<','=','H','=','>'],
                                [' ','*',' ','*',' ']])
        self.__dx = 1
        self.__pos = Point(x=pos.x - self.__image.width // 2,
                           y=pos.y - self.__image.height) 
        self.__border = border

        self.__fire = False
        self.__weapons = [Weapon()("Blaster"), Weapon()("Laser"), Weapon()("UM")]
        self.__weapon = self.__weapons[0]

        self.__max_hull= 100
        self.__max_shield = 100
        self.__hull = 100
        self.__shield = 100



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
                self.__weapon.make_shot(Point(x=self.__pos.x + self.__image.width // 2,
                                              y=self.__pos.y))
            except ValueError as e:
                self.next_weapon()


    #@property
    #def image(self):
    #    return self.__image


    @property
    def pos(self):
        return self.__pos


    def get_weapon_info(self):
        return "Weapon: {w} | [{c}/{m}]".format(w=self.__weapon.type,
                                                c=self.__weapon.ammo,
                                                m=self.__weapon.max_ammo)



    @property
    def max_hull(self):
        return self.__max_hull


    @property
    def max_shield(self):
        return self.__max_shield


    def get_hinfo(self):
        return self.__hull


    def get_sinfo(self):
        return self.__shield


    def get_render_data(self):
        return self.__pos, self.__image.get_image()




class Bar(object):
    def __init__(self, title, pos, get_data, max_value):
        self.__title = title
        self.__pos = pos
        self.__get_data = get_data
        self.__value = self.__get_data()
        self.__max_value = max_value

        self.__bar = "{title}: [{elements}]".format(title=self.__title, elements=" "*10)
        self.__image = Surface([[ch for ch in self.__bar]])

        self.gui_style = Color.ui_norm | curses.A_BOLD
        self.status_style = {"crit" : Color.dp_critical | curses.A_BLINK | curses.A_BOLD,
                             "dmgd" : Color.dp_middle   | curses.A_BOLD,
                             "good" : Color.dp_ok       | curses.A_BOLD,
                             "blank": Color.dp_blank}




    def __get_style(self, num):
        if num == -1:
            return self.status_style["blank"]

        if 0 <= num < 35:
            return self.status_style["crit"]
        elif 25 <= num < 70:
            return self.status_style["dmgd"]
        elif 70 <= num <= 100:
            return self.status_style["good"]

    def __generate_style_map(self):
        num = self.__value * 10 // self.__max_value

        elem_style = self.__get_style(num)
        blank_style = self.__get_style(-1)
        gui_style = self.gui_style

        m = []
        elem = 0
        in_bar = False
        for ch in self.__bar:
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

    def testmap(self):
        st = self.status_style["dmgd"]
        return [(ch, curses.A_BLINK) for ch in self.__bar]

    def update(self):
        self.__value = self.__get_data()
        stylemap = self.testmap() #self.__generate_style_map()
        self.__image = Surface([[ch[0] for ch in stylemap]], [[st[1] for st in stylemap]])


    def get_render_data(self):
        return self.__pos, self.__image.get_image()


class App(object):
    def __init__(self):
        self.layout = Layout().init_layout()

        self.border = self.layout.field["border"]
        self.field  = Point(x=self.border.x, y=self.border.y-1)
        self.screen = self.create_window(x=self.border.x, y=self.border.y)

        self.renderer = Renderer()

        self.spaceship = Spaceship(self.layout.field["spaceship"], self.field)
        self.renderer.add_object(self.spaceship)

        #gui

        self.hbar = Bar("Hull",   self.layout.gui["hbar"], self.spaceship.get_hinfo, self.spaceship.max_hull)
        self.sbar = Bar("Shield", self.layout.gui["sbar"], self.spaceship.get_sinfo, self.spaceship.max_shield)
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
            self.spaceship.toggle_fire()


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


        #Render cannons
        image, coords = self.spaceship._Spaceship__weapon.get_data()
        for pos in coords:
            self.screen.addstr(pos.y, pos.x, image, curses.color_pair(Color.laser) | curses.A_BOLD)

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
