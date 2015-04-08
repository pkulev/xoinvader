""" This is module docstring """

from .render import Renderable
from .utils import Surface, style


class WeaponWidget(Renderable):
    """this is class docstring stub """
    def __init__(self, pos, get_data):
        """This is init docstring """

        self._pos = pos
        self._get_data = get_data
        self._data = self._get_data()
        self._image = self._make_image()

    def _make_image(self):
        return Surface([[ch for ch in self._data]],
                       [[style.gui["yellow"] for _ in range(len(self._data))]])


    def update(self):
        self._data = self._get_data()
        self._image = self._make_image()

    def get_render_data(self):
        return [self._pos], self._image.get_image()


class _Bar(Renderable):
    def __init__(self, pos,
                 prefix="", postfix="",
                 left="[", right="]",
                 marker=" ", marker_style=None,
                 count=10, maxval=100,
                 template=None, data=None):
        
        self._prefix = prefix
        self._postfix = postfix
        self._left = left
        self._right = right
        self._marker = marker
        self._marker_style = marker_style
        self._count = count
        self._maxval = maxval
        if template:
            self._template = template
        else:
            self._template = "".join([
                self.prefix, self.left, "{blocks}",
                self.right, self.postfix
            ])

    def update(self, val):
        pass

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
                             "blank": style.gui["dp_blank"]}


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

        style_map = []
        elem = 0
        in_bar = False
        for char in self._bar:
            if char == "[":
                style_map.append((char, gui_style))
                in_bar = True
            elif char == " " and in_bar:
                if elem < num:
                    style_map.append((char, elem_style))
                else:
                    style_map.append((char, blank_style))
                elem += 1
            elif char == "]":
                in_bar = False
                style_map.append((char, gui_style))
            else:
                style_map.append((char, gui_style))

        return style_map


    def update(self):
        self._value = self._get_data()[0]
        if self._update_all:
            self._max_value = self._get_data()[1]
        stylemap = self._generate_style_map()
        self._image = Surface([[ch[0] for ch in stylemap]], [[st[1] for st in stylemap]])


    def get_render_data(self):
        return [self._pos], self._image.get_image()
