"""Animation.

Animation is set of keyframes.
Value of selected attribute changes in time.

Keyframe:
  (time, value)

Objects have animation manager which manages animation graph and switching."""

from __future__ import division

from operator import itemgetter

from xoinvader.utils import Point, Timer


class AnimationBoundariesExceeded(Exception):
    """Exception to show that interpolated value will be incorrect."""

    def __init__(self, first, current_time, second):
        super(AnimationBoundariesExceeded, self).__init__(
            self,
            "Animation frame boundaries exceeded: {0} <= {1} <= {2}".format(
                first, current_time, second))


class InterpolationUnknownTypes(Exception):
    """Such type combination is unsupported."""

    def __init__(self, first, second):
        super(InterpolationUnknownTypes, self).__init__(
            self, "Unknown types of interpolating values: {0} and {1}".format(
                first, second))


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

    def add(self, name, *args, **kwargs):
        """Add new animation, pass args to Animation class.

        See interface of `class::xoinvader.animation.Animation`.

        :param str name: animation name
        """

        animation = Animation(name, *args, **kwargs)
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


# pylint: disable=too-many-instance-attributes,too-many-arguments
# pylint: disable=too-few-public-methods
class Animation(object):
    """Animation unit.

    Animation object holds sorted list of (time, value) items and changes
    selected attribute of bound object according to local animation time.
    Time measured by timer. When current time is greater or equal then time
    of next keyframe - animation object changes it to appropriate value.
    When animation is done and if not looped - raise StopIteration.
    In case of interpolated animation value calculation occurs within two
    bounding frames and on frame switch.

    :param str name: animation name
    :param object bind: object to bind animation
    :param str attr: attribute to change in frames
    :param list keyframes: (float, object) tuples
    :param bool interp: interpolate values between frames or not
    :param bool loop: loop animation or not
    """

    def __init__(self, name, bind, attr, keyframes, interp=False, loop=False):
        self._name = name
        self._obj = bind
        self._attr = attr

        if not keyframes:
            raise ValueError("Animation keyframes must not be empty.")
        self._keyframes = sorted(keyframes, key=itemgetter(0))

        self._interp = interp
        self._loop = loop

        # Timer for tracking local time
        self._timer = Timer(self._keyframes[-1][0], lambda: True)
        self._timer.start()

        # Current keyframe index
        self._current = 0

        if self._interp:
            self.update = self._update_interpolated
        else:
            self.update = self._update_discrete

    @property
    def name(self):
        """Animation's name.

        :getter: yes
        :setter: no
        :type: str
        """
        return self._name

    def _apply_value(self, value):
        """Apply new value to linked object.

        :param obj value: value to apply
        """

        setattr(self._obj, self._attr, value)

    def _update_interpolated(self):
        """Advance animation and interpolate value.

        NOTE: animation frame switching depends on interp mode
        animation with interpolation switches frame only when current local
        time exceeds NEXT frames' time border.
        """

        self._check_animation_state()
        self._timer.update()

        current_time = self._timer.get_elapsed()
        keyframe = self._keyframes[self._current]
        next_keyframe = self._keyframes[self._current + 1]

        # it's time to switch keyframe
        if current_time >= next_keyframe[0]:
            self._current += 1
            keyframe = self._keyframes[self._current]

        if self._current == len(self._keyframes) - 1:
            self._apply_value(keyframe[1])
            self._current += 1
            self._check_animation_state()
            return

        next_keyframe = self._keyframes[self._current + 1]

        value = interpolate(keyframe, next_keyframe, current_time)
        self._apply_value(value)

    def _update_discrete(self):
        """Advance animation without interpolating value.

        NOTE: animation frame switching depends on interp mode
        discrete animation swiches frame and updates value only if
        current local time is >= time of current keyframe.
        No need to worry about calculating value between frames - thus
        no need to complicate behaviour.
        """

        self._check_animation_state()
        self._timer.update()

        keyframe = self._keyframes[self._current]

        # Check if animation need to switch keyframe
        if self._timer.get_elapsed() >= keyframe[0]:
            self._apply_value(keyframe[1])
            self._current += 1

    def _check_animation_state(self):
        """Check animation state and restart if needed.

        :raise StopIteration: when animation exceeded frames.
        """

        if len(self._keyframes) == self._current:
            if self._loop:
                self._current = 0
                self._timer.restart()
            else:
                self._timer.stop()
                raise StopIteration


def linear_equation(val1, val2, time1, time2, current_time):
    """Linear equation to get interpolated value.

    :param float val1: first keyframe value
    :param float val2: second keyframe value
    :param float time1: first keyframe local time
    :param float time2: second keyframe local time
    :param float current_time: current animation local time
    """

    return val1 + (val2 - val1) / (time2 - time1) * (current_time - time1)


def same_type(values, types):
    """Check if values are belongs to same type or type tuple.

    :param collections.Iterable values: values to check type similarity
    :param tuple|type types: type or tuple of types
    """

    return all(map(lambda it: isinstance(it, types), values))


def interpolate(first, second, current_time):
    """Interpolate value by two bounding keyframes.

    :param collections.Iterable first: first bounding keyframe
    :param collections.Iterable second: second bounding keyframe
    :param float current_time: current animation local time

    :raises AnimationBoundariesExceeded: when time interval is invalid
    :raises InterpolationUnknownTypes: when interpolating invalid types
    """

    if not first[0] <= current_time <= second[0]:
        raise AnimationBoundariesExceeded(first[0], current_time, second[0])

    def frames_of(*args):
        """If frames both of specified type."""
        return same_type((first[1], second[1]), args)

    if frames_of(int, float):
        value = linear_equation(
            float(first[1]), float(second[1]),
            float(first[0]), float(second[0]), float(current_time))

    elif frames_of(Point):
        value = linear_equation(
            first[1], second[1], float(first[0]), float(second[0]),
            float(current_time))
    else:
        raise InterpolationUnknownTypes(type(first[1]), type(second[1]))

    return value
