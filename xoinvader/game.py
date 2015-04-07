#! /usr/bin/env python3

"""Main XOInvader module, that is entry point to game.

Prepare environment for starting game and start it."""

import sys
import time
import curses

from .gui import WeaponWidget, Bar
from .ship import GenericXEnemy, Playership
from .utils import Point, style, Layout
from .render import Renderer
from .common import Settings
from .curses_utils import create_curses_window, deinit_curses


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
    """Main game class that is game entry point.

    Create window, settings and pass them to appropriate objects when it's
    really needed.
    """

    def __init__(self):
        self.settings = Settings()
        self.settings.layout = Layout().init_layout()
        self.settings.border = self.settings.layout.field["border"]
        self.settings.field = Point(x=self.settings.border.x,
                                    y=self.settings.border.y-1)

        self.screen = create_curses_window(ncols=self.settings.border.x,
                                           nlines=self.settings.border.y)
        style.init_styles(curses)

        self.settings.renderer = Renderer(self.settings.border)

        self.playership = Playership(self.settings.layout.field["playership"],
                                     self.settings.field, self.settings)
        self.settings.renderer.add_object(self.playership)

        self.enemy = GenericXEnemy(Point(x=15, y=3), self.settings.field,
                                   self.settings)

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

        for state in ["good", "dmgd", "crit"]:
            self.wbar.status_style[state] = style.gui["dp_ok"]

        self.winfo = WeaponWidget(self.settings.layout.gui["winfo"],
                                  self.playership.get_weapon_info)

        self.gui = [self.hbar, self.sbar, self.wbar, self.winfo]
        for gui_object in self.gui:
            self.settings.renderer.add_object(gui_object)




    def events(self):
        """Handle events and give command to playership."""

        key = self.screen.getch()
        if key == K_ESCAPE:
            deinit_curses(self.screen)
            sys.exit(1)
        elif key == K_A:
            self.playership.move_left()
        elif key == K_D:
            self.playership.move_right()
        elif key == K_E:
            self.playership.next_weapon()
        elif key == K_Q:
            self.playership.prev_weapon()
        elif key == K_SPACE:
            self.playership.toggle_fire()
        elif key == K_R:
            self.playership.take_damage(5)


    def update(self):
        """Update all object's state."""
        self.playership.update()
        self.enemy.update()
        for gui_object in self.gui:
            gui_object.update()

    def render(self):
        """Render GUI and renderable objects to screen."""
        self.screen.erase()
        self.screen.border(0)
        self.screen.addstr(0, 2, "Score: {} ".format(0))
        self.screen.addstr(0, self.settings.field.x // 2 - 4,
                           "XOInvader", curses.A_BOLD)

        self.settings.renderer.render_all(self.screen)

        self.screen.refresh()

    def loop(self):
        """Main game loop."""
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
    """Entry point. Create application class and go to main loop."""
    app = App()
    app.loop()

if __name__ == "__main__":
    main()
