#! /usr/bin/env python3

"""Main XOInvader module, that is entry point to game.

Prepare environment for starting game and start it."""

import sys
import time
import curses

from xoinvader.gui import WeaponWidget, Bar
from xoinvader.ship import GenericXEnemy, Playership
from xoinvader.utils import Point
from xoinvader.render import Renderer
from xoinvader.common import Settings
from xoinvader.settings import dotdict
from xoinvader.input_handler import InputHandler, ExitGameCommand
from xoinvader.curses_utils import create_curses_window, deinit_curses, style


MILLISECONDS_PER_FRAME = 16


class App(object):
    """Main game class that is game entry point.

    Create window, settings and pass them to appropriate objects when it's
    really needed.
    """

    def __init__(self, startup_args={}):
        self._update_settings_from_args(startup_args)
        self.screen = create_curses_window(ncols=Settings.layout.field.border.x,
                                           nlines=Settings.layout.field.border.y)
        style.init_styles(curses)
        Settings.renderer = Renderer(Settings.layout.field.border)

        self.playership = Playership(Settings.layout.field.player,
                                     Settings.layout.field.edge, Settings)
        Settings.renderer.add_object(self.playership)

        self.enemy = GenericXEnemy(Point(x=15, y=3), Settings.layout.field.edge,
                                   Settings)

        Settings.renderer.add_object(self.enemy)
        #gui

        self.gui = dotdict(
            hull=Bar(pos=Settings.layout.gui.bar.health, prefix="Hull: ",
                  stylemap={
                      lambda val: 70.0 <= val <= 100.0 : style.gui["dp_ok"],
                      lambda val: 35.0 <= val < 70.0 : style.gui["dp_middle"],
                      lambda val: 0.0 <= val < 35.0 : style.gui["dp_critical"]
                  }),
            shield=Bar(pos=Settings.layout.gui.bar.shield, prefix="Shield: ",
                    stylemap={
                        lambda val: 70.0 <= val <= 100.0 : style.gui["sh_ok"],
                        lambda val: 35.0 <= val < 70.0 : style.gui["sh_mid"],
                        lambda val: 0.0 <= val < 35.0 : style.gui["dp_critical"]
                    }),
            weapon=Bar(pos=Settings.layout.gui.bar.weapon,
                    stylemap={
                        lambda val: 0.0 <= val <= 100.0 : style.gui["dp_ok"]
                    }),
            weapon_info=WeaponWidget(Settings.layout.gui.info.weapon,
                                  self.playership.get_weapon_info)
        )

        for gui_object in self.gui.values():
            Settings.renderer.add_object(gui_object)
        self._input_handler = InputHandler()
    def _update_gui(self):
        self.gui.hull.update(self.playership.getHullPercentage())
        self.gui.shield.update(self.playership.getShieldPercentage())
        self.gui.weapon.update(self.playership.getWeaponPercentage())
        self.gui.weapon_info.update()

    def _update_settings_from_args(self, args):
        for arg, val in args.items():
            if arg in Settings.system:
                Settings.system[arg] = val
            else:
                raise KeyError("No such parameter in settings.")

    def events(self):
        """Handle events and give command to playership."""

        key = self.screen.getch()
        command = self._input_handler.handle(key)
        if command:
            if isinstance(command, ExitGameCommand):
                self.exit()
            command.execute(self.playership)
        # if key == K_ESCAPE:
        #     deinit_curses(self.screen)
        #     sys.exit(1)
        # elif key == K_A:
        #     self.playership.move_left()
        # elif key == K_D:
        #     self.playership.move_right()
        # elif key == K_E:
        #     self.playership.next_weapon()
        # elif key == K_Q:
        #     self.playership.prev_weapon()
        # elif key == K_SPACE:
        #     self.playership.toggle_fire()
        # elif key == K_R:
        #     self.playership.take_damage(5)


    def update(self):
        """Update all object's state."""
        self.playership.update()
        self.enemy.update()
        self._update_gui()

    def render(self):
        """Render GUI and renderable objects to screen."""
        self.screen.erase()
        self.screen.border(0)
        self.screen.addstr(0, 2, "Score: {} ".format(0))
        self.screen.addstr(0, Settings.layout.field.edge.x // 2 - 4,
                           "XOInvader", curses.A_BOLD)

        Settings.renderer.render_all(self.screen)

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

    def exit(self):
        deinit_curses(self.screen)
        sys.exit(1)

def main():
    """Entry point. Create application class and go to main loop."""
    app = App()
    app.loop()

if __name__ == "__main__":
    main()
