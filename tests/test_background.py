"""Test xoinvader.background module."""

import os
from copy import copy

import pytest

from xoinvader.background import Background, Chunk, load_chunks
from xoinvader.common import Settings

from .common import PREFIX


CHUNK_NO_NAME = os.path.join(PREFIX, "chunk_no_name.bg")
"""Background file contains unnamed chunk."""

CHUNK_DUPLICATE_NAMES = os.path.join(PREFIX, "chunk_duplicate_names.bg")
"""Background file contains duplicated chunk names."""

CHUNK_NO_CHUNKS = os.path.join(PREFIX, "no_chunks.bg")
"""Background file doesn't contain chunks at all."""

CHUNK_NORMAL = os.path.join(PREFIX, "chunk_normal.bg")
"""Absolutely valid background file."""


# pylint: disable=invalid-name,protected-access,missing-docstring
def test_chunk() -> None:
    c = Chunk("test")
    assert not c.lines
    assert len(c) == 0  # pylint: disable=len-as-condition
    assert c.name == "test"

    c.add_line("wut")
    assert c.lines[0] == "wut"
    assert len(c) == 1

    c[0] = "ugh"
    assert c[0] == "ugh"


def test_load_chunks() -> None:
    with pytest.raises(ValueError):
        load_chunks(CHUNK_NO_NAME)

    with pytest.raises(ValueError):
        load_chunks(CHUNK_DUPLICATE_NAMES)

    with pytest.raises(ValueError):
        load_chunks(CHUNK_NO_CHUNKS)

    c = load_chunks(CHUNK_NORMAL)
    assert len(c) == 3
    assert c[0][0] == "qweqwe"
    assert len(c[0]) == 1

    d = load_chunks(CHUNK_NORMAL, 3)
    assert d[0][0] == "qwe"


# pylint: disable=too-many-statements
def test_background() -> None:
    Settings.layout.field.edge.x = 3
    Settings.layout.field.edge.y = 2

    b = Background()
    assert not b.loop
    assert not b.loop_all
    assert not b.speed
    assert not b.chunks
    assert not b.background
    assert not b._current_chunk
    assert not b._current_chunk_num
    assert not b._chunk_line

    b.background = ["qwe", "asd"]
    assert b.background == ["qwe", "asd"]

    b.chunks = "test"
    assert b.chunks == "test"

    assert b._advance_chunk(1) == "   "

    b = Background(CHUNK_NORMAL)
    assert len(b.chunks) == 3
    assert len(b.chunks[2]) == 3

    b.start()
    assert b._current_chunk is b.chunks[0]
    assert b.background == [
        "   ",
        "   ",
    ]

    b.start(True)
    assert b._chunk_line == 1
    assert b._current_chunk is b.chunks[1]
    assert b.background == [
        "qwe",
        "asd",
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

    assert not b.update(13)
    b.speed = 40
    bg = copy(b.background)
    b.update(13)
    assert bg == b.background
    b.update(13)
    assert bg != b.background

    b.speed = -40
    bg = copy(b.background)
    b.update(13)
    assert bg == b.background
    b.update(13)
    assert bg != b.background
