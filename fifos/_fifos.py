"""Behavioural FIFOs for myhdl.
"""
__author__ = 'Uri Nix'

__all__ = ['DCFifo', 'SCFifo']

### Module Globals ###########################################################

from Queue import Queue
from myhdl import always, instances

### Building Block Units #####################################################


class DCFifo(object):
    def __init__(self, depth):
        """
        Dual Clock FIFO using rdy/valid.

        Parameters:
        -----------
        depth: int
            maximum size of FIFO.

        Returns:
        --------
        None
        """
        self.depth_m1 = depth - 1
        self.queue = Queue(maxsize=depth)

    def generate(self,
            i_wrclk, o_wrrdy, i_wrvalid, i_wrdata,
            i_rdclk, i_rdrdy, o_rdvalid, o_rddata,
            o_fullness):
        """
        Generate instance.

        Ports:
        ------
        i_*clk: Signal(bool)
            access clock
        o_wrrdy: Signal(bool)
            FIFO ready to accept data from source on next cycle
        i_rdrdy: Signal(bool)
            Sink ready to accept data from FIFO on next cycle
        i_wrdata, o_rddata: Signal(any)
        i_wrvalid, o_rdvalid: Signal(bool)
            signify that applicable data lines can be sampled
        o_fullness: Signal(int)
            number of elements in FIFO
        """
        @always(i_wrclk.posedge)
        def wr_access():
            o_wrrdy.next = (self.queue.qsize() < self.depth_m1)
            if i_wrvalid and o_wrrdy:
                self.queue.put_nowait(i_wrdata.val)
                o_fullness.next = self.queue.qsize()

        @always(i_rdclk.posedge)
        def rd_access():
            if i_rdrdy and (not self.queue.empty()):
                o_rddata.next = self.queue.get_nowait()
                o_fullness.next = self.queue.qsize()
                o_rdvalid.next = True
            else:
                o_rdvalid.next = False

        return instances()


class SCFifo(object):
    def __init__(self, depth):
        """
        Single Clock FIFO using rdy/valid.

        Parameters:
        -----------
        depth: int
            maximum size of FIFO.

        Returns:
        --------
        None
        """
        self.depth_m1 = depth - 1
        self.queue = Queue(maxsize=depth)

    def generate(self, i_clk,
            o_wrrdy, i_wrvalid, i_wrdata,
            i_rdrdy, o_rdvalid, o_rddata,
            o_fullness):
        """
        Generate instance.

        Ports:
        ------
        i_clk: Signal(bool)
            access clock
        o_wrrdy: Signal(bool)
            FIFO ready to accept data from source on next cycle
        i_rdrdy: Signal(bool)
            Sink ready to accept data from FIFO on next cycle
        i_wrdata, o_rddata: Signal(any)
        i_wrvalid, o_rdvalid: Signal(bool)
            signify that applicable data lines can be sampled
        o_fullness: Signal(int)
            number of elements in FIFO
        """
        @always(i_clk.posedge)
        def wr_access():
            o_wrrdy.next = (self.queue.qsize() < self.depth_m1)
            if i_wrvalid and o_wrrdy:
                self.queue.put_nowait(i_wrdata.val)
                o_fullness.next = self.queue.qsize()

        @always(i_clk.posedge)
        def rd_access():
            if i_rdrdy and (not self.queue.empty()):
                o_rddata.next = self.queue.get_nowait()
                o_fullness.next = self.queue.qsize()
                o_rdvalid.next = True
            else:
                o_rdvalid.next = False

        return instances()

