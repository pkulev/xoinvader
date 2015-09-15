import sys
import unittest
import pprint

from xoinvader.utils import create_logger
from xoinvader.utils import InfiniteList
from xoinvader.utils import Point
from xoinvader.utils import Surface
from xoinvader.utils import Timer


class TestLogger(unittest.TestCase):
    def test_create_logger(self):
        logger = create_logger("test", "test.log")
        self.assertTrue(logger)


class TestPoint(unittest.TestCase):
    def test_point_operations(self):
        ax, ay, az = 10, 10, 10
        bx, by, bz = 20, 20, 20
        a = Point(ax, ay, az)
        b = Point(bx, by, bz)

        self.assertEqual(a.x, ax)
        self.assertEqual(a.y, ay)
        self.assertEqual(a.z, az)
        self.assertEqual(b.x, bx)
        self.assertEqual(b.y, by)
        self.assertEqual(b.z, bz)

        self.assertEqual(a.__repr__(), "Point(x={0}, y={1}, z={2})".format(a.x, a.y, a.z))

        self.assertEqual(a + b, Point(ax + bx, ay + by, az + bz))

        a.x = bx
        a.y = by
        a.z = bz

        self.assertEqual(a.x, bx)
        self.assertEqual(a.y, by)
        self.assertEqual(a.z, bz)

        b.x = -bx
        b.y = -by
        b.z = -bz

        self.assertEqual(a + b, Point(0, 0, 0))
        self.assertEqual(a + Point(-50, -50, -50), Point(-30, -30, -30))


class TestInfiniteList(unittest.TestCase):
    def test_infinite_list_operations(self):
        # Test empty InfiniteList behaviour

        inf_list = InfiniteList()
        for func in [inf_list.current, inf_list.next, inf_list.prev]:
            self.assertRaises(IndexError, func)

        # Test one element behaviour
        data = "test1"
        inf_list = InfiniteList([data])

        self.assertEqual(len(inf_list), 1)
        self.assertEqual(inf_list[0], data)
        self.assertEqual(inf_list.current(), data)
        self.assertEqual(inf_list.next(), data)
        self.assertEqual(inf_list.prev(), data)

        # Test many elements behaviour


class TestSurface(unittest.TestCase):
    def setUp(self):
        self.image = [
                [" ", "O", " "],
                ["x", "X", "x"]]

        self.style = []

    def test_surface_attributes(self):
        surface = Surface(self.image)
        self.assertEqual(surface.height, len(self.image))
        self.assertEqual(surface.width, len(self.image[0]))
        self.assertEqual(surface._image)

    def test_image_generator(self):
        surface = Surface(self.image)
        image_gen = surface.get_image()
        for lpos, image, style in image_gen:
            self.assertEqual(self.image[lpos.y][lpos.x], image)
            self.assertEqual(style, None)


class TestTimer(unittest.TestCase):
    def _func(self):
        self.check = True

    @unittest.skip("Need to fix timer or test.")
    def test_timer_get_elapsed(self):
        self.check = False
        self.timer = Timer(5.0, self._func)
        self.timer.start()
        while self.timer.running:
            self.assertGreaterEqual(self.timer.get_elapsed(), 0.0,
                    msg="check={0}\n".format(str(self.check)) + pprint.pformat(vars(self.timer)))
            self.timer.update()
            self.assertGreaterEqual(self.timer.get_elapsed(), 0.0,
                    msg="check={0}\n".format(str(self.check)) + pprint.pformat(vars(self.timer)))
