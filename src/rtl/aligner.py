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

   Author Name:
   Date:
   File Name:
   Description:
"""

from pyhcl import *


def aligner():
    class ALIGNER(Module):
        # aligner stage local parameter
        ALIGNED32 = U.w(3)(0)
        MISALIGNED32 = U.w(3)(1)
        MISALIGNED16 = U.w(3)(2)
        BRANCH_MISALIGNED = U.w(3)(3)
        WAIT_VALID_BRANCH = U.w(3)(4)

        io = IO(
            fetch_valid_i=Input(Bool),
            aligner_ready_o=Output(Bool),  # prevents overwriting the fetched instruction

            if_valid_i=Input(Bool),

            fetch_rdata_i=Input(U.w(32)),
            instr_aligned_o=Output(U.w(32)),  # aligned instruction
            instr_valid_o=Output(Bool),

            branch_addr_i=Input(U.w(32)),
            branch_i=Input(Bool),  # Asserted if we are branching/jumping now

            pc_o=Output(U.w(32))
        )
        r_instr_h = Reg(U.w(16))  # store the upper 16bits
        state = Reg(U.w(3))
        pc_q = Reg(U.w(32))  # the current pc
        pc_plus4 = Wire(U.w(32))
        pc_plus2 = Wire(U.w(32))
        aligner_ready_q = Reg(U.w(1))
        update_state = Wire(U.w(1))  # Asserted if the state should change
        io.pc_o <<= pc_q

        pc_plus2 <<= pc_q + U(2)
        pc_plus4 <<= pc_q + U(4)
        # default outputs
        io.instr_valid_o <<= io.fetch_valid_i
        io.instr_aligned_o <<= io.fetch_rdata_i
        io.aligner_ready_o <<= U(1)

        # output value
        with when(state == ALIGNED32):
            with when(io.fetch_rdata_i[1:0] == U.w(2)(3)):
                io.instr_aligned_o <<= io.fetch_rdata_i
                update_state <<= io.fetch_valid_i & io.if_valid_i
            with otherwise():
                io.instr_aligned_o <<= io.fetch_rdata_i
                update_state <<= io.fetch_valid_i & io.if_valid_i
        with elsewhen(state == MISALIGNED32):
            with when(r_instr_h[1:0] == U.w(2)(3)):
                io.instr_aligned_o <<= CatBits(io.fetch_rdata_i[15:0], r_instr_h[15:0])
                update_state <<= io.fetch_valid_i & io.if_valid_i
            with otherwise():
                io.instr_aligned_o <<= CatBits(io.fetch_rdata_i[31:16], r_instr_h[15:0])
                io.instr_valid_o <<= U(1)
                io.aligner_ready_o <<= ~io.fetch_valid_i
                update_state <<= io.if_valid_i
        with elsewhen(state == MISALIGNED16):
            io.instr_valid_o <<= ~aligner_ready_q | io.fetch_valid_i
            with when(io.fetch_rdata_i[1:0] == U.w(2)(3)):
                io.instr_aligned_o <<= io.fetch_rdata_i
                update_state <<= (~aligner_ready_q | io.fetch_valid_i) & io.if_valid_i
            with otherwise():
                io.instr_aligned_o <<= io.fetch_rdata_i
                update_state <<= (~aligner_ready_q | io.fetch_valid_i) & io.if_valid_i
        with elsewhen(state == BRANCH_MISALIGNED):
            with when(io.fetch_rdata_i[17:16] == U.w(2)(3)):
                io.instr_valid_o <<= U(1)
                io.instr_aligned_o <<= io.fetch_rdata_i
                update_state <<= io.fetch_valid_i & io.if_valid_i
            with otherwise():
                io.instr_aligned_o <<= CatBits(io.fetch_rdata_i[31:16], io.fetch_rdata_i[31:16])
                update_state <<= io.fetch_valid_i & io.if_valid_i
        with otherwise():
            io.instr_valid_o <<= io.fetch_valid_i
            io.instr_aligned_o <<= io.fetch_rdata_i
            io.aligner_ready_o <<= U(1)
            update_state <<= U(0)

        with when(io.branch_i):
            update_state <<= U(1)

        with when(Module.reset):
            state <<= ALIGNED32
            r_instr_h <<= U(0)
            pc_q <<= U(0)
            aligner_ready_q <<= U(0)

        # state change
        with when(update_state):
            r_instr_h <<= io.fetch_rdata_i[31:16]
            aligner_ready_q <<= io.aligner_ready_o
            with when(io.branch_i):
                # JUMP, BRANCH, SPECIAL JUMP control
                pc_q <<= io.branch_addr_i
                state <<= Mux(io.branch_addr_i[1], BRANCH_MISALIGNED, ALIGNED32)
            with when(state == ALIGNED32):
                with when(io.fetch_rdata_i[1:0] == U.w(2)(3)):
                    state <<= ALIGNED32
                    pc_q <<= pc_plus4
                with otherwise():
                    state <<= MISALIGNED32
                    pc_q <<= pc_plus2
            with elsewhen(state == MISALIGNED32):
                with when(r_instr_h[1:0] == U.w(2)(3)):
                    state <<= MISALIGNED32
                    pc_q <<= pc_plus4
                with otherwise():
                    state <<= MISALIGNED16
                    pc_q <<= pc_plus2
            with elsewhen(state == MISALIGNED16):
                with when(io.fetch_rdata_i[1:0] == U.w(2)(3)):
                    state <<= ALIGNED32
                    pc_q <<= pc_plus4
                with otherwise():
                    state <<= MISALIGNED32
                    pc_q <<= pc_plus2
            with elsewhen(state == BRANCH_MISALIGNED):
                with when(io.fetch_rdata_i[17:16] == U.w(2)(3)):
                    state <<= MISALIGNED32
                    pc_q <<= pc_q
                with otherwise():
                    state <<= ALIGNED32
                    pc_q <<= pc_plus2

    return ALIGNER()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(aligner()), "aligner.fir"))
