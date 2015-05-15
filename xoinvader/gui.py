""" Graphical user interface widgets."""

from xoinvader.render import Renderable
from xoinvader.utils import Surface
from xoinvader.curses_utils import style


class WeaponWidget(Renderable):
    """Widget for displaying weapon information."""

    def __init__(self, pos, get_data):
        self._pos = pos
        self._get_data = get_data
        self._data = self._get_data()
        self._image = self._make_image()

    def _make_image(self):
        """Return Surface object."""
        return Surface([[ch for ch in self._data]],
                       [[style.gui["yellow"] for _ in range(len(self._data))]])

    def update(self):
        """Obtain new data and refresh image."""
        self._data = self._get_data()
        self._image = self._make_image()

    def get_render_data(self):
        return [self._pos], self._image.get_image()


class Bar(Renderable):
    """
    Progress bar widget.

    General:

    :pos - position of the bar (global coordinates);

    Bar specific:

    :prefix - text before the bar;
    :postfix - text after the bar;
    :left - left edge of the bar;
    :right - right edge of the bar;
    :marker - symbol that fills the bar;
    :marker_style - curses style for marker (passes to render);
    :empty - symbols that fills empty bar space (without marker);
    :empty_style - curses style for empty marker (passes to render);
    :count - number of markers in the bar;
    :maxval - max value of displayed parameter (affects the accuracy);
    :general_style - style of other characters(prefix, postfix, etc);
    :stylemap - mapping of compare functions and integers to curses style.
    """

    def __init__(self, pos,
                 prefix="", postfix="",
                 left="[", right="]",
                 marker="█", marker_style=None,
                 empty="-", empty_style=None,
                 count=10, maxval=100,
                 general_style=None,
                 stylemap=None):

        self._pos = pos
        self._prefix = prefix
        self._postfix = postfix
        self._left = left
        self._right = right
        self._marker = marker
        self._marker_style = marker_style
        self._empty = empty
        self._empty_style = empty_style
        self._count = count
        self._maxval = maxval
        self._general_style = general_style
        self._stylemap = stylemap

        self._template = "".join([str(val) for val in
                                  [self._prefix, self._left, "{blocks}",
                                   self._right, self._postfix]])

        self._current_count = self._count
        self._image = None
        self._update_image()

    def _update_current_count(self, val):
        """Normalize current percentage and update count of marker blocks."""
        self._current_count = int(round(val * self._count / self._maxval))

    def _style(self, val):
        """Return style in depend on percentage."""
        for cmp_func, bar_style in self._stylemap.items():
            if cmp_func(val):
                return bar_style
        return None

    def _update_image(self):
        """Update image in depend on persentage."""
        left = self._marker * self._current_count
        right = self._empty * (self._count - self._current_count)
        bar = self._template.format(blocks=left + right)
        image = []
        for char in bar:
            if char == self._marker:
                image.append((char, self._marker_style))
            else:
                image.append((char, self._general_style))
        self._image = Surface([[ch[0] for ch in image]],
                              [[st[1] for st in image]])

    def update(self, val):
        """Update bar."""
        self._marker_style = self._style(val)
        self._update_current_count(val)
        self._update_image()

    def get_render_data(self):
        """Return render specific data."""
        return [self._pos], self._image.get_image()
