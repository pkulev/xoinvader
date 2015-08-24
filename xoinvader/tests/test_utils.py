import sys
import unittest
import pprint

from xoinvader.utils import create_logger
from xoinvader.utils import InfiniteList
from xoinvader.utils import Point


class TestUtils(unittest.TestCase):
    def test_create_logger(self):
        logger = create_logger("test", "test.log")
        self.assertTrue(logger)

    def test_point_operations(self):
        ax, ay, bx, by = 10, 10, 20, 20
        a = Point(ax, ay)
        b = Point(bx, by)

        self.assertEqual(a.x, ax)
        self.assertEqual(a.y, ay)
        self.assertEqual(b.x, bx)
        self.assertEqual(b.y, by)

        self.assertEqual(a.__repr__(), "Point(x={}, y={})".format(a.x, a.y))

        self.assertEqual(a + b, Point(ax + bx, ay + by))

        a.x = bx
        a.y = by

        self.assertEqual(a.x, bx)
        self.assertEqual(a.y, by)

        b.x = -bx
        b.y = -by

        self.assertEqual(a + b, Point(0, 0))
        self.assertEqual(a + Point(-50, -50), Point(-30, -30))

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
