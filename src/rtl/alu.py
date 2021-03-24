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
   Date: 2021-03-18
   File Name: alu.py
   Description: Arithmetic logic unit of the pipeline processor
"""
from pyhcl import *
from src.include.pkg import *


def alu():
    class ALU(Module):
        io = IO(
            enable_i=Input(Bool),
            operator_i=Input(U.w(ALU_OP_WIDTH)),
            operand_a_i=Input(U.w(32)),
            operand_b_i=Input(U.w(32)),
            operand_c_i=Input(U.w(32)),

            # Our currently implementation has no vector/bit manipulation support
            # vector_mode_i, bmask_a/b_i, imm_vec_ext_i deprecated

            # is_clpx_i, is_subrot_i, clpx_shift_i deprecated

            result_o=Output(U.w(32)),
            comparison_result_o=Output(Bool),

            ready_o=Output(Bool),
            ex_ready_i=Input(Bool)
        )

        operand_a_rev = Wire(U.w(32))
        operand_a_neg = Wire(U.w(32))
        operand_a_neg_rev = Wire(U.w(32))

        operand_a_neg <<= ~io.operand_a_i

        # Bit reverse operand a for left shifts and bit counting
        # Generate reverse array
        # op_a_rev_arr = [io.operand_a_i[31-i] for i in range(32)]
        op_a_rev_arr = []
        for i in range(32):
            op_a_rev_arr.append(io.operand_a_i[31-i])
        operand_a_rev <<= CatBits(*op_a_rev_arr)

        # Bit reverse operand_a_neg for left shifts and bit counting
        op_a_neg_rev_arr = []
        for i in range(32):
            op_a_neg_rev_arr.append(op_a_neg_rev_arr[31-i])
        operand_a_neg_rev <<= CatBits(*op_a_neg_rev_arr)

        operand_b_neg = Wire(U.w(32))
        operand_b_neg <<= ~io.operand_b_i

        div_shift = Wire(U.w(6))
        div_valid = Wire(Bool)

        ##################################################################################
        # Partitioned Adder
        ##################################################################################
        adder_op_b_negate = Wire(Bool)
        adder_op_a, adder_op_b = [Wire(U.w(32)) for _ in range(2)]
        adder_in_a, adder_in_b = [Wire(U.w(36)) for _ in range(2)]
        adder_result = Wire(U.w(32))
        adder_result_expanded = Wire(U.w(36))

        adder_op_b_negate <<= (io.operator_i == ALU_SUB) | (io.operator_i == ALU_SUBR) | \
                              (io.operator_i == ALU_SUBU) | (io.operator_i == ALU_SUBUR)

        # Prepare operand a
        adder_op_a <<= Mux(io.operator_i == ALU_ABS, operand_a_neg, io.operand_a_i)

        # Prepare operand b
        adder_op_b <<= Mux(adder_op_b_negate, operand_b_neg, io.operand_b_i)

        # Prepare carry
        adder_in_a <<= CatBits(adder_op_a[31:24], U.w(1)(1), adder_op_a[23:16], U.w(1)(1),
                               adder_op_a[15:8], U.w(1)(1), adder_op_a[7:0], U.w(1)(1))
        adder_in_b <<= CatBits(adder_op_b[31:24], U.w(1)(0), adder_op_b[23:16], U.w(1)(0),
                               adder_op_b[15:8], U.w(1)(0), adder_op_b[7:0],
                               Mux(adder_op_b_negate | (io.operator_i == ALU_ABS) | (io.operator_i == ALU_CLIP),
                                   U.w(1)(1), U.w(1)(0)))

        # Actual adder
        adder_result_expanded <<= (adder_in_a.to_sint() + adder_in_b.to_sint()).to_uint()
        adder_result <<= CatBits(adder_result_expanded[35:28], adder_result_expanded[26:19],
                                 adder_result_expanded[17:10], adder_result_expanded[8:1])

        # Normalization stage deprecated

    return ALU()
