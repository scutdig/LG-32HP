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
            regc_mux_o=Output(U.w(2)),              # Register c selection: S3, RD or 0
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
        io.alu_op_a_mux_sel_o <<= OP_A_REGA_OR_FWD
        io.alu_op_b_mux_sel_o <<= OP_B_REGB_OR_FWD
        io.alu_op_c_mux_sel_o <<= OP_C_REGC_OR_FWD
        io.regc_mux_o <<= REGC_ZERO
        io.imm_a_mux_sel_o <<= IMMA_ZERO
        io.imm_b_mux_sel_o <<= IMMB_I

        io.mult_operator_o <<= MUL_I
        io.mult_int_en <<= Bool(False)
        io.mult_imm_mux_o <<= MIMM_ZERO
        io.mult_signed_mode_o <<= U.w(2)(0)

        regfile_mem_we <<= Bool(False)
        regfile_alu_we <<= Bool(False)
        io.regfile_alu_waddr_sel_o <<= Bool(True)

        io.csr_access_o <<= Bool(False)
        io.csr_statues_o <<= Bool(False)
        csr_illegal <<= Bool(False)
        csr_op <<= CSR_OP_READ
        io.mret_insn_o <<= Bool(False)
        io.uret_insn_o <<= Bool(False)
        io.dret_insn_o <<= Bool(False)

        io.data_we_o <<= Bool(False)
        io.data_type_o <<= U.w(2)(0)
        io.data_sign_extension_o <<= U.w(2)(0)
        io.data_reg_offset_o <<= U.w(2)(0)
        data_req <<= Bool(False)
        io.prepost_useincr_o <<= Bool(True)

        io.illegal_insn_o <<= Bool(False)
        io.ebrk_insn_o <<= Bool(False)
        io.ecall_insn_o <<= Bool(False)
        io.wfi_o <<= Bool(False)

        io.fencei_insn_o <<= Bool(False)

        io.rega_used_o <<= Bool(False)
        io.regb_used_o <<= Bool(False)
        io.regc_used_o <<= Bool(False)

        io.mret_dec_o <<= Bool(False)
        io.uret_dec_o <<= Bool(False)
        io.dret_dec_o <<= Bool(False)

        ##################################################################################
        # Jumps
        ##################################################################################
        # OPCODE Mux
        with when(io.instr_rdata_i[6:0] == OPCODE_JAL):
            # Jump and Link
            io.ctrl_transfer_target_mux_sel_o <<= JT_JAL
            ctrl_transfer_insn <<= BRANCH_JAL
            # Calculate and store PC+4
            io.alu_op_a_mux_sel_o <<= OP_A_CURRPC
            io.alu_op_b_mux_sel_o <<= OP_B_IMM
            io.imm_b_mux_sel_o <<= IMMB_PCINCR
            io.alu_operator_o <<= ALU_ADD
            regfile_alu_we <<= Bool(True)
            # Calculate jump target (= PC + UJ imm)
        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_JALR):
            # Jump and Link Register
            io.ctrl_transfer_target_mux_sel_o <<= JT_JALR
            ctrl_transfer_insn <<= BRANCH_JALR
            # Calculate and store PC+4
            io.alu_op_a_mux_sel_o <<= OP_A_CURRPC
            io.alu_op_b_mux_sel_o <<= OP_B_IMM
            io.imm_b_mux_sel_o <<= IMMB_PCINCR
            io.alu_operator_o <<= ALU_ADD
            regfile_alu_we <<= Bool(True)
            # Calculate jump target (= RS1 + I imm)
            io.rega_used_o <<= Bool(True)

            with when(io.instr_rdata_i[14:12] != U.w(3)(0)):
                # funct3 != 0x000
                ctrl_transfer_insn <<= BRANCH_NONE
                regfile_alu_we <<= Bool(False)
                io.illegal_insn_o <<= Bool(True)
        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_BRANCH):
            # All Branch instructions
            io.ctrl_transfer_target_mux_sel_o <<= JT_COND
            ctrl_transfer_insn <<= BRANCH_COND
            io.alu_op_c_mux_sel_o <<= OP_C_JT
            io.rega_used_o <<= Bool(True)
            io.regb_used_o <<= Bool(True)

            # PULP_XPULP always == 0
            # funct3
            io.alu_operator_o <<= LookUpTable(io.instr_rdata_i[14:12], {
                U.w(3)(0x000): ALU_EQ,
                U.w(3)(0x001): ALU_NE,
                U.w(3)(0x100): ALU_LTS,
                U.w(3)(0x101): ALU_GES,
                U.w(3)(0x110): ALU_LTU,
                U.w(3)(0x111): ALU_GEU,
                ...: ALU_SLTU
            })
            with when((io.instr_rdata_i[14:12] == U.w(3)(0x010)) |
                      (io.instr_rdata_i[14:12] == U.w(3)(0x011))):
                io.illegal_insn_o <<= Bool(True)

        ##################################################################################
        # LD/ST
        ##################################################################################
        # All Store
        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_STORE):
            data_req <<= Bool(True)
            io.data_we_o <<= Bool(True)
            io.rega_used_o <<= Bool(True)
            io.regb_used_o <<= Bool(True)
            io.alu_operator_o <<= ALU_ADD
            # Pass write data through ALU operand c
            io.alu_op_c_mux_sel_o <<= OP_C_REGB_OR_FWD

            # PULP_XPULP always == 0
            with when(io.instr_rdata_i[14] == U.w(1)(0)):
                io.imm_b_mux_sel_o <<= IMMB_S
                io.alu_op_b_mux_sel_o <<= OP_B_IMM
            with otherwise():
                io.illegal_insn_o <<= Bool(True)

            # funct3
            io.data_type_o <<= LookUpTable(io.instr_rdata_i[13:12], {
                U.w(2)(0x00): U.w(2)(0x10),      # SB
                U.w(2)(0x01): U.w(2)(0x01),      # SH
                U.w(2)(0x10): U.w(2)(0x00),      # SW
                ...: U.w(2)(0x00)
            })

            with when(io.instr_rdata_i[13:12] == U.w(2)(0x11)):
                # Undefined
                data_req <<= Bool(False)
                io.data_we_o <<= Bool(False)
                io.illegal_insn_o <<= Bool(True)

        # All Load
        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_LOAD):
            data_req <<= Bool(True)
            io.regfile_mem_we <<= Bool(True)
            io.rega_used_o <<= Bool(True)
            io.data_type_o <<= U.w(2)(0x00)     # Read always read word
            # offset from immediate
            io.alu_operator_o <<= ALU_ADD
            io.alu_op_b_mux_sel_o <<= OP_B_IMM
            io.imm_b_mux_sel_o <<= IMMB_I

            # sign/zero extension
            # funct3[2] (bit 14): Zero (= 1), Sign (= 0)
            # Output
            io.data_sign_extension_o <<= CatBits(U.w(1)(0), ~io.instr_rdata_i[14])


    return DECODER()
