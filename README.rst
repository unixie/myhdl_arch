MyHDL Arch
==========


What is MyHDL?
--------------
`MyHDL <http://www.myhdl.org/>`_ is a free, open-source package for using Python as a hardware
description and verification language.


What is MyHDL Arch?
-------------------
This package contains common components for *architectural* hardware modelling, utilizing MyHDL as an
infrastructure for idioms and simulation. Thus idioms such as signals and waveforms are shared 
between architects and designers.

Loosely comparable to SystemC TLM 1.0, the package contains a clock generator and dual-clock FIFO,
which can be used to add a timed aspect to otherwise sequential models.

MyHDL Arch is NOT meant to be synthesizeable: the intention is to remain at a high level of
expressiveness, allowing the architect full usage of Python's capabilites.


License
-------
MyHDL Arch is available under the MIT license.  See LICENSE.txt.

MyHDL Arch does not contain derivative of any portion of MyHDL source code, 
but is designed to work with MyHDL, therefore is a work that uses MyHDL.


Installation
------------
TBA: update after adding to PYPI.


Usage
-----
See test directory for examples of the components as part of testbenches.
Each test suite can be executed in two manners:

- Via standard unittest::

  $ python -m unittest discover <path_to_myhdl_arch>/test

- Standalone::

  $ cd <path_to_myhdl_arch>/test
  $ ./test_clocks.py --help


