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

        # Transaction request wires are deprecated

        # prefetch controller



    return PREFETCH_BUFFER()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(prefetch_buffer()), "prefetch_buffer.fir"))
