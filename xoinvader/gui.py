""" Graphical user interface widgets."""


from typing import Callable, Optional, List, Tuple, Generator

from xo1 import Surface, Renderable

from xoinvader.style import Style
from xoinvader.utils import (
    InfiniteList,
    Point,
    Timer,
)


class TextWidget(Renderable):
    """Simple text widget.

    :param pos: widget's global position
    :param text: contained text
    :param style: curses style for text
    """

    render_priority = 1
    draw_on_border = True

    def __init__(self, pos: Point, text: str, style: int = None):

        super().__init__(pos)

        self._text = text
        self._style = style
        self._image = self._make_image()

    def _make_image(self) -> Surface:
        """Make Surface object from text and style.

        :return: Surface instance
        :rtype: `xoinvader.utils.Surface`
        """

        _style = self._style or Style().gui["normal"]
        return Surface(
            [[ch for ch in self._text]],
            [[_style for _ in range(len(self._text))]],
        )

    def update(self, dt: int, text: Optional[str] = None, style: Optional[int] = None):
        """Obtain (or not) new data and refresh image.

        :param text: new text
        :param style: new style
        """

        if text:
            self._text = text
        if style:
            self._style = style
        if text or style:
            self._image = self._make_image()


# TODO XXX FIXME: [proper-gui-hierarchy]
#                 This bloody mess bourned in hell suburbans to serve
#                 to one great target: easily enable updating by callback
#                 to update score string. It was so easy to do...
#                 Reimplement TextWidget to support callbacks too.
class TextCallbackWidget(TextWidget):
    """Simple text widget with callback.

    :param pos: widget's global position
    :param text: contained text
    :param style: curses style for text
    """

    def __init__(
        self, pos: Point, callback: Callable, style: Optional[int] = None
    ):

        self._callback = callback

        super(TextCallbackWidget, self).__init__(pos, callback(), style)

    def update(self, dt):
        self._text = self._callback()
        self._image = self._make_image()


class MenuItemWidget(TextWidget):
    """Selectable menu item widget.

    :param pos: widget's global position
    :type pos: `xoinvader.utils.Point`

    :param text: contained text
    :type text: string

    :param template: left and right markers
    :type template: tuple of two strings

    .. note:: add [ [style] ... ] support

    :param style: curses style for text
    :type style: integer(curses style)
    """

    render_priority = 1

    def __init__(
        self,
        pos: Point,
        text: str,
        action: Optional[Callable] = None,
        template: Tuple[str, str] = ("* ", " *"),
        style=None,
        align_left=True,
    ):
        self._action = action
        self._left = template[0]
        self._right = template[1]
        self._selected = False
        self._align_left = align_left

        super(MenuItemWidget, self).__init__(pos, text, style)

    def _make_image(self) -> Surface:
        """Make Surface object from text, markers and style.

        :return: Surface instance
        :rtype: `xoinvader.utils.Surface`
        """

        _style = self._style or Style().gui["yellow"]
        if self._selected:
            _full_text = "".join([self._left, self._text, self._right])
        else:
            if self._align_left:
                _full_text = "".join([" " * len(self._left), self._text])
            else:
                _full_text = self._text

        return Surface(
            [[ch for ch in _full_text]],
            [[_style for _ in range(len(_full_text))]],
        )

    def toggle_select(self):
        """Draw or not selector characters."""
        self._selected = not self._selected
        self._image = self._make_image()

    def select(self):
        """Select and refresh image."""

        self._selected = True
        self._image = self._make_image()

    def deselect(self):
        """Deselect and refresh image."""

        self._selected = False
        self._image = self._make_image()

    @property
    def selected(self) -> bool:
        """Shows is item selected or not.

        .. warning:: Complete menu workflow.
        """

        return self._selected

    def do_action(self):
        """Call action callback."""

        if callable(self._action):
            self._action()


class MenuItemContainer(Renderable):  # (CompoundMixin)
    """Container for menu items, manages current selected, dispatches action."""

    compound = True

    def __init__(self, items: Optional[List[MenuItemWidget]] = None):

        # This object is containter, it doesn't matter where it placed
        # (while we have no local coordinates of childs implemented).
        super().__init__(Point())
        self._image = None

        self._items = InfiniteList(items) if items else InfiniteList()

    def add(self, item: MenuItemWidget):
        self._items.append(item)

    # TODO: add ability to update infinity list index after changing?
    def remove(self, item: MenuItemWidget):
        self._items.remove(item)

    def select(self, index: int) -> MenuItemWidget:
        """Select desired element by index, returns this element."""

        self._items.current().deselect()
        selected = self._items.select(index)
        selected.select()
        return selected

    def do_action(self):
        self._items.current().do_action()

    def prev(self):
        self._items.current().deselect()
        item = self._items.prev()
        item.select()
        return item

    def next(self):
        self._items.current().deselect()
        item = self._items.next()
        item.select()
        return item

    def current(self):
        return self._items.current()

    def update(self, dt):
        pass

    def get_renderable_objects(self):
        return list(self._items)


