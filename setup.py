"""Setup manifest for XOInvader."""

import os

from setuptools import setup, find_packages


BASEDIR = os.path.abspath(os.path.dirname(__file__))


def read(filename):
    """Read description."""
    with open(os.path.join(BASEDIR, filename)) as fd:
        return fd.read()


# TODO: Think about pygame installing.

setup(
    name="XOInvader",
    description="Curses/Pygame space game",
    version="0.1",
    author="Pavel Kulyov",
    author_email="kulyov.pavel@gmail.com",
    long_description=read("README.md"),
    url="http://www.g-v.im/",
    packages=find_packages(),
    license="MIT",
    include_package_data=True,
    platforms="Posix",
    install_requires=[],

    entry_points="""
    [console_scripts]
    xoigame = xoinvader.game:main
    """,

    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console :: Curses",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Games/Entertainment :: Arcade",
        "Topic :: Software Development :: Libraries :: pygame",
    ]
)
