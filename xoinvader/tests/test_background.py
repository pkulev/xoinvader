import pytest
from copy import copy

from xoinvader.background import Background, Chunk, load_chunks
from xoinvader.common import Settings
from xoinvader.utils import Point


PREFIX = "xoinvader/tests/fixtures/"


def test_chunk():
    c = Chunk("test")
    assert not c.lines
    assert len(c) == 0
    assert c.name == "test"

    c.add_line("wut")
    assert c.lines[0] == "wut"
    assert len(c) == 1

    c[0] = "ugh"
    assert c[0] == "ugh"


def test_load_chunks():
    with pytest.raises(ValueError):
        load_chunks(PREFIX + "chunk_no_name.bg")

    with pytest.raises(ValueError):
        load_chunks(PREFIX + "chunk_duplicate_names.bg")

    with pytest.raises(ValueError):
        load_chunks(PREFIX + "no_chunks.bg")

    c = load_chunks(PREFIX + "chunk_normal.bg")
    assert len(c) == 3
    assert c[0][0] == "qweqwe"
    assert len(c[0]) == 1

    d = load_chunks(PREFIX + "chunk_normal.bg", 3)
    assert d[0][0] == "qwe"


def test_background():
    Settings.layout.field.edge.x = 3
    Settings.layout.field.edge.y = 2

    b = Background()
    assert not b.loop
    assert not b.loop_all
    assert not b.speed
    assert not b.chunks
    assert not b.background
    assert not b._background_surface
    assert not b._current_chunk
    assert not b._current_chunk_num
    assert not b._chunk_line
    assert not b._ticks_since_last_update

    b.background = ["qwe", "asd"]
    assert b.background == ["qwe", "asd"]

    b.chunks = "test"
    assert b.chunks == "test"

    assert b._advance_chunk(1) == "   "

    b = Background(PREFIX + "chunk_normal.bg")
    assert len(b.chunks) == 3
    assert len(b.chunks[2]) == 3

    b.start()
    assert b._current_chunk is b.chunks[0]
    assert b.background == [
        "   ",
        "   "
    ]

    b.start(True)
    assert b._chunk_line == 1
    assert b._current_chunk is b.chunks[1]
    assert b.background == [
        "qwe",
        "asd"
    ]

    assert b._chunk_line == 1
    assert b._advance_chunk(1) == "zxc"
    assert b._chunk_line == 1
    assert b._advance_chunk(-1) == "123"
    assert b._chunk_line == 0
    assert b._advance_chunk(1) == "zxc"
    assert b._chunk_line == 1
    b.loop = True
    assert b._advance_chunk(1) == "123"
    assert b._advance_chunk(1) == "!@#"
    assert b._advance_chunk(-1) == "zxc"
    assert b._advance_chunk(-1) == "!@#"
    b.loop = False
    b.loop_all = True
    assert b._advance_chunk(1) == "123"
    assert b._advance_chunk(1) == "!@#"
    assert b._advance_chunk(1) == "qwe"
    assert b._advance_chunk(1) == "asd"
    assert b._advance_chunk(1) == "zxc"
    assert b._advance_chunk(-1) == "123"
    assert b._advance_chunk(-1) == "zxc"
    assert b._advance_chunk(-1) == "asd"
    assert b._advance_chunk(-1) == "qwe"
    assert b._advance_chunk(-1) == "!@#"
    b.loop_all = False
    assert b._advance_chunk(1) == "123"
    assert b._advance_chunk(1) == "!@#"
    assert b._advance_chunk(1) == "   "

    pos, gen = b.get_render_data()
    assert pos == [Point(0, 0)]
    assert next(gen) == (Point(0, 0, 0), "q", None)
    assert next(gen) == (Point(1, 0, 0), "w", None)
    assert next(gen) == (Point(2, 0, 0), "e", None)
    assert next(gen) == (Point(0, 1, 0), "a", None)
    assert next(gen) == (Point(1, 1, 0), "s", None)
    assert next(gen) == (Point(2, 1, 0), "d", None)
    with pytest.raises(StopIteration):
        next(gen)

    assert not b.update()
    b.speed = 40
    bg = copy(b.background)
    b.update()
    assert bg == b.background
    b.update()
    assert not bg == b.background

    b.speed = -40
    bg = copy(b.background)
    b.update()
    assert bg == b.background
    b.update()
    assert not bg == b.background
