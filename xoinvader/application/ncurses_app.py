"""NCurses application class."""

from operator import attrgetter

from eaf.app import Application
from eaf.render import Renderer

import xoinvader.curses_utils

from xoinvader.common import Settings
from xoinvader.utils import Point


INVISIBLE_SYMBOLS = " "
"""Symbols that renderer must not render on the screen."""


class CursesRenderer(Renderer):
    """Curses renderer."""

    def __init__(self, screen):
        super().__init__(screen)

    def clear(self):
        self.screen.erase()
        self.screen.border(0)

    def render_objects(self, objects):
        """Render all renderable objects."""

        border = Point(*self.screen.getmaxyx()[::-1])
    
        # TODO: Move sorting to some kind of object manager
        # Must be sorted on adding objects
        for obj in sorted(objects, key=attrgetter("render_priority")):
            gpos_list, data_gen = obj.get_render_data()
    
            for data in data_gen:
                for gpos in gpos_list:
                    lpos, image, style = data
                    cpos = (gpos + lpos)[int]
    
                    if (
                        (cpos.x >= border.x - 1 or cpos.y >= border.y - 1) or
                        (cpos.x <= 0 or cpos.y <= 0)
                    ) and not obj.draw_on_border:
                        obj.remove_obsolete(gpos)
                        continue
    
                    if image in INVISIBLE_SYMBOLS:
                        continue
    
                    if style:
                        self.screen.addstr(
                            cpos.y, cpos.x,
                            image, style)
                    else:
                        self.screen.addstr(cpos.y, cpos.x, image)

    def present(self):
        self.screen.refresh()

    def get_width(self):
        return self.screen.getmaxyx()[0]

    def get_height(self):
        return self.screen.getmaxyx()[1]


class CursesApplication(Application):
    """Curses-powered application class."""

    def __init__(self):
        window = xoinvader.curses_utils.create_window(
            ncols=Settings.layout.field.border.x,
            nlines=Settings.layout.field.border.y)
        renderer = CursesRenderer(window)

        super().__init__(renderer, window)

        self._clock = xoinvader.curses_utils.get_clock()

    def set_caption(self, caption: str, icontitle: str = ""):
        """Set window caption.

        :param caption: window caption
        :param icontitle: short title
        """

        # FIXME: Maybe we can update text via terminal API
        pass

    def stop(self):
        self._ioloop.add_callback(
            lambda: xoinvader.curses_utils.deinit_curses(self.renderer.screen))
        super().stop()
