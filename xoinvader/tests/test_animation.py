import time

import pytest

from xoinvader.animation import Animation, AnimationManager


class GameObject(object):
    """Game object mock."""

    def __init__(self):
        self.attr = 0


@pytest.mark.slow
def test_animation():

    with pytest.raises(ValueError):
        Animation("dummy", bind=None, attr=None, keyframes=[])

    obj = GameObject()
    keyframes = [
        (0.0, 1),
        (0.5, 2),
        (2.0, 10),
    ]
    anim = Animation(name="test", bind=obj, attr="attr", keyframes=keyframes)

    obj.anim = anim
    assert anim.name == "test"

    anim.update()
    assert obj.attr == 1
    time.sleep(1)

    # Frame must be unchanged
    for _ in range(10):
        anim.update()

    assert obj.attr == 2
    time.sleep(1)
    anim.update()  # here time is > 2
    assert obj.attr == 10
    with pytest.raises(StopIteration):
        anim.update()  # It's time to switch animation


@pytest.mark.slow
def test_animation_loop():
    obj = GameObject()
    animgr = AnimationManager()
    animgr.add("test", obj, "attr", keyframes=[(0.0, 0), (1.0, 1)], loop=True)

    animgr.update()
    assert obj.attr == 0
    time.sleep(1)
    animgr.update()
    assert obj.attr == 1
    time.sleep(1)
    animgr.update()
    assert obj.attr == 0
    animgr.update()
    assert obj.attr == 0
    time.sleep(1)
    animgr.update()
    assert obj.attr == 1


@pytest.mark.slow
def test_animation_manager():
    obj = GameObject()
    animgr = AnimationManager()

    with pytest.raises(AttributeError):
        animgr.animation

    animgr.add("test1", bind=obj, attr="attr", keyframes=[(0.0, 1)])
    animgr.add("test2", bind=obj, attr="attr", keyframes=[(0.0, 2)])

    assert animgr.animation == "test1"

    with pytest.raises(ValueError):
        animgr.animation = "bad-animation"

    animgr.animation = "test2"
    assert animgr.animation == "test2"
    animgr.animation = "test1"

    animgr.update()
    time.sleep(1)

    assert animgr.update() is None
