#! /usr/bin/env python
"""Test myhdl_atk clocks.py.
"""
__author__ = 'Uri Nix'

### Globals ##################################################################
# Module scope imports and variables
import unittest
import myhdl

import sys; sys.path.append(r"../..")
import myhdl_atk

### Classes and Core functions ###############################################

class ClockMonitor(object):
    """
    Clock counting facilities.
    """
    def __init__(self):
        self.high = 0.0
        self.low = 0.0
        self.cycles = 0.0

    def counters(self):
        mean_high = int(self.high/self.cycles)
        mean_low = int(self.low/self.cycles)
        return mean_high, mean_low

    def generate(self, i_clk, i_testclk):
        """
        Generate instance.

        Ports:
        ------
        i_clk: bool
            logic clock
        i_testclk: bool
            clock signal to monitor
        """
        @myhdl.always(i_clk.posedge)
        def count_hl():
            if i_testclk.val:
                self.high += 1
            else:
                self.low += 1

        @myhdl.always(i_testclk.posedge)
        def count_cycles():
            self.cycles += 1

        return myhdl.instances()


class TestClockDivide(unittest.TestCase):
    def __init__(self, test_name="TestClockDivide", test_parameters=None):
        super(TestClockDivide, self).__init__()
        self.name = test_name
        self.ticks = 10
        self.high = 1
        self.low = 1
        self.init_clk = True
        if test_parameters:
            self.__dict__.update(test_parameters)
        self.monitor = ClockMonitor()
        self.clkgen = myhdl_atk.clocks.ClockGen()
        self.clkdiv = myhdl_atk.clocks.ClockDivide(self.high, self.low)

    def shortDescription(self):
        return self.name

    def prepareDUT(self):
        root_clk = myhdl.Signal(self.init_clk)
        div_clk = myhdl.Signal(self.init_clk)
        clkgen_inst = self.clkgen.generate(root_clk)
        clkdiv_inst = self.clkdiv.generate(root_clk, div_clk)
        monitor_inst = self.monitor.generate(root_clk, div_clk)
        return myhdl.instances()

    def setUp(self):
        self.dut = self.prepareDUT()

    def tearDown(self):
        pass

    def runTest(self):
        sim = myhdl.Simulation(self.dut)
        sim.run(self.ticks)
        print "\nMonitor: high=%3d low=%3d" % self.monitor.counters()
        print "Test:    high=%3d low=%3d" % (self.high, self.low)
        self.assertItemsEqual(self.monitor.counters(), (self.high, self.low))


### unittest test discovery protocol for regression ##########################

test_parms = (
        {"init_clk" : True, "high" : 1, "low" : 1, "ticks" : 23},
        {"init_clk" : True, "high" : 5, "low" : 3, "ticks" : 50},
        {"init_clk" : False, "high" : 3, "low" : 3, "ticks" : 143},
        {"init_clk" : False, "high" : 4, "low" : 4, "ticks" : 97}
        )

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for i,p in enumerate(test_parms):
        suite.addTest(TestClockDivide("clocks_test%d" % i, p))
    return suite


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
    parser.add_argument('--high',
                        default=1,
                        type=int,
                        help='Divided high cycles'
    )
    parser.add_argument('--low',
                        default=1,
                        type=int,
                        help='Divided low cycles'
    )
    parser.add_argument('--init-clk',
                        default=False,
                        type=bool,
                        help='Initial state of clock signal'
    )
    parser.add_argument('-t', '--ticks',
                        default=100,
                        type=int,
                        help='Simulation ticks'
    )

    # positional arguments

    ### argument validation ##################################################
    args = parser.parse_args()

    ### process ##############################################################

    ### MyHDL Simulation
    test = TestClockDivide('StandAlone', vars(args))
    top_inst = myhdl.traceSignals(test.prepareDUT)
    sim = myhdl.Simulation(top_inst)
    sim.run(args.ticks)
    myhdl_atk.misc.clean_vcd()
