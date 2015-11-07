MyHDL Arch
==========


What is MyHDL Arch?
-------------------
This package contains common components for *architectural* hardware modelling, utilizing `MyHDL <http://www.myhdl.org/>`_ as an infrastructure for idioms and simulation.
Thus idioms such as signals and waveforms are shared between architects and designers.

Loosely comparable to SystemC TLM 1.0, the package contains a clock generator and dual-clock FIFO,
which can be used to add a timed aspect to otherwise sequential models.

MyHDL Arch is NOT meant to be synthesizeable: the intention is to remain at a high level of
expressiveness, allowing the architect full usage of Python's capabilites.


License
-------
MyHDL Arch is available under the MIT license.  See LICENSE.txt.

MyHDL Arch does not contain derivative of any portion of MyHDL source code, 
but is designed to work with MyHDL.


Installation
------------
Proper installation is WIP, in the meantime please clone and follow the usage instructions.

.. Note:: Requires myhdl version 0.7 onwards, available on `PYPI <http://pypi.python.org/pypi/myhdl/>`_


Usage
-----
See test directory for examples of the components as part of testbenches.
Each test suite can be executed in two manners:

- Via standard unittest::

  $ python -m unittest discover <path_to_myhdl_arch>/test

- Standalone::

  $ cd <path_to_myhdl_arch>/test
  $ ./test_clocks.py --help

The standalone method is useful for exploration and development.

