"""
Copyright Digisim, Computer Architecture team of South China University of Technology,

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   Author Name: Ruohui Chen
   Date: 2021-03-01
   File Name: prefetch_buffer.py
   Description: "Prefetch Buffer that caches instructions. this cuts overly long critical
                paths to the instruction cache." -- original RIS5Y annotation
"""

from pyhcl import *
from math import log
from src.rtl.prefetch_controller import *
from src.rtl.obi_interface import *
from src.rtl.fifo import *


# PULP_XPULP is for PULP ISA Extension, deprecated in our implementation
def prefetch_buffer(PULP_OBI=0):
    """
        args:
            PULP_OBI: Legacy PULP OBI behavior
    """

    # local parameters
    # FIFO_DEPTH also controls the number of outstanding memory requests
    # FIFO_DEPTH > 1 -> respect assertion in prefetch controller
    # FIFO_DEPTH % 2 == 0 -> FIFO implementation
    FIFO_DEPTH = 2
    FIFO_ADDER_DEPTH = int(log(FIFO_DEPTH, 2))

    class PREFETCH_BUFFER(Module):
        io = IO(
            req_i=Input(Bool),
            branch_i=Input(Bool),
            branch_addr_i=Input(U.w(32)),

            # Deprecated hardware loop ports

            fetch_ready_i=Input(Bool),
            fetch_valid_o=Output(Bool),
            fetch_rdata_o=Output(U.w(32)),

            # goes to instruction memory / instruction cache
            instr_req_o=Output(Bool),
            instr_gnt_i=Input(Bool),
            instr_addr_o=Output(U.w(32)),
            instr_rdata_i=Input(U.w(32)),
            instr_rvalid_i=Input(Bool),

            # Not used yet (future addition, from RIS5Y source code)
            instr_err_i=Input(Bool),
            instr_err_pmp_i=Input(Bool),

            # Prefetch Buffer Status
            busy_o=Output(Bool)
        )

        # In PyHCL, these wires are redundant
        # Transaction request Wires (between prefetch_controller and obi_interface)
        trans_valid = Wire(Bool)
        trans_ready = Wire(Bool)
        trans_addr = Wire(U.w(32))

        fifo_flush = Wire(Bool)
        fifo_flush_but_first = Wire(Bool)
        fifo_cnt = Wire(U.w(FIFO_ADDER_DEPTH+1))

        fifo_rdata = Wire(U.w(32))
        fifo_push = Wire(Bool)
        fifo_pop = Wire(Bool)
        fifo_empty = Wire(Bool)
        fifo_full = Wire(Bool)

        # Transaction response interface (between obi_interface and fifo)
        resp_valid = Wire(Bool)
        resp_rdata = Wire(U.w(32))
        resp_err = Wire(Bool)

        pref_ctl = prefetch_controller(DEPTH=FIFO_DEPTH, PULP_OBI=PULP_OBI)
        fifo_i = fifo(FALL_THROUGH=0, DATA_WIDTH=32, DEPTH=FIFO_DEPTH)
        obi_inf = obi_interface(TRANS_STABLE=0)

        ##################################################################################
        # Prefetch Controller
        ##################################################################################

        pref_ctl.io.req_i <<= io.req_i
        pref_ctl.io.branch_i <<= io.branch_i
        pref_ctl.io.branch_addr_i <<= io.branch_addr_i
        io.busy_o <<= pref_ctl.io.busy_o

        trans_valid <<= pref_ctl.io.trans_valid_o
        pref_ctl.io.trans_ready_i <<= trans_ready
        trans_addr <<= pref_ctl.io.trans_addr_o

        pref_ctl.io.resp_valid_i <<= resp_valid

        pref_ctl.io.fetch_ready_i <<= io.fetch_ready_i
        io.fetch_valid_o <<= pref_ctl.io.fetch_valid_o

        fifo_push <<= pref_ctl.io.fifo_push_o
        fifo_pop <<= pref_ctl.io.fifo_pop_o
        fifo_flush <<= pref_ctl.io.fifo_flush_o
        fifo_flush_but_first <<= pref_ctl.io.fifo_flush_but_first_o
        pref_ctl.io.fifo_cnt_i <<= fifo_cnt
        pref_ctl.io.fifo_empty_i <<= fifo_empty

        ##################################################################################
        # Fetch FIFO && fall-through path
        ##################################################################################

        fifo_i.io.flush_i <<= fifo_flush
        fifo_i.io.flush_but_first_i <<= fifo_flush_but_first
        fifo_i.io.testmode_i <<= U(0)
        fifo_full <<= fifo_i.io.full_o
        fifo_empty <<= fifo_i.io.empty_o
        fifo_cnt <<= fifo_i.io.cnt_o
        fifo_i.io.data_i <<= resp_rdata
        fifo_i.io.push_i <<= fifo_push
        fifo_rdata <<= fifo_i.io.data_o
        fifo_i.io.pop_i <<= fifo_pop

        # First POP from the FIFO if it is not empty.
        # Otherwise, try to fall-through it.
        io.fetch_rdata_o <<= Mux(fifo_empty, resp_rdata, fifo_rdata)

        ##################################################################################
        # OBI interface
        ##################################################################################
        obi_inf.io.trans_valid_i <<= trans_valid
        trans_ready <<= obi_inf.io.trans_ready_o
        obi_inf.io.trans_addr_i <<= CatBits(trans_addr[31:2], U.w(2)(0))
        obi_inf.io.trans_we_i <<= U.w(1)(0)     # Instruction interface, never write
        obi_inf.io.trans_be_i <<= U.w(4)(15)    # 4'b1111, no use
        obi_inf.io.trans_wdata_i <<= U.w(32)(0)       # no use
        obi_inf.io.trans_atop_i <<= U.w(6)(0)         # no use

        resp_valid <<= obi_inf.io.resp_valid_o
        resp_rdata <<= obi_inf.io.resp_rdata_o
        resp_err <<= obi_inf.io.resp_err_o

        io.instr_req_o <<= obi_inf.io.obi_req_o
        obi_inf.io.obi_gnt_i <<= io.instr_gnt_i
        io.instr_addr_o <<= obi_inf.io.obi_addr_o
        obi_inf.io.obi_rdata_i <<= io.instr_rdata_i
        obi_inf.io.obi_rvalid_i <<= io.instr_rvalid_i
        obi_inf.io.obi_err_i <<= io.instr_err_i

    return PREFETCH_BUFFER()


