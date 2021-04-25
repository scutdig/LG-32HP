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
from src.rtl.alu_div import *
from src.rtl.popcnt import *


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
        alu_div_i = alu_div()
        popcnt_i = popcnt()

        operand_a_rev = Wire(U.w(32))
        operand_a_neg = Wire(U.w(32))
        operand_a_neg_rev = Wire(U.w(32))

        operand_a_neg <<= ~io.operand_a_i

        # Bit reverse operand a for left shifts and bit counting
        # Generate reverse array
        # op_a_rev_arr = [io.operand_a_i[31-i] for i in range(32)]
        op_a_rev_arr = []
        for i in range(32):
            op_a_rev_arr.append(io.operand_a_i[i])
        operand_a_rev <<= CatBits(*op_a_rev_arr)

        # Bit reverse operand_a_neg for left shifts and bit counting
        op_a_neg_rev_arr = []
        for i in range(32):
            op_a_neg_rev_arr.append(operand_a_neg[i])
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

        # Normalization stage
        adder_round_value = Wire(U.w(32))
        adder_round_result = Wire(U.w(32))

        adder_round_value <<= U(0)
        adder_round_result <<= adder_result + adder_round_value

        ##################################################################################
        # Shift
        ##################################################################################

        shift_left = Wire(Bool)
        shift_use_round = Wire(Bool)
        shift_arithmetic = Wire(Bool)

        shift_amt_left = Wire(U.w(32))          # Amount of shift, if to the left
        shift_amt = Wire(U.w(32))               # Amount of shift, to the right
        shift_amt_int = Wire(U.w(32))           # Amount of shift, used for the actual shifters
        shift_amt_norm = Wire(U.w(32))          # Amount of shift, used for normalization
        shift_op_a = Wire(U.w(32))              # Input of the shifter
        shift_result = Wire(U.w(32))
        shift_right_result = Wire(U.w(32))
        shift_left_result = Wire(U.w(32))
        clpx_shift_ex = Wire(U.w(16))

        # Shifter is also used for preparing operand for division
        shift_amt <<= Mux(div_valid, div_shift, io.operand_b_i)

        shift_amt_left <<= shift_amt

        # ALU_FL1 and ALU_CLB are used for the bit counting ops later
        shift_left <<= (io.operator_i == ALU_SLL) | (io.operator_i == ALU_BINS) | \
                       (io.operator_i == ALU_FL1) | (io.operator_i == ALU_CLB)  | \
                       (io.operator_i == ALU_DIV) | (io.operator_i == ALU_DIVU) | \
                       (io.operator_i == ALU_REM) | (io.operator_i == ALU_REMU) | \
                       (io.operator_i == ALU_BREV)

        shift_use_round <<= (io.operator_i == ALU_ADD)  | (io.operator_i == ALU_SUB)  | \
                            (io.operator_i == ALU_ADDR)  | (io.operator_i == ALU_SUBR)  | \
                            (io.operator_i == ALU_ADDU)  | (io.operator_i == ALU_SUBU)  | \
                            (io.operator_i == ALU_ADDUR) | (io.operator_i == ALU_SUBUR)

        shift_arithmetic <<= (io.operator_i == ALU_SRA)  | (io.operator_i == ALU_BEXT) | \
                             (io.operator_i == ALU_ADD)  | (io.operator_i == ALU_SUB)  | \
                             (io.operator_i == ALU_ADDR) | (io.operator_i == ALU_SUBR)

        # Choose the bit reversed or the normal input for shift operand a
        shift_op_a <<= Mux(shift_left, operand_a_rev, Mux(shift_use_round, adder_round_result, io.operand_a_i))
        # In our implement, we never round the result
        shift_amt_int <<= shift_amt

        # Right shifts
        shift_op_a_32 = Wire(U.w(64))
        shift_op_tmp = Wire(U.w(64))
        ari_lst = []                # Arithmetic shift list
        for i in range(32):
            ari_lst.append(shift_op_a[31])
        not_ror = Mux(shift_arithmetic, CatBits(*ari_lst, shift_op_a), CatBits(U.w(32)(0), shift_op_a))
        shift_op_a_32 <<= Mux(io.operator_i == ALU_ROR, CatBits(shift_op_a, shift_op_a), not_ror)

        shift_right_result <<= shift_op_a_32 >> shift_amt_int[4:0]

        # Bit reverse the shift_right_result for left shifts
        reverse_lst = [Wire(Bool) for _ in range(32)]
        for j in range(32):
            reverse_lst[j] <<= shift_right_result[j]
        shift_left_result <<= CatBits(*reverse_lst)

        shift_result <<= Mux(shift_left, shift_left_result, shift_right_result)

        ##################################################################################
        # Comparison
        ##################################################################################

        is_equal = Wire(U.w(4))
        is_greater = Wire(U.w(4))   # Handles both signed and unsigned forms

        # 8-bit vector comparisons, basic building blocks
        cmp_signed = Wire(U.w(4))
        is_equal_vec = Wire(Vec(4, Bool))
        is_greater_vec = Wire(Vec(4, Bool))
        operand_b_eq = Wire(U.w(32))
        # is_equal_clip = Wire(Bool)

        # second == comparator for CLIP instructions
        # We dont need that support
        operand_b_eq <<= operand_b_neg

        cmp_signed <<= U(0)
        # Some ALU operations that we dont support
        with when((io.operator_i == ALU_GTS) | (io.operator_i == ALU_GES) | (io.operator_i == ALU_LTS) |
                  (io.operator_i == ALU_LES) | (io.operator_i == ALU_SLTS) | (io.operator_i == ALU_SLETS) |
                  (io.operator_i == ALU_MIN) | (io.operator_i == ALU_MAX) | (io.operator_i == ALU_ABS) |
                  (io.operator_i == ALU_CLIP) | (io.operator_i == ALU_CLIPU)):
            cmp_signed <<= U.w(4)(0b1000)

        for i in range(4):
            is_equal_vec[i] <<= io.operand_a_i[8*i+7:8*i] == io.operand_b_i[8*i+7:8*i]
            is_greater_vec[i] <<= (CatBits(io.operand_a_i[8*i+7] & cmp_signed[i], io.operand_a_i[8*i+7:8*i]).to_sint() > \
                                CatBits(io.operand_b_i[8*i+7] & cmp_signed[i], io.operand_b_i[8*i+7:8*i]).to_sint()).to_bool()

        # Generate the real equal and greater than signals that take the vector mode into account
        # Always 32-bit mode
        is_equal_s = is_equal_vec[3] & is_equal_vec[2] & is_equal_vec[1] & is_equal_vec[0]
        is_equal_lst = []
        for i in range(4):
            is_equal_lst.append(is_equal_s)
        is_equal <<= CatBits(*is_equal_lst)
        is_greater_s = is_greater_vec[3] | (is_equal_vec[3] & (is_greater_vec[2]
                                            | (is_equal_vec[2] & (is_greater_vec[1]
                                                | (is_equal_vec[1] & (is_greater_vec[0]))))))
        is_greater_lst = []
        for i in range(4):
            is_greater_lst.append(is_greater_s)
        is_greater <<= CatBits(*is_greater_lst)

        # Generate comparison result
        cmp_result = Wire(U.w(4))
        cmp_result <<= is_equal

        cmp_result <<= LookUpTable(io.operator_i, {
            ALU_EQ: is_equal,
            ALU_NE: ~is_equal,
            ALU_GTS: is_greater,
            ALU_GTU: is_greater,
            ALU_GES: is_greater | is_equal,
            ALU_GEU: is_greater | is_equal,
            ALU_LTS: ~(is_greater | is_equal),
            ALU_SLTS: ~(is_greater | is_equal),
            ALU_LTU: ~(is_greater | is_equal),
            ALU_SLTU: ~(is_greater | is_equal),
            ALU_SLETS: ~is_greater,
            ALU_SLETU: ~is_greater,
            ALU_LES: ~is_greater,
            ALU_LEU: ~is_greater,
            ...: is_equal
        })

        io.comparison_result_o <<= cmp_result[3]

        # No min/max/abs support
        # No Clip, Shuffle, Bit Manipulation

        ##################################################################################
        # DIV / REM
        ##################################################################################

        result_div = Wire(U.w(32))
        div_ready, div_signed, div_op_a_signed = [Wire(Bool) for _ in range(3)]
        div_shift_int = Wire(U.w(6))

        div_signed <<= io.operator_i[0]

        div_op_a_signed <<= io.operand_a_i[31] & div_signed

        div_shift_int <<= U.w(6)(31)
        div_shift <<= div_shift_int + Mux(div_op_a_signed, U(0), U(1))

        div_valid <<= io.enable_i & ((io.operator_i == ALU_DIV) | (io.operator_i == ALU_DIVU) |
                                     (io.operator_i == ALU_REM) | (io.operator_i == ALU_REMU))

        # Inputs A and B are swapped

        alu_div_i.io.OpA_DI <<= io.operand_b_i
        alu_div_i.io.OpB_DI <<= shift_left_result
        alu_div_i.io.OpBShift_DI <<= div_shift

        cnt_result = Wire(U.w(6))

        popcnt_i.io.in_i <<= io.operand_a_i
        cnt_result <<= popcnt_i.io.result_o
        alu_div_i.io.OpBIsZero_SI <<= cnt_result == U(0)

        alu_div_i.io.OpBSign_SI <<= div_op_a_signed
        alu_div_i.io.OpCode_SI <<= io.operator_i[1:0]

        result_div <<= alu_div_i.io.Res_DO

        alu_div_i.io.InVld_SI <<= div_valid
        alu_div_i.io.OutRdy_SI <<= io.ex_ready_i
        div_ready <<= alu_div_i.io.OutVld_SO

        ##################################################################################
        # Result Mux
        ##################################################################################
        io.result_o <<= U(0)

        with when(io.operator_i == ALU_AND):
            io.result_o <<= io.operand_a_i & io.operand_b_i
        with elsewhen(io.operator_i == ALU_OR):
            io.result_o <<= io.operand_a_i | io.operand_b_i
        with elsewhen(io.operator_i == ALU_XOR):
            io.result_o <<= io.operand_a_i ^ io.operand_b_i
        with elsewhen((io.operator_i == ALU_ADD) | (io.operator_i == ALU_ADDR) | (io.operator_i == ALU_ADDU) |
                      (io.operator_i == ALU_ADDUR) | (io.operator_i == ALU_SUB) | (io.operator_i == ALU_SUBR) |
                      (io.operator_i == ALU_SUBU) |(io.operator_i == ALU_SUBUR) | (io.operator_i == ALU_SLL) |
                      (io.operator_i == ALU_SRL) | (io.operator_i == ALU_SRA) | (io.operator_i == ALU_ROR)):
            io.result_o <<= shift_result
        with elsewhen((io.operator_i == ALU_EQ) | (io.operator_i == ALU_NE) | (io.operator_i == ALU_GTU) |
                      (io.operator_i == ALU_GEU) | (io.operator_i == ALU_LTU) | (io.operator_i == ALU_LEU) |
                      (io.operator_i == ALU_GTS) | (io.operator_i == ALU_GES) | (io.operator_i == ALU_LTS) |
                      (io.operator_i == ALU_LES)):
            cmp_res_lst0 = []
            cmp_res_lst1 = []
            cmp_res_lst2 = []
            cmp_res_lst3 = []
            for i in range(8):
                cmp_res_lst0.append(cmp_result[0])
                cmp_res_lst1.append(cmp_result[1])
                cmp_res_lst2.append(cmp_result[2])
                cmp_res_lst3.append(cmp_result[3])
            io.result_o <<= CatBits(*cmp_res_lst3, *cmp_res_lst2, *cmp_res_lst1, *cmp_res_lst0)
        with elsewhen((io.operator_i == ALU_SLTS) | (io.operator_i == ALU_SLTU) | (io.operator_i == ALU_SLETS) |
                      (io.operator_i == ALU_SLETU)):
            io.result_o <<= CatBits(U.w(31)(0), io.comparison_result_o)
        with elsewhen((io.operator_i == ALU_DIV) | (io.operator_i == ALU_DIVU) | (io.operator_i == ALU_REM) |
                      (io.operator_i == ALU_REMU)):
            io.result_o <<= result_div

        io.ready_o <<= div_ready

    return ALU()


if __name__ == '__main__':
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(alu()), "alu.fir"))
