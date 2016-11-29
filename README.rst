|Build Status| |codecov.io|

XOInvader
=========

Attempt to create small but serious game using **python** and
**ncurses**. **Migrating from curses to PyGame.**

Requrements
-----------

-  Python3 (Tested with 3.4.1)
-  pygame >=1.9.0 (pygame.Mixer)
-  SDL with devel
-  gcc with devel
-  python devel files
-  ncurses >=5.9

Documentation
-------------

Documentation can be found `here <http://www.g-v.im/>`__.

Tests
-----

-  Coverage ~40%

Installation
------------

Installation across linux distributives is quite painful because of
pygame dependency and lack of Python2.x support. The only way is to try
``python3 setup.py install`` and contact me if something goes wrong. The
best way to install pygame apparently is to clone repo, compile and
install using **python3** and **make**.

.. |Build Status| image:: https://travis-ci.org/pkulev/xoinvader.svg?branch=master
   :target: https://travis-ci.org/pkulev/xoinvader
.. |codecov.io| image:: http://codecov.io/github/pkulev/xoinvader/coverage.svg?branch=master
   :target: http://codecov.io/github/pkulev/xoinvader?branch=master
