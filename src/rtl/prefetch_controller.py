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
            trans_ready_i=Input(Bool),      # Transaction reuqest ready
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

    return PREFETCH_CONTROLLER()
