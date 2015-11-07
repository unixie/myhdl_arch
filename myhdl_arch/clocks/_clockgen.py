"""Behavioural Clock generators for myhdl.
"""
__author__ = 'Uri Nix'

__all__ = ['ClockGen', 'ClockDivide']

### Module Globals ###########################################################

### MyHDL
from myhdl import always, instance, delay, now

### Building Block Units #####################################################


class ClockGen(object):
    def __init__(self, ticks=1):
        """
        Clock Generator.

        Parameters:
        -----------
        ticks: int
            simulation delay per clock edge.

        Returns:
        --------
        None
        """
        assert isinstance(ticks, int)
        self.ticks = ticks

    def generate(self, o_clk):
        """
        Generate instance.

        Ports:
        ------
        o_clk: bool
            logic clock
        """
        @always(delay(self.ticks))
        def logic():
            o_clk.next = not o_clk

        return logic


class ClockDivide(object):
    def __init__(self, high=1, low=1):
        """
        Divide clock by programming high and low cycle lengths.
        Uses counter updated per i_clk.posedge.

        Parameters:
        -----------
        high, low: int
            number of i_clk cycles in o_clk high and low phases.

        Parameters:
        -----------
        high, low: int
            number of i_clk cycles in o_clk high and low phases.

        Returns:
        --------
        None
        """
        assert isinstance(high, int)
        assert isinstance(low, int)
        self.high = high
        self.low = low
        self.cycle_counter = 0

    def generate(self, i_clk, o_clk):
        """
        Generate instance.

        Ports:
        ------
        i_clk: bool
            input clock
        o_clk: bool
            divided output clock
        """
        @always(i_clk.posedge)
        def logic():
            self.cycle_counter += 1
            if self.cycle_counter >= (self.high if o_clk.val else self.low):
                o_clk.next = not o_clk
                self.cycle_counter = 0

        return logic
