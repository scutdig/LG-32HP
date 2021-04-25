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
   Date: 2021-03-08
   File Name: register_file_ff.py
   Description: "Register file with 31x 32 bit wide registers. Register 0
                is fixed to 0. This register file is based on flip-flops.
                Also supports the fp-register file now if FPU=1
                If PULP_ZFINX is 1, floating point operations take values
                from the X register file." -- Original RI5SY annotation
"""
from pyhcl import *


def register_file(ADDR_WIDTH=5, DATA_WIDTH=32):
    # In our implementations, we currently do not implement floating point units
    # So FPU, PULP_ZFINX = 0

    # Number of integer registers
    NUM_WORDS = pow(2, ADDR_WIDTH - 1)
    NUM_TOT_WORDS = NUM_WORDS

    class REGISTER_FILE(Module):
        io = IO(
            scan_cg_en_i=Input(Bool),

            # Read port R1
            raddr_a_i=Input(U.w(ADDR_WIDTH)),
            rdata_a_o=Output(U.w(DATA_WIDTH)),

            # Read port R2
            raddr_b_i=Input(U.w(ADDR_WIDTH)),
            rdata_b_o=Output(U.w(DATA_WIDTH)),

            # Read port R3
            raddr_c_i=Input(U.w(ADDR_WIDTH)),
            rdata_c_o=Output(U.w(DATA_WIDTH)),

            # Write port W1
            waddr_a_i=Input(U.w(ADDR_WIDTH)),
            wdata_a_i=Input(U.w(DATA_WIDTH)),
            we_a_i = Input(U.w(1)),

            # Write port W2
            waddr_b_i=Input(U.w(ADDR_WIDTH)),
            wdata_b_i=Input(U.w(DATA_WIDTH)),
            we_b_i = Input(U.w(1))
        )

        # Integer register file
        mem = Reg(Vec(NUM_WORDS, U.w(DATA_WIDTH)))

        # Masked write addresses
        waddr_a = Wire(U.w(NUM_WORDS))
        waddr_b = Wire(U.w(NUM_WORDS))

        # Write enable signals for all registers
        we_a_dec = Wire(U.w(NUM_TOT_WORDS))
        we_b_dec = Wire(U.w(NUM_TOT_WORDS))

        ##################################################################################
        # -- READ : Read Address Decoder RAD
        ##################################################################################
        io.rdata_a_o <<= mem[io.raddr_a_i[4:0]]
        io.rdata_b_o <<= mem[io.raddr_b_i[4:0]]
        io.rdata_c_o <<= mem[io.raddr_c_i[4:0]]

        ##################################################################################
        # -- WRITE: Write Address Decoder (WAD), combinartorial process
        ##################################################################################

        # Mask top bit of write address to disable fp regfile
        waddr_a <<= U.w(NUM_TOT_WORDS)(1) << io.waddr_a_i
        waddr_b <<= U.w(NUM_TOT_WORDS)(1) << io.waddr_b_i

        # Mask
        we_a_dec <<= Mux(io.we_a_i, U.w(NUM_TOT_WORDS)(pow(2, NUM_TOT_WORDS)-1) & waddr_a, U(0))
        we_b_dec <<= Mux(io.we_b_i, U.w(NUM_TOT_WORDS)(pow(2, NUM_TOT_WORDS)-1) & waddr_b, U(0))

        ##################################################################################
        # -- WRITE: Write operation
        ##################################################################################
        # Ro is nil
        mem[0] <<= U(0)

        # Loop from 1 to NUM_WORDS-1 as R0 is nil
        for i in range(1, NUM_WORDS):
            with when(Module.reset):
                mem[i] <<= U.w(32)(0)
            with otherwise():
                with when(we_b_dec[i] == U.w(1)(1)):
                    mem[i] <<= io.wdata_b_i
                with elsewhen(we_a_dec[i] == U.w(1)(1)):
                    mem[i] <<= io.wdata_a_i

    return REGISTER_FILE()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(register_file()), "register_file_ff.fir"))
