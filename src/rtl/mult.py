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
   Date: 2021-04-08
   File Name: mult.py
   Description: Multiplier and MAC unit
"""
from pyhcl import *
from src.include.pkg import *


# FSM state
IDLE = U.w(3)(0)
STEP0 = U.w(3)(1)
STEP1 = U.w(3)(2)
STEP2 = U.w(3)(3)
FINISH = U.w(3)(4)


def mult():
    class MULT(Module):
        io = IO(
            enable_i=Input(Bool),
            operator_i=Input(U.w(MUL_OP_WIDTH)),

            # Integer and short multiplier
            short_subword_i=Input(Bool),
            short_signed_i=Input(U.w(2)),

            op_a_i=Input(U.w(32)),
            op_b_i=Input(U.w(32)),
            op_c_i=Input(U.w(32)),

            imm_i=Input(U.w(5)),

            result_o=Output(U.w(32)),

            multicycle_o=Output(Bool),
            ready_o=Output(Bool),
            ex_ready_i=Input(Bool)
        )

        ##################################################################################
        # Integer Mult
        ##################################################################################

        short_op_a = Wire(U.w(17))
        short_op_b = Wire(U.w(17))
        short_op_c = Wire(U.w(33))
        short_mul = Wire(U.w(34))
        short_mac = Wire(U.w(34))
        short_round, short_round_tmp = [Wire(U.w(32)) for _ in range(2)]
        short_result = Wire(U.w(34))

        short_mac_msb0, short_mac_msb1 = [Wire(Bool) for _ in range(2)]

        short_imm = Wire(U.w(5))
        short_subword = Wire(U.w(2))
        short_signed = Wire(U.w(2))
        short_shift_arith = Wire(Bool)
        mulh_imm = Wire(U.w(5))
        mulh_subword = Wire(U.w(2))
        mulh_signed = Wire(U.w(2))
        mulh_carry_q = RegInit(Bool(False))
        mulh_shift_arith, mulh_active, \
            mulh_save, mulh_clearcarry, mulh_ready = [Wire(Bool) for _ in range(5)]

        mulh_CS = RegInit(IDLE)
        mulh_NS = Wire(U.w(3))

        # Prepare the rounding value
        short_round_tmp <<= U.w(32)(0x00000001) << io.imm_i
        short_round <<= Mux(io.operator_i == MUL_IR, CatBits(U.w(1)(0), short_round_tmp[31:1]), U(0))

        # Perform subword selection and sign extensions
        short_op_a <<= CatBits(short_signed[0] & short_op_a[15],
                               Mux(short_subword[0], io.op_a_i[31:16], io.op_a_i[15:0]))
        short_op_b <<= CatBits(short_signed[1] & short_op_b[15],
                               Mux(short_subword[1], io.op_b_i[31:16], io.op_b_i[15:0]))
        short_op_c <<= Mux(mulh_active, CatBits(mulh_carry_q, io.op_c_i).to_sint(), short_round.to_sint()).to_uint()

        short_mul <<= (short_op_a.to_sint() * short_op_b.to_sint()).to_uint()
        short_mac <<= (short_op_c.to_sint() + short_mul.to_sint() + short_round.to_sint()).to_uint()

        # We use only short_signed_i[0] as it cannot be short_signed_i[1] 1 and short_signed_i[0] 0
        short_result <<= (CatBits(short_shift_arith & short_mac_msb1, short_shift_arith & short_mac_msb0,
                                 short_mac[31:0]).to_sint() >> short_imm).to_uint()

        # Choose between normal short multiplication operation and mulh operation
        short_imm <<= Mux(mulh_active, mulh_imm, io.imm_i)
        short_subword <<= Mux(mulh_active, mulh_subword, CatBits(io.short_subword_i, io.short_subword_i))
        short_signed <<= Mux(mulh_active, mulh_signed, io.short_signed_i)
        short_shift_arith <<= Mux(mulh_active, mulh_shift_arith, io.short_signed_i[0])

        short_mac_msb1 <<= Mux(mulh_active, short_mac[33], short_mac[31])
        short_mac_msb0 <<= Mux(mulh_active, short_mac[32], short_mac[31])

        mulh_NS          <<= mulh_CS
        mulh_imm         <<= U(0)
        mulh_subword     <<= U(0)
        mulh_signed      <<= U(0)
        mulh_shift_arith <<= U(0)
        mulh_ready       <<= U(0)
        mulh_active      <<= U(1)
        mulh_save        <<= U(0)
        mulh_clearcarry  <<= U(0)
        io.multicycle_o     <<= U(0)

        with when(mulh_CS == IDLE):
            mulh_active <<= Bool(False)
            mulh_ready <<= Bool(True)
            mulh_save <<= Bool(False)
            with when((io.operator_i == MUL_H) & io.enable_i):
                mulh_ready <<= Bool(False)
                mulh_NS <<= STEP0
        with elsewhen(mulh_CS == STEP0):
            io.multicycle_o <<= Bool(True)
            mulh_imm <<= U.w(5)(16)
            mulh_active <<= Bool(True)
            # AL * BL never overflows
            mulh_save <<= Bool(False)
            mulh_NS <<= STEP1
            # Here always a 32'b unsigned result (no carry)
        with elsewhen(mulh_CS == STEP1):
            io.multicycle_o <<= Bool(True)
            # AL*BH is signed iff B is signed
            mulh_signed <<= CatBits(io.short_signed_i[1], U.w(1)(0))
            mulh_subword <<= U.w(2)(0b10)
            mulh_save <<= Bool(True)
            mulh_shift_arith <<= Bool(True)
            mulh_NS <<= STEP2
            # Here signed 32'b + unsigned 32'b result.
            # Result is a signed 33'b
            # Store the carry as it will be used as sign extension, we do
            # not shift
        with elsewhen(mulh_CS == STEP2):
            io.multicycle_o <<= Bool(True)
            # AH*BL is signed if A is signed
            mulh_signed <<= CatBits(U.w(1)(0), io.short_signed_i[0])
            mulh_subword <<= U.w(2)(0b01)
            mulh_imm <<= U.w(5)(16)
            mulh_save <<= Bool(True)
            mulh_clearcarry <<= Bool(True)
            mulh_shift_arith <<= Bool(True)
            mulh_NS <<= FINISH
            # Here signed 32'b + signed 33'b result.
            # Result is a signed 34'b
            # We do not store the carries as the bits 34:33 are shifted back, so we clear it
        with elsewhen(mulh_CS == FINISH):
            mulh_signed <<= io.short_signed_i
            mulh_subword <<= U.w(2)(0b11)
            mulh_ready <<= Bool(True)
            with when(io.ex_ready_i):
                mulh_NS <<= IDLE

        mulh_CS <<= mulh_NS

        with when(mulh_save):
            mulh_carry_q <<= ~mulh_clearcarry & short_mac[32]
        with elsewhen(io.ex_ready_i):
            mulh_carry_q <<= Bool(False)

        # 32x32 = 32-bit multiplier
        int_op_a_msu = Wire(U.w(32))
        int_op_b_msu = Wire(U.w(32))
        int_result = Wire(U.w(32))
        int_is_msu = Wire(Bool)

        int_is_msu <<= io.operator_i == MUL_MSU32

        ext_int_is_msu = Wire(U.w(32))
        ext_int_is_msu_lst = []
        for i in range(32):
            ext_int_is_msu_lst.append(int_is_msu)
        ext_int_is_msu <<= CatBits(*ext_int_is_msu_lst)
        int_op_a_msu <<= io.op_a_i ^ ext_int_is_msu
        int_op_b_msu <<= io.op_b_i & ext_int_is_msu

        int_result <<= (io.op_c_i.to_sint() + int_op_b_msu.to_sint() + int_op_a_msu.to_sint() * io.op_b_i.to_sint()).to_uint()

        # Result Mux
        io.result_o <<= U(0)

        with when((io.operator_i == MUL_MAC32) | (io.operator_i == MUL_MSU32)):
            io.result_o <<= int_result[31:0]
        with elsewhen((io.operator_i == MUL_I) | (io.operator_i == MUL_IR) | (io.operator_i == MUL_H)):
            io.result_o <<= short_result[31:0]

        io.ready_o <<= mulh_ready

    return MULT()


if __name__ == '__main__':
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(mult()), "mult.fir"))
