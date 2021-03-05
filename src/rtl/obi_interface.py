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
   File Name: obi_interface.py
   Description: "Open Bus Interface adapter. Translates transaction request
                on the trans_* interface into an OBI A channel transfer.
                The OBI R channel transfer translated (i.e. passed on) as
                a transaction response on the resp_* interface.

                This adapter does not limit the number of outstanding
                OBI transactions in any way." -- original RIS5Y annotation

                Current OBI interface is Master side.
"""
from pyhcl import *


def obi_interface(TRANS_STABLE=0):
    """
        args:
            TRANS_STABLE: TODO: missing description here
    """

    class OBI_INTERFACE(Module):
        # FSM state definition
        TRANSPARENT = U.w(1)(0)
        REGISTERED = U.w(1)(1)

        io = IO(
            # Transaction request interface
            trans_valid_i=Input(Bool),
            trans_ready_o=Output(Bool),
            trans_addr_i=Input(U.w(32)),
            trans_we_i=Input(Bool),
            trans_be_i=Input(U.w(4)),
            trans_wdata_i=Input(U.w(32)),
            trans_atop_i=Input(U.w(6)),         # Future proof addition, no use

            # Transaction response interface
            resp_valid_o=Output(Bool),
            resp_rdata_o=Output(U.w(32)),
            resp_err_o=Output(Bool),

            # OBI interface
            obi_req_o=Output(Bool),
            obi_gnt_i=Input(Bool),
            obi_addr_o=Output(U.w(32)),
            obi_we_o=Output(Bool),
            obi_be_o=Output(U.w(4)),
            obi_wdata_o=Output(U.w(32)),
            obi_atop_o=Output(U.w(6)),
            obi_rdata_i=Input(U.w(32)),
            obi_rvalid_i=Input(Bool),
            obi_err_i=Input(Bool)
        )

        state_q = RegInit(U.w(1)(0))   # Reset state: TRANSPARENT
        next_state = Wire(U.w(1))

        ##################################################################################
        # OBI R Channel
        ##################################################################################

        # The OBI R channel signals are passed on directly on the transaction response
        # interface (resp_*). It is assumed that the consumer of the transaction response
        # is always receptive when resp_valid_o == 1 (otherwise a response would get dropped)

        io.resp_valid_o <<= io.obi_rvalid_i
        io.resp_rdata_o <<= io.obi_rdata_i
        io.resp_err_o <<= io.obi_err_i

        ##################################################################################
        # OBI A Channel
        ##################################################################################

        if TRANS_STABLE == 1:
            # If the incoming transaction itself is stable, then it satisfies the OBI protocol
            # and signals can be passed to/from OBI directly.
            io.obi_req_o <<= io.trans_valid_i
            io.obi_addr_o <<= io.trans_addr_i
            io.obi_we_o <<= io.trans_we_i
            io.obi_be_o <<= io.trans_be_i
            io.obi_wdata_o <<= io.trans_wdata_i
            io.obi_atop_o <<= io.trans_atop_i

            io.trans_ready_o <<= io.obi_gnt_i

            # FSM not used
            state_q <<= TRANSPARENT
            next_state <<= TRANSPARENT
        else:
            # OBI A channel registers (to keep A channel stable)
            obi_addr_q = RegInit(U.w(32)(0))
            obi_we_q = RegInit(Bool(False))
            obi_be_q = RegInit(U.w(4)(0))
            obi_wdata_q = RegInit(U.w(32)(0))
            obi_atop_q = RegInit(U.w(6)(0))

            # If the incoming transaction itself if not stable; use an FSM to make sure that
            # the OBI address phase signals are kept stable during non-granted requests.

            ##################################################################################
            # OBI FSM
            ##################################################################################

            # FSM (state_q, next_state) to control OBI A channel signals
            next_state <<= state_q

            with when(state_q == TRANSPARENT):
                # Default (TRANSPARENT) state. Transaction requests are passed directly onto the OBI A channel.
                with when(io.obi_req_o & (~io.obi_gnt_i)):
                    # OBI request not immediately granted. (Ready to accept address transfer, condition:
                    # Address transfer is accepted on rising clk with req=1 and gnt=1.) Move to REGISTERED state
                    # such that OBI address phase signals can be kept stable while the transaction request (trans_*)
                    # can possibly change.
                    next_state <<= REGISTERED
                # End case: TRANSPARENT
            with elsewhen(state_q == REGISTERED):
                # Registered state. OBI address phase signals are kept stable (driven from registers).
                with when(io.obi_gnt_i):
                    # Received grant. Move back to TRANSPARENT state such that next transaction request can be passed on
                    next_state <<= TRANSPARENT
                # End case: REGISTERED

            with when(state_q == TRANSPARENT):
                io.obi_req_o <<= io.trans_valid_i   # Do not limit number of outstanding transactions
                io.obi_addr_o <<= io.trans_addr_i
                io.obi_we_o <<= io.trans_we_i
                io.obi_be_o <<= io.trans_be_i
                io.obi_wdata_o <<= io.trans_wdata_i
                io.obi_atop_o <<= io.trans_atop_i
            with otherwise():
                # state_q == REGISTERED
                io.obi_req_o <<= U.w(1)(1)      # Kept request signal stable
                io.obi_addr_o <<= obi_addr_q
                io.obi_we_o <<= obi_we_q
                io.obi_be_o <<= obi_be_q
                io.obi_wdata_o <<= obi_wdata_q
                io.obi_atop_o <<= obi_atop_q

            ##################################################################################
            # Registers
            ##################################################################################

            state_q <<= next_state
            with when((state_q == TRANSPARENT) & (next_state == REGISTERED)):
                obi_addr_q <<= io.obi_addr_o
                obi_we_q <<= io.obi_we_o
                obi_be_q <<= io.obi_be_o
                obi_wdata_q <<= io.obi_wdata_o
                obi_atop_q <<= io.obi_atop_o

            # Always ready to accept a new transfer requests when previous A channel
            # transfer has been granted. Note that the obi interface does not limit
            # the number of outstanding transactions in any way.
            io.trans_ready_o <<= state_q == TRANSPARENT

    return OBI_INTERFACE()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(obi_interface()), "obi_interface.fir"))
