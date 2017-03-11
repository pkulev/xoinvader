"""Level background."""

from xoinvader.common import Settings
from xoinvader.render import Renderable
from xoinvader.utils import Point, Surface


CHUNK_MAGIC = "~chunk~"
"""Background file format chunk marker."""


class Chunk(object):
    """Class for storing background chunks.

    :param str name: name of the chunk
    :param list lines: list of all chunk lines
    """

    def __init__(self, name):
        self._name = name
        self._lines = []

    @property
    def name(self):
        """Chunk name.

        :getter: yes
        :setter: no
        :type: str
        """
        return self._name

    @property
    def lines(self):
        """All chunk lines.

        :getter: yes
        :setter: no
        :type: list
        """
        return self._lines

    def add_line(self, line):
        """Add line to `lines` list of the chunk.

        :param str line: line to add
        """
        self._lines.append(line)

    def __getitem__(self, index):
        return self._lines[index]

    def __setitem__(self, index, item):
        self._lines[index] = item

    def __len__(self):
        return len(self._lines)


def load_chunks(filename, trim_width=None):
    """Load chunks from file.

    File format:
    ```
    -~chunk~- <chunk_name>
    <data>
    ...
    ```

    `~chunk~` is magic string, and chunk spans until next magic line, or
    until end of file.

    Completely blank lines are ignored.
    If `trim_width` is provided, all lines are truncated to this length.

    :param str filename: path to file to load chunks from
    :param int trim_width: width to truncate long lines to
    :return: list of loaded chunks
    :rtype: list
    """

    chunks = []
    current_chunk = None
    names = []
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            elif line.startswith(CHUNK_MAGIC):
                name_split = line.split()
                if len(name_split) < 2:
                    raise ValueError("Chunks with empty names are not allowed")
                name = name_split[1].strip()
                if name in names:
                    raise ValueError("Name {0} already defined in background "
                                     "file {1}".format(name, filename))
                current_chunk = Chunk(name)
                chunks.append(current_chunk)
                names.append(name)
                continue
            elif current_chunk is None:
                continue
            # ok, now we got both chunk and something to store in it
            line_add = line[:trim_width] if trim_width else line
            current_chunk.add_line(line_add)
    if not chunks:
        raise ValueError("File {0} does not contain "
                         "any chunks".format(filename))
    return chunks


