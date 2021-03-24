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


# Helper function for generating CSRs access illegal judgement
# Hardware Performance Monitor
def csrs_hpm(addr):
    return (addr == CSR_MCYCLE) | (addr == CSR_MINSTRET) | (addr == CSR_MHPMCOUNTER3) | (addr == CSR_MHPMCOUNTER4) | \
           (addr == CSR_MHPMCOUNTER5) | (addr == CSR_MHPMCOUNTER6) | (addr == CSR_MHPMCOUNTER7) | (addr == CSR_MHPMCOUNTER8) | \
           (addr == CSR_MHPMCOUNTER9) | (addr == CSR_MHPMCOUNTER10) | (addr == CSR_MHPMCOUNTER11) | (addr == CSR_MHPMCOUNTER12) | \
           (addr == CSR_MHPMCOUNTER13) | (addr == CSR_MHPMCOUNTER14) | (addr == CSR_MHPMCOUNTER15) | (addr == CSR_MHPMCOUNTER16) | \
           (addr == CSR_MHPMCOUNTER17) | (addr == CSR_MHPMCOUNTER18) | (addr == CSR_MHPMCOUNTER19) | (addr == CSR_MHPMCOUNTER20) | \
           (addr == CSR_MHPMCOUNTER21) | (addr == CSR_MHPMCOUNTER22) | (addr == CSR_MHPMCOUNTER23) | (addr == CSR_MHPMCOUNTER24) | \
           (addr == CSR_MHPMCOUNTER25) | (addr == CSR_MHPMCOUNTER26) | (addr == CSR_MHPMCOUNTER27) | (addr == CSR_MHPMCOUNTER28) | \
           (addr == CSR_MHPMCOUNTER29) | (addr == CSR_MHPMCOUNTER30) | (addr == CSR_MHPMCOUNTER31) | \
           (addr == CSR_MCYCLEH) | (addr == CSR_MINSTRETH) | \
           (addr == CSR_MHPMCOUNTER3H) | (addr == CSR_MHPMCOUNTER4H) | \
           (addr == CSR_MHPMCOUNTER5H) | (addr == CSR_MHPMCOUNTER6H) | (addr == CSR_MHPMCOUNTER7H) | (addr == CSR_MHPMCOUNTER8H) | \
           (addr == CSR_MHPMCOUNTER9H) | (addr == CSR_MHPMCOUNTER10H) | (addr == CSR_MHPMCOUNTER11H) | (addr == CSR_MHPMCOUNTER12H) | \
           (addr == CSR_MHPMCOUNTER13H) | (addr == CSR_MHPMCOUNTER14H) | (addr == CSR_MHPMCOUNTER15H) | (addr == CSR_MHPMCOUNTER16H) | \
           (addr == CSR_MHPMCOUNTER17H) | (addr == CSR_MHPMCOUNTER18H) | (addr == CSR_MHPMCOUNTER19H) | (addr == CSR_MHPMCOUNTER20H) | \
           (addr == CSR_MHPMCOUNTER21H) | (addr == CSR_MHPMCOUNTER22H) | (addr == CSR_MHPMCOUNTER23H) | (addr == CSR_MHPMCOUNTER24H) | \
           (addr == CSR_MHPMCOUNTER25H) | (addr == CSR_MHPMCOUNTER26H) | (addr == CSR_MHPMCOUNTER27H) | (addr == CSR_MHPMCOUNTER28H) | \
           (addr == CSR_MHPMCOUNTER29H) | (addr == CSR_MHPMCOUNTER30H) | (addr == CSR_MHPMCOUNTER31H) | \
           (addr == CSR_MCOUNTINHIBIT) | (addr == CSR_MHPMEVENT3) | (addr == CSR_MHPMEVENT4) | \
           (addr == CSR_MHPMEVENT5) | (addr == CSR_MHPMEVENT6) | (addr == CSR_MHPMEVENT7) | (addr == CSR_MHPMEVENT8) | \
           (addr == CSR_MHPMEVENT9) | (addr == CSR_MHPMEVENT10) | (addr == CSR_MHPMEVENT11) | (addr == CSR_MHPMEVENT12) | \
           (addr == CSR_MHPMEVENT13) | (addr == CSR_MHPMEVENT14) | (addr == CSR_MHPMEVENT15) | (addr == CSR_MHPMEVENT16) | \
           (addr == CSR_MHPMEVENT17) | (addr == CSR_MHPMEVENT18) | (addr == CSR_MHPMEVENT19) | (addr == CSR_MHPMEVENT20) | \
           (addr == CSR_MHPMEVENT21) | (addr == CSR_MHPMEVENT22) | (addr == CSR_MHPMEVENT23) | (addr == CSR_MHPMEVENT24) | \
           (addr == CSR_MHPMEVENT25) | (addr == CSR_MHPMEVENT26) | (addr == CSR_MHPMEVENT27) | (addr == CSR_MHPMEVENT28) | \
           (addr == CSR_MHPMEVENT29) | (addr == CSR_MHPMEVENT30) | (addr == CSR_MHPMEVENT31)


