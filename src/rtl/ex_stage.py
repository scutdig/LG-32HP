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
   File Name: ex_stage.py
   Description: Execution stage: Hosts ALU and MAC unit
                ALU: computes additions/subtractions/comparisons
                MULT: computes normal multiplications
"""
from pyhcl import *
from src.include.pkg import *
from src.rtl.alu import *
from src.rtl.mult import *


def ex_stage():
    class EX_STAGE(Module):
        io = IO(
            # ALU signals from ID stage
            alu_operator_i=Input(U.w(ALU_OP_WIDTH)),
            alu_operand_a_i=Input(U.w(32)),
            alu_operand_b_i=Input(U.w(32)),
            alu_operand_c_i=Input(U.w(32)),
            alu_en_i=Input(Bool),

            # Multiplier signals
            mult_operator_i=Input(U.w(MUL_OP_WIDTH)),
            mult_operand_a_i=Input(U.w(32)),
            mult_operand_b_i=Input(U.w(32)),
            mult_operand_c_i=Input(U.w(32)),
            mult_en_i=Input(Bool),
            mult_sel_subword_i=Input(Bool),
            mult_signed_mode_i=Input(U.w(2)),
            mult_imm_i=Input(U.w(5)),
            mult_multicycle_o=Output(Bool),

            lsu_en_i=Input(Bool),
            lsu_rdata_i=Input(U.w(32)),

            # Input from ID stage
            branch_in_ex_i=Input(Bool),
            regfile_alu_waddr_i=Input(U.w(6)),
            regfile_alu_we_i=Input(Bool),

            # Directly passed through to WB stage, not used in EX
            regfile_we_i=Input(Bool),
            regfile_waddr_i=Input(U.w(6)),

            # CSR access
            csr_access_i=Input(Bool),
            csr_rdata_i=Input(U.w(32)),

            # Output of EX stage pipeline
            regfile_waddr_wb_o=Output(U.w(6)),
            regfile_alu_we_fw_o=Output(Bool),
            regfile_alu_wdata_fw_o=Output(U.w(32)),

            # To IF: Jump and branch target and decision
            jump_target_o=Output(U.w(32)),
            branch_decision_o=Output(Bool),

            # Stall Control
            is_decoding_i=Input(Bool),
            lsu_ready_ex_i=Input(Bool),
            lsu_err_i=Input(Bool),

            ex_ready_o=Output(Bool),
            ex_valid_i=Output(Bool),
            wb_ready_i=Input(Bool)
        )
        alu_i = alu()
        mult_i = mult()

        alu_result = Wire(U.w(32))
        mult_result = Wire(U.w(32))
        alu_cmp_result = Wire(Bool)

        regfile_we_lsu = Wire(Bool)
        regfile_waddr_lsu = Wire(U.w(6))

        wb_contention = Wire(Bool)
        wb_contention_lsu = Wire(Bool)

        alu_ready = Wire(Bool)
        mult_ready = Wire(Bool)

        # ALU write port mux
        wb_contention <<= U(0)

        io.regfile_alu_we_fw_o <<= io.regfile_alu_we_i
        io.regfile_alu_waddr_fw_o <<= io.regfile_alu_waddr_i
        with when(io.alu_en_i):
            io.regfile_alu_wdata_fw_o <<= alu_result
        with elsewhen(io.mult_en_i):
            io.regfile_alu_wdata_fw_o <<= mult_result
        with elsewhen(io.csr_access_i):
            io.regfile_alu_wdata_fw_o <<= io.csr_rdata_i

        # LSU write port mux
        io.regfile_we_wb_o <<= Bool(False)
        io.regfile_waddr_wb_o <<= regfile_waddr_lsu
        io.regfile_wdata_wb_o <<= io.lsu_rdata_i
        wb_contention_lsu <<= Bool(False)

        with when(regfile_we_lsu):
            io.regfile_we_wb_o <<= Bool(True)

        # Branch handling
        io.branch_decision_o <<= alu_cmp_result
        io.jump_target_o <<= io.alu_operand_c_i

        ##################################################################################
        # ALU
        ##################################################################################

        alu_i.io.enable_i <<= io.alu_en_i
        alu_i.io.operator_i <<= io.alu_operator_i
        alu_i.io.operand_a_i <<= io.alu_operand_a_i
        alu_i.io.operand_b_i <<= io.alu_operand_b_i
        alu_i.io.operand_c_i <<= io.alu_operand_c_i

        alu_result <<= alu_i.io.result_o
        alu_cmp_result <<= alu_i.io.comparison_result_o

        alu_ready <<= alu_i.io.alu_ready
        alu_i.io.ex_ready_i <<= io.ex_ready_o

        ##################################################################################
        # Multiplier
        ##################################################################################
        mult_i.io.enable_i <<= io.mult_en_i
        mult_i.io.operator_i <<= io.mult_operator_i

        mult_i.io.short_subword_i <<= io.mult_sel_subword_i
        mult_i.io.short_signed_i <<= io.mult_signed_mode_i

        mult_i.io.op_a_i <<= io.mult_operand_a_i
        mult_i.io.op_b_i <<= io.mult_operand_b_i
        mult_i.io.op_c_i <<= io.mult_operand_c_i
        mult_i.io.imm_i <<= io.mult_imm_i

        mult_result <<= mult_i.io.result_o

        io.mult_multicycle_o <<= mult_i.io.multcycle_o
        mult_ready <<= mult_i.io.ready_o
        mult_i.io.ex_ready_i <<= io.ex_ready_o

    return EX_STAGE()