# pylint: disable=too-many-instance-attributes
class Background(Renderable):
    """Class for storing and managing level background.

    Manages background rendering and changing in time.

    :param bool loop: flag if current chunk should loop after it had ended
    :param bool loop_all: flag if whole background should repeat from beginning
    :param float speed: speed of background advance. Can be negative to
    represent moving backwards
    :param list chunks: list of background chunks
    :param list background: list of background lines. You may change it at any
    time. This list directly converts into Surface which then goes to the
    renderer
    """

    render_priority = -1000  # TODO: render-priority

    def __init__(self, filename=None, speed=0, loop=False, loop_all=False):
        self._speed = speed
        self._loop = loop
        self._loop_all = loop_all
        self._chunks = []
        self._background = []

        # pylint: disable=invalid-name
        self._w = Settings.layout.field.edge.x
        self._h = Settings.layout.field.edge.y
        self._background_surface = None
        self._current_chunk = None
        self._current_chunk_num = 0  # position of chunk in chunk list
        self._chunk_line = 0  # position in current chunk
        self._ticks_since_last_update = 0

        if filename:
            self.load_file(filename)

    @property
    def loop(self):
        """Loop current chunk.

        :getter: yes
        :setter: yes
        :type: bool
        """
        return self._loop

    @loop.setter
    def loop(self, value):
        """Setter."""
        self._loop = value

    @property
    def loop_all(self):
        """Loop all chunks.

        :getter: yes
        :setter: yes
        :type: bool
        """
        return self._loop_all

    @loop_all.setter
    def loop_all(self, value):
        """Setter."""
        self._loop_all = value

    @property
    def speed(self):
        """Speed of background advance.

        :getter: yes
        :setter: yes
        :type: int
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        """Setter."""
        self._speed = value

    @property
    def chunks(self):
        """Background chunks.

        :getter: yes
        :setter: yes
        :type: list
        """
        return self._chunks

    @chunks.setter
    def chunks(self, value):
        """Setter."""
        self._chunks = value

    @property
    def background(self):
        """Background lines.

        :getter: yes
        :setter: yes
        :type: list
        """
        return self._background

    @background.setter
    def background(self, value):
        """Setter."""
        self._background = value

    def clear(self):
        """Clear all background.

        Doesn't prevent subsequent updating, if speed is not 0.
        """

        self._background = [" " * self._w] * self._h

    def load_file(self, filename):
        """Load background from file.

        Calls `load_chunks` function int trim mode, and stores return value in
        the `chunks` field.

        :param str filename:
        """

        self._chunks = load_chunks(filename, self._w)

    def _fill(self):
        """Fills the whole background.

        Takes first chunk and fills background with it's contents. If there's
        not enough lines, switches to next chunk, etc. I.e, we just advance
        background momentary, and update all pointers accordingly.
        """

        self._background = []
        for _ in range(self._h):
            self._background.append(self._advance_chunk(1))

    def start(self, filled=False):
        """Start background from the beginning.

        If `filled` parameter is provided, fills the background starting with
        first chunk, using `_fill` method.

        :param bool filled: if true, perform initial background fill
        """

        self._ticks_since_last_update = 0
        self._current_chunk_num = 0
        self._current_chunk = self._chunks[0]
        self._chunk_line = 0
        if filled:
            self._fill()
        else:
            self.clear()
        self.update_surface()

    def _advance_chunk(self, advance):
        """Return current chunk line and update pointers.

        Performs checks if current chunk number and current line position are
        valid, updates them, if they're not, returns current line and then
        updates current line position. I.e., performs boundary checks, updates
        if necessary and then updates current line position.

        :return: current line in chunk sequence
        :rtype: string
        """

        if not self._current_chunk:
            return " " * self._w

        # start checks
        if (self._chunk_line < len(self._current_chunk) and
                self._chunk_line >= 0):
            line = self._current_chunk[self._chunk_line]
            self._chunk_line += advance
            return line

        # chunk ended! now we decide what to do
        if self._loop:
            if self._chunk_line < 0:
                self._chunk_line = len(self._current_chunk) - 1
            else:
                self._chunk_line = 0
            line = self._current_chunk[self._chunk_line]
            self._chunk_line += advance
            return line

        # next chunk or stop advancing
        self._current_chunk_num += advance
        if (self._current_chunk_num < len(self._chunks) and
                self._current_chunk_num >= 0):
            # okay, just set new chunk
            self._current_chunk = self._chunks[self._current_chunk_num]
            self._chunk_line = 0
            line = self._current_chunk[self._chunk_line]
            self._chunk_line += advance
            return line

        if self._loop_all:
            if self._current_chunk_num < 0:
                self._current_chunk_num = len(self._chunks) - 1
                self._current_chunk = self._chunks[-1]
                self._chunk_line = len(self._current_chunk) - 1
            else:
                self._current_chunk_num = 0
                self._current_chunk = self._chunks[0]
                self._chunk_line = 0
            line = self._current_chunk[self._chunk_line]
            self._chunk_line += advance
            return line

        # looks like we don't have any more chunks, and we're not looping
        # thus return void line
        self._current_chunk = None
        return " " * self._w

    def get_render_data(self):
        return [Point(0, 0)], self._background_surface.get_image()

    def update_surface(self):
        """Regenerate background surface.

        Intended to be call after all update operations on the `background`
        member list so updated info will immediately come into effect.
        """

        self._background_surface = Surface(self._background)

    def update(self):
        """Update background.

        Checks if time to update has come, and calls `_advance_chunk` method
        with appropriate parameter. Calls `update_surface` at the end.

        """

        if self._speed == 0:
            return

        self._ticks_since_last_update += abs(self._speed)
        if self._ticks_since_last_update < 60:  # TODO FIXME: hardcode wololo
            return

        self._ticks_since_last_update = 0

        advance = 1 if self._speed > 0 else -1
        new_line = self._advance_chunk(advance)
        if advance > 0:
            self._background.pop()
            self._background.insert(0, new_line)
        else:
            self._background.pop(0)
            self._background.append(new_line)
        self.update_surface()
