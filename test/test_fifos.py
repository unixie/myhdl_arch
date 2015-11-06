#! /usr/bin/env python
"""Test myhdl_arch fifos.py.
"""
__author__ = 'Uri Nix'

### Globals ##################################################################
# Module scope imports and variables
import unittest
import myhdl

import sys; sys.path.append(r"../..")
import myhdl_arch

### Classes and Core functions ###############################################


class Source(object):
    """
    Transaction source.
    """
    def __init__(self, plan = (0)):
        self.stimulus = 0
        self.index = 0
        self.plan = plan
        self.trace = []

    def generate(self, i_clk, i_rdy, o_valid, o_data):
        """
        Generate source: attempt to write according to test plan and
        FIFO readiness.

        Data is incremental, with -1 to signify invalid entries.
        """
        @myhdl.always(i_clk.posedge)
        def logic():
            if bool(self.plan[self.index]):
                o_valid.next = True
                if i_rdy:
                    self.stimulus += 1
                    self.trace.append(self.stimulus)
                o_data.next = self.stimulus
            else:
                o_valid.next = False
                o_data.next = -1
            self.index += 1
            if (self.index >= len(self.plan)):
                self.index = 0
        return myhdl.instances()


class Sink(object):
    """
    Transaction sink.
    """
    def __init__(self, plan = (0)):
        self.index = 0
        self.plan = plan
        self.trace = []
        self.rdy_d1 = myhdl.Signal(False)

    def generate(self, i_clk, o_rdy, i_valid, i_data, o_trace_data):
        """
        Generate source: attempt to read according to test plan and
        FIFO readiness.
        """
        @myhdl.always(i_clk.posedge)
        def logic():
            if (o_rdy or self.rdy_d1) and i_valid:
                self.trace.append(i_data.val)
                o_trace_data.next = i_data.val  # for debugging
            if bool(self.plan[self.index]):
                o_rdy.next = True
            else:
                o_rdy.next = False
            self.index += 1
            if (self.index >= len(self.plan)):
                self.index = 0
            self.rdy_d1.next = o_rdy
        return myhdl.instances()


class TestSClkFifo(unittest.TestCase):
    def __init__(self, test_name="TestSClkFifo", test_parameters=None):
        super(TestSClkFifo, self).__init__()
        self.name = test_name
        self.depth = 3
        self.source_plan = [1]
        self.sink_plan = [1]
        if test_parameters:
            self.__dict__.update(test_parameters)
        self.clkgen = myhdl_arch.clocks.ClockGen()
        self.source = Source(self.source_plan)
        self.sink = Sink(self.sink_plan)
        self.fifo = myhdl_arch.fifos.SCFifo(self.depth)

    def shortDescription(self):
        return self.name

    def prepareDUT(self):
        root_clk = myhdl.Signal(False)
        wr_rdy = myhdl.Signal(False)
        wr_valid = myhdl.Signal(False)
        wr_data = myhdl.Signal(0)
        rd_rdy = myhdl.Signal(False)
        rd_valid = myhdl.Signal(False)
        rd_data = myhdl.Signal(0)
        fullness = myhdl.Signal(0)
        trace_data = myhdl.Signal(0)

        clkgen_inst = self.clkgen.generate(root_clk)
        source_inst = self.source.generate(root_clk, wr_rdy, wr_valid, wr_data)
        sink_inst = self.sink.generate(root_clk, rd_rdy, rd_valid, rd_data, trace_data)
        fifo_inst = self.fifo.generate(root_clk, wr_rdy, wr_valid, wr_data, rd_rdy, rd_valid,
                rd_data, fullness)
        return myhdl.instances()

    def setUp(self):
        self.dut = self.prepareDUT()

    def tearDown(self):
        pass

    def runTest(self):
        sim = myhdl.Simulation(self.dut)
        ticks = int(max(len(self.sink_plan), len(self.source_plan)) * 1.5)
        sim.run(ticks)
        #print "Source: %s" % self.source.trace
        #print "Source: %s" % self.source.trace[:len(self.sink.trace)]
        #print "Sink: %s" % self.sink.trace
        self.assertItemsEqual(self.source.trace[:len(self.sink.trace)], self.sink.trace)


