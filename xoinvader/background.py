"""Level background."""


CHUNK_MAGIC = "~chunk~"
"""Background file format chunk marker."""


class Chunk(object):
    """Class for storing background chunks.

    :param str name: name of the chunk
    :param list lines: list of all chunk lines
    :param int length: length of lines list (for convenience)

    """

    def __init__(self, name):
        self._name = name
        self._lines = []
        self._length = 0

    @property
    def name(self):
        return self._name

    @property
    def lines(self):
        return self._lines

    @property
    def length(self):
        return self._length

    def add_line(self, line):
        """Add line to `lines` list of the chunk. Increases `length` by 1.

        :param str line: line to add
        """
        self._lines.append(line)
        self._length += 1

    def __getitem__(self, index):
        return self._lines[index]

    def __setitem__(self, index, item):
        self._lines[index] = item


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
            elif not current_chunk:
                continue
            # ok, now we got both chunk and something to store in it
            line_add = line[:trim_width] if trim_width else line
            current_chunk.add_line(line_add)
        if not chunks:
            raise ValueError("File {0} does not contain "
                             "any chunks".format(filename))
        return chunks
