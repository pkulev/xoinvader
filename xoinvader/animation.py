"""Animation.

Animation is set of keyframes.
Value of selected attribute changes in time.

Keyframe:
  (time, value)

Objects have animation manager which manages animation graph and switching."""


from operator import itemgetter

from xoinvader.utils import Timer


# TODO: Implement animation graph and etc
class AnimationManager(object):
    """Manage list of object animation."""

    def __init__(self):
        self._animations = {}
        self._animation = None

    @property
    def animation(self):
        """AnimationManager's current animation name.

        To set animation - assign it's name.

        :getter: yes
        :setter: yes
        :type: str
        """

        if self._animation:
            return self._animation.name
        else:
            raise AttributeError("There is no available animation.")

    @animation.setter
    def animation(self, name):
        if name in self._animations:
            self._animation = self._animations[name]
        else:
            raise ValueError("No such animation: '{0}'.".format(name))

    def add(self, name, bind, attr, keyframes, loop=False):
        """Add new animation, pass args to Animation class.

        :param str name: animation name
        :param object bind: object to bind animation
        :param str attr: attribute to change in frames
        :param list keyframes: (float, object) tuples
        :param bool loop: loop animation or not
        """

        animation = Animation(name, bind, attr, keyframes, loop)
        self._animations[name] = animation

        if not self._animation:
            self._animation = animation

    def update(self):
        """Update manager's state."""

        if not self._animation:
            return

        try:
            self._animation.update()
        except StopIteration:
            return  # TODO: think about method to change animation


class Animation(object):
    """Animation unit.

    :param str name: animation name
    :param object bind: object to bind animation
    :param str attr: attribute to change in frames
    :param list keyframes: (float, object) tuples
    :param bool loop: loop animation or not
    """

    def __init__(self, name, bind, attr, keyframes, loop=False):
        self._name = name
        self._obj = bind
        self._attr = attr

        if not keyframes:
            raise ValueError("Animation keyframes must not be empty.")
        self._keyframes = sorted(keyframes, key=itemgetter(0))

        self._loop = loop

        # Timer for tracking local time
        self._timer = Timer(self._keyframes[-1][0], lambda: True)
        self._timer.start()

        # Current keyframe index
        self._current = 0

    @property
    def name(self):
        """Animation's name.

        :getter: yes
        :setter: no
        :type: str
        """
        return self._name

    def update(self):
        """Update animation state.

        Animation object holds sorted list of (time, value) items and changes
        selected attribute of binded object according to local animation time.
        Time measured by timer. When current time is greater or equal then time
        of next keyframe - animation object changes it to appropriate value.
        When animation is done and if not looped - raise StopIteration.
        """

        # TODO: feature-animation: approximation
        if len(self._keyframes) == self._current:
            if self._loop:
                self._current = 0
                self._timer.restart()
            else:
                self._timer.stop()
                raise StopIteration

        self._timer.update()

        keyframe = self._keyframes[self._current]
        if self._timer.get_elapsed() >= keyframe[0]:
            setattr(self._obj, self._attr, keyframe[1])
            self._current += 1
