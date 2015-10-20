"""Setup manifest for XOInvader."""

import os

from setuptools import setup, find_packages


BASEDIR = os.path.abspath(os.path.dirname(__file__))


def description():
    """Read description."""
    with open(os.path.join(BASEDIR, "README.md")) as fd:
        return fd.read()


# TODO: Think about pygame installing.

setup(
    name="XOInvader",
    description="Curses-based space game",
    long_description=description(),
    author="Pavel Kulyov",
    author_email="kulyov.pavel@gmail.com",
    version="0.1a1",
    url="http://www.g-v.im/",
    py_modules=["game"],
    packages=find_packages(),
    package_dir={"xoinvader": "xoinvader"},
    package_data={"xoinvader": ["config/*.json", "res/*"]},
    licence="MIT",
    platforms="Posix",
    install_requires=[],
    entry_points="""
    [console_scripts]
    xoigame = xoinvader.game:main
    """
)
