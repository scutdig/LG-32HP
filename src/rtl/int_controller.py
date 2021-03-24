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
   Date: 2021-03-14
   File Name: int_controller.py
   Description: "Interrupt Controller of the pipelined processor" -- original RI5CY annotation
"""
from pyhcl import *
from src.include.pkg import *


def int_controller(PULP_SECURE=0):
    class INT_CONTROLLER(Module):
        io = IO(
            # External interrupt lines
            irq_i=Input(U.w(32)),           # Level-triggered interrupt inputs
            irq_sec_i=Input(Bool),          # Interrupt secure bit from EU

            # To controller
            irq_req_ctrl_o=Output(Bool),
            irq_sec_ctrl_o=Output(Bool),
            irq_id_ctrl_o=Output(U.w(5)),
            irq_wu_ctrl_o=Output(Bool),

            # To/from cs_regsiters
            mie_bypass_i=Input(U.w(32)),    # MIE CSR (bypass)
            mip_o=Output(U.w(32)),          # MIP CSR
            m_ie_i=Input(Bool),             # Interrupt enable bit from CSR (M mode)
            u_ie_i=Input(Bool),             # Interrupt enable bit from CSR (U mode)
            current_priv_lvl_i=Input(U.w(PRIV_SEL_WIDTH))
        )

        global_irq_enable = Wire(Bool)
        irq_local_qual = Wire(U.w(32))
        irq_q = RegInit(U.w(32)(0))
        irq_sec_q = RegInit(Bool(False))

        # Register all interrupt inputs (on gated clock). The wake-up logic will
        # observe irq_i as well, but in all other places irq_q will be used to
        # avoid timing paths from irq_i to instr_*_o
        irq_q <<= io.irq_i & IRQ_MASK
        irq_sec_q <<= io.irq_sec_i

        # MIP CSR
        io.mip_o <<= irq_q

        # Qualify registered IRQ with MIE CSR to compute locally enabled IRQs
        irq_local_qual <<= irq_q & io.mie_bypass_i

        # Wake-up signal based on unregistered IRQ such that wake-up can be caused if no clock is present
        t = io.irq_i & io.mie_bypass_i
        # Bit or reduction
        for i in range(31, -1, -1):
            io.irq_wu_ctrl_o <<= io.irq_wu_ctrl_o | t[i]

        # Global interrupt enable
        global_irq_enable <<= io.m_ie_i

        # Request to take interrupt if there is a locally enabled interrupt while interrupts are also enabled globally
        t_irq_local_qual = Wire(Bool)
        # Bit or reduction
        for i in range(31, -1, -1):
            t_irq_local_qual <<= t_irq_local_qual | irq_local_qual[i]
        io.irq_req_ctrl_o <<= t_irq_local_qual & global_irq_enable

        # Interrupt Encoder
        #
        # - sets correct id to request to ID
        # - encodes priority order

        with when(irq_local_qual[31]):
            io.irq_id_ctrl_o <<= U.w(5)(31)
        with elsewhen(irq_local_qual[30]):
            io.irq_id_ctrl_o <<= U.w(5)(30)
        with elsewhen(irq_local_qual[29]):
            io.irq_id_ctrl_o <<= U.w(5)(29)
        with elsewhen(irq_local_qual[28]):
            io.irq_id_ctrl_o <<= U.w(5)(28)
        with elsewhen(irq_local_qual[27]):
            io.irq_id_ctrl_o <<= U.w(5)(27)
        with elsewhen(irq_local_qual[26]):
            io.irq_id_ctrl_o <<= U.w(5)(26)
        with elsewhen(irq_local_qual[25]):
            io.irq_id_ctrl_o <<= U.w(5)(25)
        with elsewhen(irq_local_qual[24]):
            io.irq_id_ctrl_o <<= U.w(5)(24)
        with elsewhen(irq_local_qual[23]):
            io.irq_id_ctrl_o <<= U.w(5)(23)
        with elsewhen(irq_local_qual[22]):
            io.irq_id_ctrl_o <<= U.w(5)(22)
        with elsewhen(irq_local_qual[20]):
            io.irq_id_ctrl_o <<= U.w(5)(20)
        with elsewhen(irq_local_qual[19]):
            io.irq_id_ctrl_o <<= U.w(5)(19)
        with elsewhen(irq_local_qual[18]):
            io.irq_id_ctrl_o <<= U.w(5)(18)
        with elsewhen(irq_local_qual[17]):
            io.irq_id_ctrl_o <<= U.w(5)(17)
        with elsewhen(irq_local_qual[16]):
            io.irq_id_ctrl_o <<= U.w(5)(16)
        with elsewhen(irq_local_qual[15]):
            io.irq_id_ctrl_o <<= U.w(5)(15)
        with elsewhen(irq_local_qual[14]):
            io.irq_id_ctrl_o <<= U.w(5)(14)
        with elsewhen(irq_local_qual[13]):
            io.irq_id_ctrl_o <<= U.w(5)(13)
        with elsewhen(irq_local_qual[12]):
            io.irq_id_ctrl_o <<= U.w(5)(12)
        with elsewhen(irq_local_qual[CSR_MEIX_BIT]):
            io.irq_id_ctrl_o <<= U(CSR_MEIX_BIT)
        with elsewhen(irq_local_qual[CSR_MSIX_BIT]):
            io.irq_id_ctrl_o <<= U(CSR_MSIX_BIT)
        with elsewhen(irq_local_qual[CSR_MTIX_BIT]):
            io.irq_id_ctrl_o <<= U(CSR_MTIX_BIT)
        with elsewhen(irq_local_qual[10]):
            io.irq_id_ctrl_o <<= U.w(5)(10)
        with elsewhen(irq_local_qual[2]):
            io.irq_id_ctrl_o <<= U.w(5)(2)
        with elsewhen(irq_local_qual[6]):
            io.irq_id_ctrl_o <<= U.w(5)(6)
        with elsewhen(irq_local_qual[9]):
            io.irq_id_ctrl_o <<= U.w(5)(9)
        with elsewhen(irq_local_qual[1]):
            io.irq_id_ctrl_o <<= U.w(5)(1)
        with elsewhen(irq_local_qual[5]):
            io.irq_id_ctrl_o <<= U.w(5)(5)
        with elsewhen(irq_local_qual[8]):
            io.irq_id_ctrl_o <<= U.w(5)(8)
        with elsewhen(irq_local_qual[0]):
            io.irq_id_ctrl_o <<= U.w(5)(0)
        with elsewhen(irq_local_qual[4]):
            io.irq_id_ctrl_o <<= U.w(5)(4)
        with otherwise():
            io.irq_id_ctrl_o <<= U(CSR_MTIX_BIT)

        io.irq_sec_ctrl_o <<= irq_sec_q

    return INT_CONTROLLER()


if __name__ == '__main__':
    # TODO: Seems like here exist combinational loop here
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(int_controller()), "int_controller.fir"))