if __name__ == '__main__':
    # In current prefetch_buffer implements, there exists combinational loops:
    # PREFETCH_BUFFER.pref_ctl.io_fifo_empty_i
    # PREFETCH_BUFFER.pref_ctl._T_23
    # PREFETCH_BUFFER.pref_ctl.fifo_valid
    # PREFETCH_BUFFER.pref_ctl._T_27
    # PREFETCH_BUFFER.pref_ctl._T_28
    # PREFETCH_BUFFER.pref_ctl._T_31
    # PREFETCH_BUFFER.pref_ctl.io_fifo_push_o
    # PREFETCH_BUFFER.fifo_push
    # PREFETCH_BUFFER.fifo_i.io_push_i
    # PREFETCH_BUFFER.fifo_i._T_1
    # PREFETCH_BUFFER.fifo_i._T_2
    # PREFETCH_BUFFER.fifo_i._T_3
    # PREFETCH_BUFFER.fifo_i.io_empty_o
    # PREFETCH_BUFFER.fifo_empty
    # PREFETCH_BUFFER.pref_ctl.io_fifo_empty_i
    # Please use "firrtl -i prefetch_buffer.fir -o prefetch_buffer.fir.v --no-check-comb-loops"
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(prefetch_buffer()), "prefetch_buffer.fir"))
