#! /usr/bin/env python3

import sys
import time
import curses
from collections import namedtuple

from gui import WeaponWidget, Bar
from ship import GenericXEnemy, Playership
from utils import Point, Event, Surface, Color, style, Layout
from render import Renderer, Renderable
from common import Settings


KEY = "KEY"
K_Q = ord("q")
K_E = ord("e")
K_A = ord("a")
K_D = ord("d")
K_R = ord("r")
K_SPACE = ord(" ")
K_ESCAPE = 27

MILLISECONDS_PER_FRAME = 16


class App(object):
    
    settings = Settings()
    
    def __init__(self):
        self.settings.layout = Layout().init_layout()
        self.settings.border = self.settings.layout.field["border"]
        self.settings.field  = Point(x=self.settings.border.x, y=self.settings.border.y-1)

        self.screen = self.create_window(x=self.settings.border.x, y=self.settings.border.y)
        style.init_styles(curses)

        self.settings.renderer = Renderer(self.settings.border)

        self.playership = Playership(self.settings.layout.field["playership"], self.settings.field, self.settings)
        self.settings.renderer.add_object(self.playership)

        self.enemy = GenericXEnemy(Point(x=15, y=3), self.settings.field, self.settings)
        self.settings.renderer.add_object(self.enemy)
        #gui

        self.hbar = Bar("Hull",
                        self.settings.layout.gui["hbar"],
                        self.playership.get_full_hinfo)

        self.sbar = Bar("Shield",
                        self.settings.layout.gui["sbar"],
                        self.playership.get_full_sinfo)

        self.sbar.status_style["good"] = style.gui["sh_ok"]
        self.sbar.status_style["dmgd"] = style.gui["sh_mid"]

        self.wbar = Bar("", self.settings.layout.gui["wbar"],
                            self.playership.get_full_wcinfo,
                            update_all=True)

        for s in ["good", "dmgd", "crit"]:
            self.wbar.status_style[s] = style.gui["dp_ok"]

        self.winfo = WeaponWidget(self.settings.layout.gui["winfo"],
                                  self.playership.get_weapon_info)

        self.gui = [self.hbar, self.sbar, self.wbar, self.winfo]
        for e in self.gui: self.settings.renderer.add_object(e)


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
        self.screen.addstr(0, self.settings.field.x // 2 - 4, "XOInvader", curses.A_BOLD)

        self.settings.renderer.render_all(self.screen)

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
