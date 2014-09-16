#! /usr/bin/env python3

import sys
import time
import curses
from collections import namedtuple

from ship import GenericXEnemy, Playership
from render import Renderer, Renderable
from utils import Point, Event, Surface, Color, Style, Layout


KEY = "KEY"
K_Q = ord("q")
K_E = ord("e")
K_A = ord("a")
K_D = ord("d")
K_R = ord("r")
K_SPACE = ord(" ")
K_ESCAPE = 27

MILLISECONDS_PER_FRAME = 16
style = Style()


class WeaponWidget(Renderable):
    def __init__(self, pos, get_data):
        self._pos = pos
        self._get_data = get_data
        self._data = self._get_data()
        self._image = self._make_image()

    def _make_image(self):
        return Surface([[ch for ch in self._data]],
                       [[curses.color_pair(Color.ui_yellow)
                       | curses.A_BOLD for _ in range(len(self._data))]])



    def update(self):
        self._data = self._get_data()
        self._image = self._make_image()
        open("lol.log", "w").write(str(self._data))

    def get_render_data(self):
        return [self._pos], self._image.get_image()

class Bar(Renderable):
    def __init__(self, title, pos, get_data, update_all=False):
        self._title = title
        self._pos = pos
        self._get_data = get_data
        self._value = self._get_data()[0]
        self._max_value = self._get_data()[1]
        self._update_all = update_all

        self._bar = "{title}: [{elements}]".format(title=self._title, elements=" "*10)
        self._image = Surface([[ch for ch in self._bar]])

        self.gui_style = style.gui["normal"]
        self.status_style = {"crit" : style.gui["dp_critical"],
                             "dmgd" : style.gui["dp_middle"],
                             "good" : style.gui["dp_ok"],
                             "blank": style.gui["dp_blank"]
                             }


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

        num_percent = self._value * 100 // self._max_value
        elem_style = self._get_style(num_percent)
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
        self._value = self._get_data()[0]
        if self._update_all:
            self._max_value = self._get_data()[1]
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
        style.init_styles(curses)

        self.renderer = Renderer(self.border)

        self.playership = Playership(self.layout.field["playership"], self.field, self)
        self.renderer.add_object(self.playership)

        self.enemy = GenericXEnemy(Point(x=15, y=3), self.field, self)
        self.renderer.add_object(self.enemy)
        #gui

        self.hbar = Bar("Hull",
                        self.layout.gui["hbar"],
                        self.playership.get_full_hinfo)

        self.sbar = Bar("Shield",
                        self.layout.gui["sbar"],
                        self.playership.get_full_sinfo)

        self.sbar.status_style["good"] = style.gui["sh_ok"]
        self.sbar.status_style["dmgd"] = style.gui["sh_mid"]

        self.wbar = Bar("", self.layout.gui["wbar"],
                            self.playership.get_full_wcinfo,
                            update_all=True)

        for s in ["good", "dmgd", "crit"]:
            self.wbar.status_style[s] = style.gui["dp_ok"]

        self.winfo = WeaponWidget(self.layout.gui["winfo"],
                                  self.playership.get_weapon_info)

        self.gui = [self.hbar, self.sbar, self.wbar, self.winfo]
        for e in self.gui: self.renderer.add_object(e)


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
            self.playership.move_left()
        elif c == K_D:
            self.playership.move_right()
        elif c == K_E:
            self.playership.next_weapon()
        elif c == K_Q:
            self.playership.prev_weapon()
        elif c == K_SPACE:
            self.playership.toggle_fire()
        elif c == K_R:
            self.playership.take_damage(5)


    def update(self):
        self.playership.update()
        self.enemy.update()
        for e in self.gui: e.update()


    def render(self):
        self.screen.erase()
        self.screen.border(0)
        self.screen.addstr(0, 2, "Score: {} ".format(0))
        self.screen.addstr(0, self.field.x // 2 - 4, "XOInvader", curses.A_BOLD)

        self.renderer.render_all(self.screen)

        self.screen.refresh()

    def loop(self):
        while True:
            start_time = time.perf_counter()

            self.events()
            self.update()
            self.render()

            finish_time = time.perf_counter()
            delta = finish_time - start_time
            if delta <= MILLISECONDS_PER_FRAME:
                time.sleep((MILLISECONDS_PER_FRAME - delta) / 1000.0)
            #else: log
def main():
    app = App()
    app.loop()

if __name__ == "__main__":
    main()
