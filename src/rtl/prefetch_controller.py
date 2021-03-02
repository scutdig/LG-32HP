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
   File Name: prefetch_controller.py
   Description: "Prefetch Controller which receives control flow
                 information (req_i, branch_*) from the Fetch stage
                 and based on that performs transactions requests to the
                 bus interface adapter instructions. Prefetching based on
                 incrementing addressed is performed when no new control
                 flow change is requested. New transaction requests are
                 only performed if it can be guaranteed that the fetch FIFO
                 will not overflow (resulting in a maximum of DEPTH
                 outstanding transactions." -- original RIS5Y annotation
"""
from pyhcl import *
from ..include.pkg import *
from math import log


def prefetch_controller(PULP_OBI=0, DEPTH=4):
    """
        args:
            PULP_OBI: Legacy PULP OBI behavior
            DEPTH: Prefetch FIFO Depth
    """
    FIFO_ADDR_DEPTH = int(log(DEPTH, 2)) if DEPTH > 1 else 1

    class PREFETCH_CONTROLLER(Module):
        io = IO(
            # Fetch stage interface
            req_i=Input(Bool),              # Fetch stage requests instructions
            branch_i=Input(Bool),           # Taken branch
            branch_addr_i=Input(U.w(32)),   # Taken branch address (only valid when branch_i = 1)
            busy_o=Output(Bool),            # Prefetcher busy

            # Deprecated hardware loop ports

            # Transaction request interface
            trans_valid_o=Output(Bool),     # Transaction request valid (to bus interface adapter)
            trans_ready_i=Input(Bool),      # Transaction request ready
                                            # ((trans_valid_o && trans_ready_i) -> transaction gets accepted)
            trans_addr_o=Output(U.w(32)),   # Transaction address (only valid when trans_valid_o == 1)

            # Transaction response interface
            resp_valid_i=Input(Bool),

            # Fetch interface is ready/valid
            fetch_ready_i=Input(Bool),
            fetch_valid_o=Output(Bool),

            # FIFO interface
            fifo_push_o=Output(Bool),               # PUSH an instruction into the FIFO
            fifo_pop_o=Output(Bool),                # POP an instruction from the FIFO
            fifo_flush_o=Output(Bool),              # Flush the FIFO
            fifo_flush_but_first_o=Output(Bool),    # Flush the FIFO, but keep the first instruction if present
            fifo_cnt_i=Input(U.w(FIFO_ADDR_DEPTH)), # Number of valid items/words in the prefetch FIFO
            fifo_empty_i=Input(U.w(Bool))           # FIFO is empty
        )

        ##################################################################################
        # Module internal signals
        ##################################################################################

        # Using Python built-in Enum
        state_q, next_state = [RegInit(U.w(1)(0)) for _ in range(2)]

        # Transaction counter and Next value for cnt_q
        cnt_q, nex_cnt = [RegInit(U.w(FIFO_ADDR_DEPTH)(0)) for _ in range(2)]

        count_up = Wire(Bool)   # Increment outstanding transaction count by 1 (can happen at same time as count_down)
        count_down = Wire(Bool) # Decrement outstanding transaction count by 1 (can happen at same time as count_up)

        # Response flush counter and Next value for flush_cnt_q
        # To flush speculative responses after branch
        flush_cnt_q, next_flush_cnt = [RegInit(U.w(FIFO_ADDR_DEPTH)(0)) for _ in range(2)]

        # Transaction address
        trans_addr_q = RegInit(U.w(32)(0))
        trans_addr_incr = Wire(U.w(32))

        # Word-aligned branch target address
        aligned_branch_addr = Wire(U.w(32))

        # FIFO auxiliary signal
        fifo_valid = Wire(Bool)             # FIFO output valid (if !fifo_empty)
        # FIFO_cnt signal, masked when we are branching to allow a new memory request in that cycle
        fifo_cnt_masked = Wire(U.w(32))

        # Deprecated hardware loop signals

        ##################################################################################
        # Prefetch buffer status
        ##################################################################################

        # Busy is there are ongoing (or potentially outstanding) transfers
        io.busy_o <<= (cnt_q != U.w(3)(0)) | io.trans_valid_o

        ##################################################################################
        # IF/ID interface
        ##################################################################################

        # Fetch valid control. Fetch NEVER valid if jumping or flushing responses.
        # Fetch valid if there are instructions in FIFO or there is an incoming instruction from memory
        io.fetch_valid_o <<= (fifo_valid | io.resp_valid_i) & (~(io.branch_i | (flush_cnt_q > U(0))))

        ##################################################################################
        # Transaction request generation
        # Transactions between obi interface and prefetch buffer
        # Assumes that corresponding response is at least 1 cycle after request
        # - Only request transaction when fetch stage requires fetch (req_i), and
        # - make sure that FIFO never overflows: fifo_cnt_i + cnt_q < DEPTH
        ##################################################################################

        # Prefetcher will only perform WORD fetches
        aligned_branch_addr <<= CatBits(io.branch_addr_i[31:2], U.w(2)(0))

        # Increment address (always WORD fetch)
        trans_addr_incr <<= CatBits(io.trans_addr_q[31:2], U.w(2)(0)) + U.w(32)(4)

        # Transaction request generation
        if PULP_OBI == 0:
            # TODO: I cannot found the combinatorial path from instr_ravlid_i to instr_req_o
            # OBI compatible (avoids combinatorial path from instr_rvalid_i to instr_req_o)
            # Multiple trans_* transactions can be issued (and accepted) before a response
            # (resp_*) is received.
            # @Ruohui Chen: if fifo_cnt_masked (optimized fifo_cnt_i) and the count of
            # current transactions less then the depth of the queue, allow to request
            # another transaction.
            io.trans_valid_o <<= io.req_i & (fifo_cnt_masked + cnt_q < U(DEPTH))
        else:
            # TODO: Remind the timing critical path noticed in here
            # Legacy PULP OBI behavior, i.e. only issue subsequent transaction if preceding transfer
            # is about to finish (re-introducing timing critical path from instr_rvalid_i to instr_req_o)
            io.trans_valid_o <<= Mux(cnt_q == U(0),
                                     io.req_i & (fifo_cnt_masked + cnt_q < U(DEPTH)),
                                     (io.req_i & fifo_cnt_masked + cnt_q < U(DEPTH)) & io.resp_valid_i)

        # Optimize fifo_cnt_i:
        # fifo_cnt_i is used to understand if we can perform new meory requests
        # When branching , we flush both the FIFO and the outstanding requests. Therefore,
        # there is surely space for a new request.
        # Masking fifo_cnt in this case allows for making a new request when the FIFO
        # is not empty and we are jumping, and (fifo_cnt_i + cnt_q == DEPTH)
        fifo_cnt_masked <<= Mux(io.branch_i, U(0), io.fifo_cnt_i)

        # FSM (state_q, next_state) to control OBI A channel signals


    return PREFETCH_CONTROLLER()
