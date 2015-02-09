"""Miscellaneous functions for myhdl.
"""
__author__ = 'Uri Nix'

__all__ = ['cycles', 'clean_vcd']

### Module Globals ###########################################################
from myhdl import now
from glob import iglob, glob
import os
import os.path
import sys

### Building Block Units #####################################################


def cycles():
    """
    Return number of cycles passed in simulation.
    """
    return now() / 2


def clean_vcd(file_name=None):
    """
    Remove all previous VCD created by myhdl.traceSignals() and rename current.

    Parameters:
    -----------
    file_name: string
        file name of stored VCD

    Returns:
    --------
    None
    """
    for f in iglob('*.vcd.*'): os.remove(f)
    if file_name is None:
        vcd_name = os.path.splitext(os.path.basename(sys.argv[0]))[0] + '.vcd'
    else:
        vcd_name = file_name
    vcd_files = glob('*.vcd')
    vcd_files.sort(key=lambda x: os.path.getmtime(x))
    os.rename(vcd_files[-1], vcd_name)