# Hardware Performance Monitor (unprivileged read-only mirror CSRs)
def csrs_hpm_mirror(addr):
    return (addr == CSR_CYCLE) | \
           (addr == CSR_INSTRET) | \
           (addr == CSR_HPMCOUNTER3) | \
           (addr == CSR_HPMCOUNTER4) |  (addr == CSR_HPMCOUNTER5) |  (addr == CSR_HPMCOUNTER6) |  (addr == CSR_HPMCOUNTER7) | \
           (addr == CSR_HPMCOUNTER8) |  (addr == CSR_HPMCOUNTER9) |  (addr == CSR_HPMCOUNTER10) | (addr == CSR_HPMCOUNTER11) | \
           (addr == CSR_HPMCOUNTER12) | (addr == CSR_HPMCOUNTER13) | (addr == CSR_HPMCOUNTER14) | (addr == CSR_HPMCOUNTER15) | \
           (addr == CSR_HPMCOUNTER16) | (addr == CSR_HPMCOUNTER17) | (addr == CSR_HPMCOUNTER18) | (addr == CSR_HPMCOUNTER19) | \
           (addr == CSR_HPMCOUNTER20) | (addr == CSR_HPMCOUNTER21) | (addr == CSR_HPMCOUNTER22) | (addr == CSR_HPMCOUNTER23) | \
           (addr == CSR_HPMCOUNTER24) | (addr == CSR_HPMCOUNTER25) | (addr == CSR_HPMCOUNTER26) | (addr == CSR_HPMCOUNTER27) | \
           (addr == CSR_HPMCOUNTER28) | (addr == CSR_HPMCOUNTER29) | (addr == CSR_HPMCOUNTER30) | (addr == CSR_HPMCOUNTER31) | \
           (addr == CSR_CYCLEH) | \
           (addr == CSR_INSTRETH) | \
           (addr == CSR_HPMCOUNTER3H) | \
           (addr == CSR_HPMCOUNTER4H) |  (addr == CSR_HPMCOUNTER5H) |  (addr == CSR_HPMCOUNTER6H) |  (addr == CSR_HPMCOUNTER7H) | \
           (addr == CSR_HPMCOUNTER8H) |  (addr == CSR_HPMCOUNTER9H) |  (addr == CSR_HPMCOUNTER10H) | (addr == CSR_HPMCOUNTER11H) | \
           (addr == CSR_HPMCOUNTER12H) | (addr == CSR_HPMCOUNTER13H) | (addr == CSR_HPMCOUNTER14H) | (addr == CSR_HPMCOUNTER15H) | \
           (addr == CSR_HPMCOUNTER16H) | (addr == CSR_HPMCOUNTER17H) | (addr == CSR_HPMCOUNTER18H) | (addr == CSR_HPMCOUNTER19H) | \
           (addr == CSR_HPMCOUNTER20H) | (addr == CSR_HPMCOUNTER21H) | (addr == CSR_HPMCOUNTER22H) | (addr == CSR_HPMCOUNTER23H) | \
           (addr == CSR_HPMCOUNTER24H) | (addr == CSR_HPMCOUNTER25H) | (addr == CSR_HPMCOUNTER26H) | (addr == CSR_HPMCOUNTER27H) | \
           (addr == CSR_HPMCOUNTER28H) | (addr == CSR_HPMCOUNTER29H) | (addr == CSR_HPMCOUNTER30H) | (addr == CSR_HPMCOUNTER31H)


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

            debug_mode_i=Input(Bool),
            debug_wfi_no_sleep_i=Input(Bool),

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
        mult_int_en <<= Bool(False)
        io.mult_int_en_o <<= Bool(False)
        io.mult_imm_mux_o <<= MIMM_ZERO
        io.mult_signed_mode_o <<= U.w(2)(0)

        regfile_mem_we <<= Bool(False)
        regfile_alu_we <<= Bool(False)
        io.regfile_alu_waddr_sel_o <<= Bool(True)

        io.csr_access_o <<= Bool(False)
        io.csr_status_o <<= Bool(False)
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
                # funct3 != 0b000
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
                U.w(3)(0b000): ALU_EQ,
                U.w(3)(0b001): ALU_NE,
                U.w(3)(0b100): ALU_LTS,
                U.w(3)(0b101): ALU_GES,
                U.w(3)(0b110): ALU_LTU,
                U.w(3)(0b111): ALU_GEU,
                ...: ALU_SLTU
            })
            with when((io.instr_rdata_i[14:12] == U.w(3)(0b010)) |
                      (io.instr_rdata_i[14:12] == U.w(3)(0b011))):
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
                U.w(2)(0b00): U.w(2)(0b10),      # SB
                U.w(2)(0b01): U.w(2)(0b01),      # SH
                U.w(2)(0b10): U.w(2)(0b00),      # SW
                ...: U.w(2)(0b00)
            })

            with when(io.instr_rdata_i[13:12] == U.w(2)(0b11)):
                # Undefined
                data_req <<= Bool(False)
                io.data_we_o <<= Bool(False)
                io.illegal_insn_o <<= Bool(True)

        # All Load
        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_LOAD):
            data_req <<= Bool(True)
            io.regfile_mem_we_o <<= Bool(True)
            io.rega_used_o <<= Bool(True)
            io.data_type_o <<= U.w(2)(0b00)     # Read always read word
            # offset from immediate
            io.alu_operator_o <<= ALU_ADD
            io.alu_op_b_mux_sel_o <<= OP_B_IMM
            io.imm_b_mux_sel_o <<= IMMB_I

            # sign/zero extension
            # funct3[2] (bit 14): Zero (= 1), Sign (= 0)
            # Output
            io.data_sign_extension_o <<= CatBits(U.w(1)(0), ~io.instr_rdata_i[14])

            # Load size
            io.data_type_o <<= LookUpTable(io.instr_rdata_i[13:12], {
                U.w(2)(0b00): U.w(2)(0b10),     # LB
                U.w(2)(0b01): U.w(2)(0b01),     # LH
                U.w(2)(0b10): U.w(2)(0b00),     # LW
                ...: U.w(2)(0b00)               # Illegal
            })

            # funct3 = 0b011, 0b110, 0b111 are illegal
            with when((io.instr_rdata_i[14:12] == U.w(3)(0b111)) |
                      (io.instr_rdata_i[14:12] == U.w(3)(0b110)) |
                      (io.instr_rdata_i[14:12] == U.w(3)(0b011))):
                io.illegal_insn_o <<= Bool(True)

        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_AMO):
            # We currently didn't support AMO instructions yet
            io.illegal_insn_o <<= Bool(True)

        ##################################################################################
        # ALU
        ##################################################################################
        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_LUI):
            # Load Upper Immediate
            io.alu_op_a_mux_sel_o <<= OP_A_IMM
            io.alu_op_b_mux_sel_o <<= OP_B_IMM
            io.imm_a_mux_sel_o <<= IMMA_ZERO
            io.imm_b_mux_sel_o <<= IMMB_U
            io.alu_operator_o <<= ALU_ADD
            regfile_alu_we <<= Bool(True)
        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_AUIPC):
            # Add Upper Immediate to PC
            io.alu_op_a_mux_sel_o <<= OP_A_CURRPC
            io.alu_op_b_mux_sel_o <<= OP_B_IMM
            io.imm_b_mux_sel_o <<= IMMB_U
            io.alu_operator_o <<= ALU_ADD
            regfile_alu_we <<= Bool(True)
        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_OPIMM):
            # Register-Immediate ALU Operations
            io.alu_op_b_mux_sel_o <<= OP_B_IMM
            io.imm_b_mux_sel_o <<= IMMB_I
            regfile_alu_we <<= Bool(True)
            io.rega_used_o <<= Bool(True)

            # funct3
            io.alu_operator_o <<= LookUpTable(io.instr_rdata_i[14:12], {
                U.w(3)(0b000): ALU_ADD,     # addi
                U.w(3)(0b001): ALU_SLL,     # slli
                U.w(3)(0b010): ALU_SLTS,    # slti
                U.w(3)(0b011): ALU_SLTU,    # sltiu
                U.w(3)(0b100): ALU_XOR,     # xori
                U.w(3)(0b110): ALU_OR,      # ori
                U.w(3)(0b111): ALU_AND,     # andi
                ...: ALU_SLTU
            })

            # slli, srli, srai -> funct7 has limits
            with when((io.instr_rdata_i[14:12] == U.w(3)(0b001)) |
                      (io.instr_rdata_i[31:25] != U.w(7)(0))):
                # slli -> imm[11:5] must be 0b00
                io.illegal_insn_o <<= Bool(True)

            with when(io.instr_rdata_i[14:12] == U.w(3)(0b101)):
                # is srli or srai?
                with when(io.instr_rdata_i[31:25] == U.w(7)(0)):
                    # srli -> imm[11:5] must be 0b00
                    io.alu_operator_o <<= ALU_SRL
                with elsewhen(io.instr_rdata_i[31:25] == U.w(7)(0b0100000)):
                    # srai -> imm[11:5] must be 0b20
                    io.alu_operator_o <<= ALU_SRA
                with otherwise():
                    io.illegal_insn_o <<= Bool(True)

        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_OP):
            # Register-Register ALU operation
            # In our current implementation, funct7 (io.instr_rdata_i[31:25]) only could
            # be 0b00/0b20
            with when(io.instr_rdata_i[31:30] == U.w(2)(0b11)):
                # PREFIX 11, illegal
                io.illegal_insn_o <<= Bool(True)
            with elsewhen(io.instr_rdata_i[31:30] == U.w(2)(0b10)):
                # PREFIX 10, illegal
                io.illegal_insn_o <<= Bool(True)
            with otherwise():
                # PREFIX 00/01
                regfile_alu_we <<= Bool(True)
                io.rega_used_o <<= Bool(True)

                # In fact, in our implementation, this should not be 1
                with when(~io.instr_rdata_i[28]):
                    io.regb_used_o <<= Bool(True)

                rr_con = CatBits(io.instr_rdata_i[30:25], io.instr_rdata_i[14:12])

                # RV32I ALU Operations
                
                # I should use when/elsewhen/otherwise is more clear to read
                # io.alu_operator_o <<= LookUpTable(rr_con, {
                #     U.w(9)(0b000000000): ALU_ADD,      # add
                #     U.w(9)(0b100000000): ALU_SUB,      # sub
                #     U.w(9)(0b000000010): ALU_SLTS,     # slt
                #     U.w(9)(0b000000011): ALU_SLTU,     # sltu
                #     U.w(9)(0b000000100): ALU_XOR,      # xor
                #     U.w(9)(0b000000110): ALU_OR,       # or
                #     U.w(9)(0b000000111): ALU_AND,      # and
                #     U.w(9)(0b000000001): ALU_SLL,      # sll
                #     U.w(9)(0b000000101): ALU_SRL,      # srl
                #     U.w(9)(0b100000101): ALU_SRA,      # sra
                # })

                with when(rr_con == U.w(9)(0b000000000)):
                    io.alu_operator_o <<= ALU_ADD
                with elsewhen(rr_con == U.w(9)(0b100000000)):
                    io.alu_operator_o <<= ALU_SUB
                with elsewhen(rr_con == U.w(9)(0b000000010)):
                    io.alu_operator_o <<= ALU_SLTS
                with elsewhen(rr_con == U.w(9)(0b000000011)):
                    io.alu_operator_o <<= ALU_SLTU
                with elsewhen(rr_con == U.w(9)(0b000000100)):
                    io.alu_operator_o <<= ALU_XOR
                with elsewhen(rr_con == U.w(9)(0b000000110)):
                    io.alu_operator_o <<= ALU_OR
                with elsewhen(rr_con == U.w(9)(0b000000111)):
                    io.alu_operator_o <<= ALU_AND
                with elsewhen(rr_con == U.w(9)(0b000000001)):
                    io.alu_operator_o <<= ALU_SLL
                with elsewhen(rr_con == U.w(9)(0b000000101)):
                    io.alu_operator_o <<= ALU_SRL
                with elsewhen(rr_con == U.w(9)(0b100000101)):
                    io.alu_operator_o <<= ALU_SRA
                    
                # RV32M instructions
                with elsewhen(rr_con == U.w(9)(0b000001000)):   # mul
                    # Default unsigned x unsigned 00
                    alu_en <<= Bool(False)
                    mult_int_en <<= Bool(True)
                    io.mult_operator_o <<= MUL_MAC32
                    io.regc_mux_o <<= REGC_ZERO
                with elsewhen(rr_con == U.w(9)(0b000001001)):   # mulh
                    alu_en <<= Bool(False)
                    io.regc_used_o <<= Bool(True)
                    io.regc_mux_o <<= REGC_ZERO
                    io.mult_signed_mode_o <<= U.w(2)(0b11)      # Default signed x signed 11
                    mult_int_en <<= Bool(True)
                    io.mult_operator_o <<= MUL_H
                with elsewhen(rr_con == U.w(9)(0b000001010)):   # mulsu
                    alu_en <<= Bool(False)
                    io.regc_used_o <<= Bool(True)
                    io.regc_mux_o <<= REGC_ZERO
                    io.mult_signed_mode_o <<= U.w(2)(0b01)      # signed x unsigned 01
                    mult_int_en <<= Bool(True)
                    io.mult_operator_o <<= MUL_H
                with elsewhen(rr_con == U.w(9)(0b000001011)):   # mulu
                    alu_en <<= Bool(False)
                    io.regc_used_o <<= Bool(True)
                    io.regc_mux_o <<= REGC_ZERO
                    io.mult_signed_mode_o <<= U.w(2)(0b00)      # unsigned x unsigned 00
                    mult_int_en <<= Bool(True)
                    io.mult_operator_o <<= MUL_H
                with elsewhen(rr_con == U.w(9)(0b000001100)):   # div
                    io.alu_op_a_mux_sel_o <<= OP_A_REGB_OR_FWD
                    io.alu_op_b_mux_sel_o <<= OP_B_REGA_OR_FWD
                    io.regb_used_o <<= Bool(True)
                    io.alu_operator_o <<= ALU_DIV
                with elsewhen(rr_con == U.w(9)(0b000001101)):   # divu
                    io.alu_op_a_mux_sel_o <<= OP_A_REGB_OR_FWD
                    io.alu_op_b_mux_sel_o <<= OP_B_REGA_OR_FWD
                    io.regb_used_o <<= Bool(True)
                    io.alu_operator_o <<= ALU_DIVU
                with elsewhen(rr_con == U.w(9)(0b000001110)):   # rem
                    io.alu_op_a_mux_sel_o <<= OP_A_REGB_OR_FWD
                    io.alu_op_b_mux_sel_o <<= OP_B_REGA_OR_FWD
                    io.regb_used_o <<= Bool(True)
                    io.alu_operator_o <<= ALU_REM
                with elsewhen(rr_con == U.w(9)(0b000001111)):   # remu
                    io.alu_op_a_mux_sel_o <<= OP_A_REGB_OR_FWD
                    io.alu_op_b_mux_sel_o <<= OP_B_REGA_OR_FWD
                    io.regb_used_o <<= Bool(True)
                    io.alu_operator_o <<= ALU_REMU
                with otherwise():
                    io.illegal_insn_o <<= Bool(True)

        with elsewhen((io.instr_rdata_i[6:0] == OPCODE_OP_FP) |
                      (io.instr_rdata_i[6:0] == OPCODE_OP_FMADD) |
                      (io.instr_rdata_i[6:0] == OPCODE_OP_FMSUB) |
                      (io.instr_rdata_i[6:0] == OPCODE_OP_FNMSUB) |
                      (io.instr_rdata_i[6:0] == OPCODE_OP_FNMADD) |
                      (io.instr_rdata_i[6:0] == OPCODE_STORE_FP) |
                      (io.instr_rdata_i[6:0] == OPCODE_LOAD_FP) |
                      (io.instr_rdata_i[6:0] == OPCODE_PULP_OP) |
                      (io.instr_rdata_i[6:0] == OPCODE_VECOP)):
            # No FP/XPULP implementation currently
            io.illegal_insn_o <<= Bool(True)

        ##################################################################################
        # Special
        ##################################################################################
        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_FENCE):
            # io.fencei_insn_o <<= LookUpTable(io.instr_rdata_i[14:12], {
            #     U.w(3)(0b000): Bool(True),      # FENCE (Synch thread), flush pipeline
            #     U.w(3)(0b001): Bool(True),      # FENCE.I, flush pipeline and prefetch buffer
            #     ...: Bool(False)
            # })
            with when(io.instr_rdata_i[14:12] == U.w(3)(0b000)):
                io.fencei_insn_o <<= Bool(True)
            with elsewhen(io.instr_rdata_i[14:12] == U.w(3)(0b001)):
                io.fencei_insn_o <<= Bool(True)
            with otherwise():
                io.illegal_insn_o <<= Bool(True)

        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_SYSTEM):
            with when(io.instr_rdata_i[14:12] == U.w(3)(0)):
                # Non CSR related SYSTEM instructions
                with when((io.instr_rdata_i[19:15] == U(0)) & (io.instr_rdata_i[11:7] == U(0))):
                    with when(io.instr_rdata_i[31:20] == U.w(12)(0x000)):
                        # imm=0x0, ECALL, environment (system) call
                        io.ecall_insn_o <<= Bool(True)
                    with elsewhen(io.instr_rdata_i[31:20] == U.w(12)(0x001)):
                        # imm=0x1, EBREAK, debugger trap
                        io.ebrk_insn_o <<= Bool(True)
                    with elsewhen(io.instr_rdata_i[31:20] == U.w(12)(0x302)):   # mret
                        io.illegal_insn_o <<= (io.current_priv_lvl_i != PRIV_LVL_M) if PULP_SECURE else Bool(False)
                        io.mret_insn_o <<= ~io.illegal_insn_o
                        io.mret_dec_o <<= Bool(True)
                    with elsewhen(io.instr_rdata_i[31:20] == U.w(12)(0x002)):   # uret
                        io.illegal_insn_o <<= Bool(True) if PULP_SECURE else Bool(False)
                        io.uret_insn_o <<= ~io.illegal_insn_o
                        io.uret_dec_o <<= Bool(True)
                    with elsewhen(io.instr_rdata_i[31:20] == U.w(12)(0x7b2)):   # dret
                        io.illegal_insn_o <<= ~io.debug_mode_i
                        io.dret_insn_o <<= io.debug_mode_i
                        io.dret_dec_o <<= Bool(True)
                    with elsewhen(io.instr_rdata_i[31:20] == U.w(12)(0x105)):   # wfi
                        # Wait for interrupt
                        io.wfi_o <<= Bool(True)
                        with when(io.debug_wfi_no_sleep_i):
                            # Treat as NOP (do not cause sleep mode entry)
                            # Using decoding similar to ADDI, but without regsiter reads/writes, i.e.
                            # keep regfile_alu_we = 0, rega_used_o = 0
                            io.alu_op_b_mux_sel_o <<= OP_B_IMM
                            io.imm_b_mux_sel_o <<= IMMB_I
                            io.alu_operator_o <<= ALU_ADD
                    with otherwise():
                        io.illegal_insn_o <<= Bool(True)
                with otherwise():
                    io.illegal_insn_o <<= Bool(True)
            with otherwise():
                # instruction to read/modify CSR
                io.csr_access_o <<= Bool(True)
                regfile_alu_we <<= Bool(True)
                io.alu_op_b_mux_sel_o <<= OP_B_IMM
                io.imm_a_mux_sel_o <<= IMMA_Z
                io.imm_b_mux_sel_o <<= IMMB_I       # CSR address is encoded in I imm

                with when(io.instr_rdata_i[14] == U.w(1)(1)):
                    # rs1 field if used as immediate: CSRRXI
                    io.alu_op_a_mux_sel_o <<= OP_A_IMM
                with otherwise():
                    # CSRRX
                    io.rega_used_o <<= Bool(True)
                    io.alu_op_a_mux_sel_o <<= OP_A_REGA_OR_FWD

                # instr_rdata_i[19:14] = rs or imm
                # if set (S) or clear (C) with rs == x0 or imm == 0
                # then do not perform a write action
                with when(io.instr_rdata_i[13:12] == U.w(2)(0b01)):
                    csr_op <<= CSR_OP_WRITE
                with elsewhen(io.instr_rdata_i[13:12] == U.w(2)(0b10)):
                    csr_op <<= Mux(io.instr_rdata_i[19:15] == U(0), CSR_OP_READ, CSR_OP_SET)
                with elsewhen(io.instr_rdata_i[13:12] == U.w(2)(0b11)):
                    csr_op <<= Mux(io.instr_rdata_i[19:15] == U(0), CSR_OP_READ, CSR_OP_CLEAR)
                with otherwise():
                    csr_illegal <<= Bool(True)

                with when(io.instr_rdata_i[29:28] > io.current_priv_lvl_i):
                    # CSR Address[9:8]
                    csr_illegal <<= Bool(True)

                # Determine if CSR access is illegal
                with when((io.instr_rdata_i[31:20] == CSR_FFLAGS) |
                          (io.instr_rdata_i[31:20] == CSR_FRM) |
                          (io.instr_rdata_i[31:20] == CSR_FCSR)):
                    # FP
                    csr_illegal <<= Bool(True)
                with elsewhen((io.instr_rdata_i[31:20] == CSR_MVENDORID) |
                              (io.instr_rdata_i[31:20] == CSR_MARCHID) |
                              (io.instr_rdata_i[31:20] == CSR_MIMPID) |
                              (io.instr_rdata_i[31:20] == CSR_MHARTID)):
                    # Writes to read only CSRs results in illegal instruction
                    with when(csr_op != CSR_OP_READ):
                        csr_illegal <<= Bool(True)
                with elsewhen((io.instr_rdata_i[31:20] == CSR_MSTATUS) |
                              (io.instr_rdata_i[31:20] == CSR_MARCHID) |
                              (io.instr_rdata_i[31:20] == CSR_MIMPID) |
                              (io.instr_rdata_i[31:20] == CSR_MHARTID)):
                    # These are valid CSR registers
                    # Not illegal, but treat as status CSR for side effect handling
                    io.csr_status_o <<= Bool(True)
                with elsewhen((io.instr_rdata_i[31:20] == CSR_MISA) |
                              (io.instr_rdata_i[31:20] == CSR_MIE) |
                              (io.instr_rdata_i[31:20] == CSR_MSCRATCH) |
                              (io.instr_rdata_i[31:20] == CSR_MTVAL) |
                              (io.instr_rdata_i[31:20] == CSR_MIP)):
                    # do nothing, not illegal
                    csr_illegal <<= Bool(False)
                with elsewhen(csrs_hpm(io.instr_rdata_i[31:20])):
                    # Not illegal, but treat as status CSR to get accurate counts
                    io.csr_status_o <<= U.w(1)(1)
                with elsewhen(csrs_hpm_mirror(io.instr_rdata_i[31:20])):
                    # Read-only and readable from user mode only if the bit of mcounteren is set
                    if PULP_SECURE:
                        with when((csr_op != CSR_OP_READ) | ((io.current_priv_lvl_i != PRIV_LVL_M)
                                                             & (~io.mcounteren_i[io.instr_rdata_i[24:20]]))):
                            csr_illegal <<= Bool(True)
                    else:
                        with when(csr_op != CSR_OP_READ):
                            io.csr_status_o <<= Bool(True)

                with elsewhen(io.instr_rdata_i[31:20] == CSR_MCOUNTEREN):
                    # This register only exists in user mode
                    if not PULP_SECURE:
                        csr_illegal <<= Bool(True)
                    else:
                        io.csr_status_o <<= Bool(True)

                with elsewhen((io.instr_rdata_i[31:20] == CSR_DCSR) |
                              (io.instr_rdata_i[31:20] == CSR_DPC) |
                              (io.instr_rdata_i[31:20] == CSR_DSCRATCH0) |
                              (io.instr_rdata_i[31:20] == CSR_DSCRATCH1)):
                    # Debug register access
                    with when(~io.debug_mode_i):
                        csr_illegal <<= Bool(True)
                    with otherwise():
                        io.csr_status_o <<= Bool(True)

                with elsewhen((io.instr_rdata_i[31:20] == CSR_TSELECT) |
                              (io.instr_rdata_i[31:20] == CSR_TDATA1) |
                              (io.instr_rdata_i[31:20] == CSR_TDATA2) |
                              (io.instr_rdata_i[31:20] == CSR_TDATA3) |
                              (io.instr_rdata_i[31:20] == CSR_TINFO) |
                              (io.instr_rdata_i[31:20] == CSR_MCONTEXT) |
                              (io.instr_rdata_i[31:20] == CSR_SCONTEXT)):
                    # Debug Trigger register access
                    if not DEBUG_TRIGGER_EN:
                        csr_illegal <<= Bool(True)
                    else:
                        csr_illegal <<= Bool(False)

                with elsewhen((io.instr_rdata_i[31:20] == CSR_LPSTART0) |
                              (io.instr_rdata_i[31:20] == CSR_LPEND0) |
                              (io.instr_rdata_i[31:20] == CSR_LPCOUNT0) |
                              (io.instr_rdata_i[31:20] == CSR_LPSTART1) |
                              (io.instr_rdata_i[31:20] == CSR_LPEND1) |
                              (io.instr_rdata_i[31:20] == CSR_LPCOUNT1) |
                              (io.instr_rdata_i[31:20] == CSR_UHARTID)):
                    # Hardware loop register, we currently do not implement
                    csr_illegal <<= Bool(True)

                with elsewhen(io.instr_rdata_i[31:20] == CSR_PRIVLV):
                    csr_illegal <<= Bool(True)

                with elsewhen((io.instr_rdata_i[31:20] == CSR_PMPCFG0) | (io.instr_rdata_i[31:20] == CSR_PMPCFG1) |
                              (io.instr_rdata_i[31:20] == CSR_PMPCFG2) | (io.instr_rdata_i[31:20] == CSR_PMPCFG3) |
                              (io.instr_rdata_i[31:20] == CSR_PMPADDR0) | (io.instr_rdata_i[31:20] == CSR_PMPADDR1) |
                              (io.instr_rdata_i[31:20] == CSR_PMPADDR2) | (io.instr_rdata_i[31:20] == CSR_PMPADDR3) |
                              (io.instr_rdata_i[31:20] == CSR_PMPADDR4) | (io.instr_rdata_i[31:20] == CSR_PMPADDR5) |
                              (io.instr_rdata_i[31:20] == CSR_PMPADDR6) | (io.instr_rdata_i[31:20] == CSR_PMPADDR7) |
                              (io.instr_rdata_i[31:20] == CSR_PMPADDR8) | (io.instr_rdata_i[31:20] == CSR_PMPADDR9) |
                              (io.instr_rdata_i[31:20] == CSR_PMPADDR10) | (io.instr_rdata_i[31:20] == CSR_PMPADDR11) |
                              (io.instr_rdata_i[31:20] == CSR_PMPADDR12) | (io.instr_rdata_i[31:20] == CSR_PMPADDR13) |
                              (io.instr_rdata_i[31:20] == CSR_PMPADDR14) | (io.instr_rdata_i[31:20] == CSR_PMPADDR15)):
                    # PMP register access
                    if not USE_PMP:
                        csr_illegal <<= Bool(True)

                with elsewhen((io.instr_rdata_i[31:20] == CSR_USTATUS) | (io.instr_rdata_i[31:20] == CSR_UEPC) |
                              (io.instr_rdata_i[31:20] == CSR_UTVEC) | (io.instr_rdata_i[31:20] == CSR_UCAUSE)):
                    # User register access
                    if not PULP_SECURE:
                        csr_illegal <<= Bool(True)
                    else:
                        io.csr_status_o <<= Bool(True)

                with otherwise():
                    csr_illegal <<= Bool(True)

                io.illegal_insn_o <<= csr_illegal

        with elsewhen(io.instr_rdata_i[6:0] == OPCODE_HWLOOP):
            io.illegal_insn_o <<= Bool(True)

        with otherwise():
            io.illegal_insn_o <<= Bool(True)

        # make sure invalid compressed instruction causes an exception
        with when(io.illegal_c_insn_i):
            io.illegal_insn_o <<= Bool(True)

        # Deassert we signals (in case of stalls)
        io.alu_en_o <<= Mux(io.deassert_we_i, Bool(False), alu_en)
        io.mult_int_en_o <<= Mux(io.deassert_we_i, Bool(False), mult_int_en)
        io.regfile_mem_we_o <<= Mux(io.deassert_we_i, Bool(False), regfile_mem_we)
        io.regfile_alu_we_o <<= Mux(io.deassert_we_i, Bool(False), regfile_alu_we)
        io.data_req_o <<= Mux(io.deassert_we_i, Bool(False), data_req)
        io.csr_op_o <<= Mux(io.deassert_we_i, CSR_OP_READ, csr_op)
        io.ctrl_transfer_insn_in_id_o <<= Mux(io.deassert_we_i, BRANCH_NONE, ctrl_transfer_insn)

        io.ctrl_transfer_insn_in_dec_o <<= ctrl_transfer_insn
        io.regfile_alu_we_dec_o <<= regfile_alu_we

    return DECODER()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(decoder()), "decoder.fir"))
