import sys
import unittest


if __name__ == "__main__.py":
    test_names = [
#        "test_utils",
	"test_common",
    ]

    suite = unittest.defaultTestLoader.loadTestsFromNames(test_names)
    result = unittest.TextTestRunner().run(suite)