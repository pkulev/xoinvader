|Build Status| |codecov.io|

XOInvader
=========

Attempt to create small but serious game using **python** and
**ncurses**.

Requirements
-----------

-  Python3
-  Tornado 4.x
-  ncurses >=5.9

Optional requirements (for graphics)
------------------------------------
-  Pygame >=1.9.0 (pygame.Mixer)
-  SDL with devel
-  gcc with devel
-  python devel files


Documentation
-------------

Documentation can be found `here <http://www.g-v.im/>`__.

Development `wiki <https://github.com/pkulev/xoinvader/wiki/>`_.

Tests
-----
-  To run tests use `make tests`
-  To show coverage use `make view_cov`


Development Environment
-----------------------

.. console::
   # install virtualenv
   $ make devel
   $ source .venv/bin/activate
   $ pip install -e .

   $ xoigame  # ASCII with sound (Pygame.Mixer required)
   $ xoigame -ns  # ASCII without sound (pygame not required)
   $ xoigame -vd pygame-sdl  # Pygame-based version


.. |Build Status| image:: https://travis-ci.org/pkulev/xoinvader.svg?branch=master
   :target: https://travis-ci.org/pkulev/xoinvader
.. |codecov.io| image:: http://codecov.io/github/pkulev/xoinvader/coverage.svg?branch=master
   :target: http://codecov.io/github/pkulev/xoinvader?branch=master
