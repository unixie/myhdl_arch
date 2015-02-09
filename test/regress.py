#! /usr/bin/env python
"""Regression test runner.
"""
__author__ = 'Uri Nix'

### Globals ##################################################################
# Module scope imports and variables
import unittest

### Classes and Core functions ###############################################

### Command Line Interface ###################################################
if __name__ == '__main__':

    ### CLI Option Parser ####################################################
    import argparse

    desc = __doc__ + '''\n
Command line exploration.
    '''
    epi = '''
    '''

    # merge several help formatters
    class MyFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
        pass

    parser = argparse.ArgumentParser(description=desc, epilog=epi,
                                     formatter_class=MyFormatter)

    # options
    parser.add_argument("-v", "--verbosity",
            type = int,
            default = 2,
            help = "TestRunner verbosity level")

    parser.add_argument("--failfast",
            action = 'store_true',
            default = False,
            help = "Fail regression on first failure")

    # positional arguments
    parser.add_argument("tests_dir",
            type = str,
            help = "Root directory for test discovery")

    ### argument validation ##################################################
    args = parser.parse_args()

    ### process ##############################################################
    tests = unittest.TestLoader().discover(args.tests_dir)
    unittest.TextTestRunner(verbosity = args.verbosity, failfast = args.failfast).run(tests)


