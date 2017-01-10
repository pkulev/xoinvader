|Build Status| |codecov.io|

XOInvader
=========

Attempt to create small but serious game using **python** and
**ncurses**.

Requrements
-----------

-  Python3
-  Pygame >=1.9.0 (pygame.Mixer)
-  Tornado 3.x
-  ncurses >=5.9

Optional requirements (for graphics)
------------------------------------

-  SDL with devel
-  gcc with devel
-  python devel files


Documentation
-------------

Documentation can be found `here <http://www.g-v.im/>`__.

Development `wiki <https://github.com/pkulev/xoinvader/wiki/>`_.

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
