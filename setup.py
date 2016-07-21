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
    description="Curses/Pygame space game",
    long_description=description(),
    author="Pavel Kulyov",
    author_email="kulyov.pavel@gmail.com",
    version="0.1",
    url="http://www.g-v.im/",
    packages=find_packages(),
    package_dir={"xoinvader": "xoinvader"},
    include_package_data=True,
    license="MIT",
    platforms="Posix",
    install_requires=[],
    entry_points="""
    [console_scripts]
    xoigame = xoinvader.game:main
    """
)