class TestDClkFifo(unittest.TestCase):
    def __init__(self, test_name="TestDClkFifo", test_parameters=None):
        super(TestDClkFifo, self).__init__()
        self.name = test_name
        self.depth = 3
        self.wr_ratio = 1
        self.rd_ratio = 1
        self.source_plan = [1]
        self.sink_plan = [1]
        if test_parameters:
            self.__dict__.update(test_parameters)
        self.clkgen = myhdl_arch.clocks.ClockGen()
        self.clkdiv_wr = myhdl_arch.clocks.ClockDivide(self.wr_ratio, self.wr_ratio)
        self.clkdiv_rd = myhdl_arch.clocks.ClockDivide(self.rd_ratio, self.rd_ratio)
        self.source = Source(self.source_plan)
        self.sink = Sink(self.sink_plan)
        self.fifo = myhdl_arch.fifos.DCFifo(self.depth)

    def shortDescription(self):
        return self.name

    def prepareDUT(self):
        root_clk = myhdl.Signal(False)
        wr_clk = myhdl.Signal(False)
        wr_rdy = myhdl.Signal(False)
        wr_valid = myhdl.Signal(False)
        wr_data = myhdl.Signal(0)
        rd_clk = myhdl.Signal(False)
        rd_rdy = myhdl.Signal(False)
        rd_valid = myhdl.Signal(False)
        rd_data = myhdl.Signal(0)
        fullness = myhdl.Signal(0)
        trace_data = myhdl.Signal(0)

        clkgen_inst = self.clkgen.generate(root_clk)
        clkgen_wr_inst = self.clkdiv_wr.generate(root_clk, wr_clk)
        clkgen_rd_inst = self.clkdiv_rd.generate(root_clk, rd_clk)
        source_inst = self.source.generate(wr_clk, wr_rdy, wr_valid, wr_data)
        sink_inst = self.sink.generate(rd_clk, rd_rdy, rd_valid, rd_data, trace_data)
        fifo_inst = self.fifo.generate(wr_clk, wr_rdy, wr_valid, wr_data,
                rd_clk, rd_rdy, rd_valid, rd_data, fullness)
        return myhdl.instances()

    def setUp(self):
        self.dut = self.prepareDUT()

    def tearDown(self):
        pass

    def runTest(self):
        sim = myhdl.Simulation(self.dut)
        ticks = int(max(len(self.sink_plan), len(self.source_plan)) * 1.5)
        sim.run(ticks)
        #print "Source: %s" % self.source.trace
        #print "Source: %s" % self.source.trace[:len(self.sink.trace)]
        #print "Sink: %s" % self.sink.trace
        self.assertItemsEqual(self.source.trace[:len(self.sink.trace)], self.sink.trace)


### unittest test discovery protocol for regression ##########################

def make_test_plan(depth):
# Story:
# (1) start with empty and check underflow
# (2) read/write alternately on edge of underflow
# (3) generate full fifo
# (4) read/write alternately on edge of overflow
# (5) freeze state
# (6) partial read
# (7) read/write alternately on middle of fifo
    source = [0, 1, 1, 1, 0, 0, 1]
    sink =   [1, 1, 0, 1, 0, 1, 1]
    duration = [depth+5, 10, depth+3, 7, 5, 3, 9]
    duration = [2*x for x in duration]  # convert to clock cycles
    source = [[s]*d for s,d in zip(source, duration)]
    sink = [[s]*d for s,d in zip(sink, duration)]
    source_plan = [item for sublist in source for item in sublist]
    sink_plan = [item for sublist in sink for item in sublist]
    return (source_plan, sink_plan)


def make_sc_fifo_parms(depths_to_test):
    test_parms = []
    for d in depths_to_test:
        plans = make_test_plan(d)
        test_parms.append(dict({'depth':d, 'source_plan':plans[0], 'sink_plan':plans[1]}))
    return test_parms


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    sc_test_parms = make_sc_fifo_parms(range(2, 14))
    for i,p in enumerate(sc_test_parms):
        suite.addTest(TestSClkFifo("scfifo_test%d" % i, p))
        suite.addTest(TestDClkFifo("dcfifo_test%d" % i, p))

    ratios = zip((2,3,4,5,6,7,8), (1,1,1,1,1,1,1))
    for r in ratios:
        for t in sc_test_parms:
            t.update(dict({'wr_ratio':r[0], 'rd_ratio':r[1]}))
        for i,p in enumerate(sc_test_parms):
            suite.addTest(TestDClkFifo("dcfifo_test%d-w%d-r%d" % (i, r[0], r[1]), p))

    ratios = zip((1,1,1,1,1,1,1), (2,3,4,5,6,7,8))
    for r in ratios:
        for t in sc_test_parms:
            t.update(dict({'wr_ratio':r[0], 'rd_ratio':r[1]}))
        for i,p in enumerate(sc_test_parms):
            suite.addTest(TestDClkFifo("dcfifo_test%d-w%d-r%d" % (i, r[0], r[1]), p))

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
    parser.add_argument('--depth',
                        default=3,
                        type=int,
                        help='Fifo depth'
    )

    # positional arguments

    ### argument validation ##################################################
    args = parser.parse_args()

    ### process ##############################################################

    plan = make_test_plan(args.depth)
    test_parms = {'depth':args.depth, 'source_plan':plan[0], 'sink_plan':plan[1]}
    ticks = int(len(plan[0]) * 1.5)

    ### MyHDL Simulation
    test = TestSClkFifo('StandAlone', test_parms)
    top_inst = myhdl.traceSignals(test.prepareDUT)
    sim = myhdl.Simulation(top_inst)
    sim.run(ticks)
    myhdl_arch.misc.clean_vcd()