# pylint: disable=too-many-arguments
class PopUpNotificationWidget(TextWidget):
    """Widget that allows to show short messages with timeout.

    .. warning:: Experimental stuff. Fix constructor 6/5.

    :param pos: global position
    :type pos: :class:`xoinvader.utils.Point`

    :param text: text for display
    :type text: string

    :param style: curses style
    :type style: int | [int]

    :param timeout: timer timeout
    :type timeout: float

    :param callback: callback for removal object
    :type callback: function
    """

    def __init__(self, pos, text, style=None, timeout=1.0, callback=None):
        super(PopUpNotificationWidget, self).__init__(pos, text, style)

        self._callback = callback
        self._timer = Timer(timeout, self._finalize_cb)
        self._update_text = super(PopUpNotificationWidget, self).update
        self._timer.start()

    def _finalize_cb(self):
        """Finalize callback, e.g. pass to it self for removal."""

        if self._callback:
            self._callback(self)

    def update(self, dt: int, text: Optional[str] = None, style: Optional[int] = None):
        self._update_text(text, style)
        self._timer.update(dt)


class WeaponWidget(Renderable):
    """Widget for displaying weapon information.

    .. warning:: !!! Duplicates TextWidget !!!

    :param pos: global position
    :type pos: :class:`xoinvader.utils.Point`

    :param get_data: callback for getting data
    :type get_data: function
    """

    render_priority = 1
    draw_on_border = True

    def __init__(self, pos, get_data):
        self._pos = pos
        self._get_data = get_data
        self._data = self._get_data()
        self._image = self._make_image()

    def _make_image(self):
        """Return Surface object."""

        return Surface(
            [[ch for ch in self._data]],
            [[Style().gui["yellow"] for _ in range(len(self._data))]],
        )

    def update(self, dt):
        """Obtain new data and refresh image."""

        self._data = self._get_data()
        self._image = self._make_image()


# pylint: disable=too-many-instance-attributes
class Bar(Renderable):
    """Progress bar widget.

    :param pos: Bar's global position

    :param str prefix: text before the bar
    :param str postfix: text after the bar
    :param str left: left edge of the bar
    :param str right: right edge of the bar
    :param str marker: symbol that fills the bar
    :param int marker_style: curses style for marker (passes to render)
    :param str empty: symbols that fills empty bar space (without marker)
    :param int  empty_style: curses style for empty marker (passes to render)
    :param int count: number of markers in the bar
    :param int maxval: max value of displayed parameter (affects the accuracy)
    :param int general_style: style of other characters(prefix, postfix, etc)

    :param stylemap: mapping of compare functions and integers to curses style
    :type stylemap: dict(function, integer(curses style)

    :param function callback: calls if not None to get new percentage value
    """

    render_priority = 1
    draw_on_border = True

    def __init__(
        self,
        pos: Point,
        prefix: str = "",
        postfix: str = "",
        left: str = "[",
        right: str = "]",
        marker: str = "█",
        marker_style: Optional[int] = None,
        empty: str = "-",
        empty_style: Optional[int] = None,
        count: int = 10,
        maxval: int = 100,
        general_style: Optional[int] = None,
        stylemap=None,
        callback=None,
    ):

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
        self._callback = callback

        # fmt: off
        self._template = "".join([
            str(val) for val in [
                self._prefix,
                self._left, "{blocks}", self._right,
                self._postfix
            ]
        ])
        # fmt: on

        self._current_count = self._count
        self._image = None
        self._update_image()

    def _update_current_count(self, val):
        """Normalize current percentage and update count of marker blocks.

        :param int val: value to normalize
        """
        self._current_count = int(round(val * self._count / self._maxval))

    def _style(self, val):
        """Return style in depend on percentage."""

        for cmp_func, bar_style in self._stylemap.items():
            if cmp_func(val):
                return bar_style
        return None

    def _update_image(self):
        """Update image in depend on percentage."""

        left = self._marker * self._current_count
        right = self._empty * (self._count - self._current_count)
        bar = self._template.format(blocks=left + right)
        image = []
        for char in bar:
            if char == self._marker:
                image.append((char, self._marker_style))
            else:
                image.append((char, self._general_style))
        self._image = Surface(
            [[ch[0] for ch in image]], [[st[1] for st in image]]
        )

    def update(self, dt: int, val=None):
        """Update bar if there's need for it."""

        if self._callback:
            val = self._callback()

        if val is None:
            raise ValueError("val = None, what to do?")

        self._marker_style = self._style(val)
        self._update_current_count(val)
        self._update_image()
