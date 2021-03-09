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
   File Name: deocder.py
   Description:
"""
from pyhcl import *
from src.include.pkg import *


# PULP_XPULP, PULP_CLUSTER, A_EXTENSION, FPU, APU_WOP_CPU not used in our implementation
def decoder(PULP_SECURE=0, USE_PMP=0, DEBUG_TRIGGER_EN=1):
    class DECODER(Module):
        io = IO(
            # Signals running to/from controller
            deassert_we_i=Input(Bool),              # Deassert we, we are stalled or not active

            illegal_insn_o=Output(Bool),            # Illegal instruction encountered
            ebrk_insn_o=Output(Bool),               # Trap instruction encountered

            mret_insn_o=Output(Bool),               # Return from exception instruction encountered (M)
            uret_insn_o=Output(Bool),               # Return from exception instruction encountered (S)
            dret_insn_o=Output(Bool),               # Return from debug (M)

            mret_dec_o=Output(Bool),                # Return from exception instruction encountered (M) without deassert
            uret_dec_o=Output(Bool),                # Return from exception instruction encountered (M) without deassert
            dret_dec_o=Output(Bool),                # Return from debug (M) without deassert

            ecall_insn_o=Output(Bool),              # Environment call (syscall) instruction encountered
            wfi_o=Output(Bool),                     # Pipeline flush is requested

            fencei_insn_o=Output(Bool),             # FENCE.I instruction

            rega_used_o=Output(Bool),               # rs1 is used by current instruction
            regb_used_o=Output(Bool),               # rs2 is used by current instruction
            regc_used_o=Output(Bool),               # rs3 is used by current instruction

            # fp registers currently not used in our implementation

            # Bit manipulation currently not used in our implementation

            # From IF/ID pipeline
            instr_rdata_i=Input(U.w(32)),           # Instruction read from instr memory/cache
            illegal_c_insn_i=Input(Bool),           # Compressed instruction decode failed

            # ALU signals
            alu_en_o=Output(Bool),                  # ALU enable
            alu_operator_o=Output(U.w(ALU_OP_WIDTH)),    # ALU operation selection
            alu_op_a_mux_sel_o=Output(U.w(3)),      # Operand a selection: reg value, PC, immediate or zero
            alu_op_b_mux_sel_o=Output(U.w(3)),      # Operand b selection: reg value or immediate
            alu_op_c_mux_sel_o=Output(U.w(2)),      # Reg value or jump target
            # alu_vec_mode_o, scalar_replication_o, scalar_replication_c_o
            # are deprecated currently in our implementation
            imm_a_mux_sel_o=Output(Bool),           # Immediate selection for operand a
            imm_b_mux_sel_o=Output(U.w(4)),         # Immediate selection for operand b
            regc_mux_o=Output(U.w(2)),              # Register C selection: S3, RD or 0
            # is_clpx_o and is_subrot_o are deprecated currently in our implementation

            # MUL related control signals
            mult_operator_o=Output(U.w(MUL_OP_WIDTH)),  # Multiplication operation selection
            mult_int_en_o=Output(Bool),             # Perform integer multiplication
            # mult_dot_en_o, mult_sel_subword_o, mult_dot_signed_o are deprecated
            # currently in our implementation
            mult_imm_mux_o=Output(Bool),            # Multiplication immediate mux selector
            mult_signed_mode_o=Output(U.w(2)),      # Multiplication in signed mode

            # APU and FPU currently not implemented

            # Register file related signals
            regfile_mem_we_o=Output(Bool),          # Write enable for regfile
            regfile_alu_we_o=Output(Bool),          # Write enable for 2nd regfile port
            regfile_alu_we_dec_o=Output(Bool),      # Write enable for 2nd regfile port without deassert
            regfile_alu_waddr_sel_o=Output(Bool),   # Select register write address for ALU/MUL operations

            # CSR manipulation
            csr_access_o=Output(Bool),              # Access to CSR
            csr_status_o=Output(Bool),              # Access to xstatus CSR
            csr_op_o=Output(U.w(CSR_OP_WIDTH)),     # Operation to perform on CSR
            current_priv_lvl_i=Input(U.w(PRIV_SEL_WIDTH)),      # The current privilege level

            # LD/ST unit signals
            data_req_o=Output(Bool),                # Start transaction to data memory
            data_we_o=Output(Bool),                 # Data memory write enable
            prepost_useincr_o=Output(Bool),         # When not active bypass the alu result for address calculation
            data_type_o=Output(U.w(2)),             # Data type on data memory: byte, half word or word
            data_sign_extension_o=Output(U.w(2)),   # Sign extension on read data from data memory
            data_reg_offset_o=Output(U.w(2)),       # Offset in byte inside register for stores
            # data_load_event_o is deprecated currently in our implementation

            # Atomic memory access and hwloop signals are deprecated currently in our implementation

            # Jump/Branches
            ctrl_transfer_insn_in_dec_o=Output(U.w(2)),     # Control transfer instruction without deassert
            ctrl_transfer_insn_in_id_o=Output(U.w(2)),      # Control transfer instruction is decoded
            ctrl_transfer_target_mux_sel_o=Output(U.w(2)),  # Jump target selection

            # HPM related control signals
            mcounteren_i=Input(U.w(32)),            # HPM related control signals
        )

        # Write enable/request control
        regfile_mem_we = Wire(Bool)
        regfile_alu_we = Wire(Bool)
        data_req = Wire(Bool)
        csr_illegal = Wire(Bool)
        ctrl_transfer_insn = Wire(U.w(2))

        csr_op = Wire(U.w(CSR_OP_WIDTH))

        alu_en = Wire(Bool)
        mult_int_en = Wire(Bool)

        ##################################################################################
        # Decoder
        ##################################################################################

        # Initial assign
        ctrl_transfer_insn <<= BRANCH_NONE
        io.ctrl_transfer_target_mux_sel_o <<= JT_JAL

        alu_en <<= Bool(True)
        io.alu_operator_o <<= ALU_SLTU

    return DECODER()
