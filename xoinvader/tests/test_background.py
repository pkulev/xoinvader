import pytest

from xoinvader.background import Chunk, load_chunks

PREFIX = "xoinvader/tests/fixtures/"

def test_chunk():
    c = Chunk("test")
    assert not c.lines
    assert not c.length
    assert c.name == "test"

    c.add_line("wut")
    assert c.lines[0] == "wut"
    assert c.length == 1

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
    assert c[0].length == 1

    d = load_chunks(PREFIX + "chunk_normal.bg", 3)
    assert d[0][0] == "qwe"
