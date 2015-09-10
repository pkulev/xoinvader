from setuptools import setup, find_packages

#TODO:
#Think about pygame installing.

setup(
    name="XOInvader",
    description="Curses-based space game",
    author="Pavel Kulyov",
    author_email="kulyov.pavel@gmail.com",
    version="0.1a1",
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
