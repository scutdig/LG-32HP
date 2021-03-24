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
   Date: 2021-03-16
   File Name: id_stage.py
   Description: Decode stage of the pipeline.
"""
from pyhcl import *
from src.include.pkg import *
from src.rtl.register_file_ff import *
from src.rtl.decoder import *
from src.rtl.controller import *
from src.rtl.int_controller import *


def sign_extension(sign, width):
    # ex: assume sign extend 4 bits
    # U.w(5)(2**4-1) -> U.w(5)(15) -> U.w(4)(0b01111)
    # If sign = 1'b0 -> 5'b01111 + ~1'b0 = 5'b01111 + 1'b1 = 5'b10000 -> return 4'b0000
    # If sign = 1'b1 -> 5'b01111 + ~1'b1 = 5'b01111                   -> return 4'b1111
    return (U.w(width+1)(2**width-1) + (~sign))[width-1:0]


def id_stage(PULP_SECURE=0, USE_PMP=0, DEBUG_TRIGGER_EN=1):
    REG_S1_MSB = 19
    REG_S1_LSB = 15
    
    REG_S2_MSB = 24
    REG_S2_LSB = 20
    
    REG_S4_MSB = 31
    REG_S4_LSB = 27
    
    REG_D_MSB  = 11
    REG_D_LSB  = 7

    class ID_STAGE(Module):
        io = IO(
            # clk_ungated_i -> implement in FIRRTL code for controller
            scan_cg_en_i=Input(Bool),

            fetch_enable_i=Input(Bool),
            ctrl_busy_o=Output(Bool),
            is_decoding_o=Output(Bool),

            # Interface to IF stage
            instr_valid_i=Input(Bool),
            instr_rdata_i=Input(U.w(32)),           # Comes from pipeline of IF stage
            instr_req_o=Output(Bool),
            is_compressed_i=Input(Bool),
            illegal_c_insn_i=Input(Bool),

            # Jumps and branches
            branch_in_ex_o=Output(Bool),
            branch_decision_i=Input(Bool),
            jump_target_o=Output(U.w(32)),

            # IF and ID stage signals
            clear_instr_valid_o=Output(Bool),
            pc_set_o=Output(Bool),
            pc_mux_o=Output(U.w(4)),
            exc_pc_mux_o=Output(U.w(3)),
            trap_addr_mux_o=Output(U.w(2)),

            is_fetch_failed_i=Input(Bool),

            pc_id_i=Input(U.w(32)),

            # Stalls
            halt_if_o=Output(Bool),                 # Controller requests a halt of the IF stage

            id_ready_o=Output(Bool),                # ID stage is ready for the next instruction
            ex_ready_i=Input(Bool),                 # EX stage is ready for the next instruction
            wb_ready_i=Input(Bool),                 # WB stage is ready for the next instruction

            id_valid_o=Output(Bool),                # ID stage is done
            ex_valid_i=Input(Bool),                 # EX stage is done

            # Pipeline ID/EX
            pc_ex_o=Output(U.w(32)),

            alu_operand_a_ex_o=Output(U.w(32)),
            alu_operand_b_ex_o=Output(U.w(32)),
            alu_operand_c_ex_o=Output(U.w(32)),
            bmask_a_ex_o=Output(U.w(5)),
            bmask_b_ex_o=Output(U.w(5)),
            imm_vec_ext_ex_o=Output(U.w(2)),

            regfile_waddr_ex_o=Output(U.w(6)),
            regfile_we_ex_o=Output(Bool),

            regfile_alu_waddr_ex_o=Output(U.w(6)),
            regfile_alu_ex_o=Output(Bool),

            # ALU
            alu_en_ex_o=Output(Bool),
            alu_operator_ex_o=Output(U.w(ALU_OP_WIDTH)),
            alu_is_clpx_ex_o=Output(Bool),
            alu_is_subrot_ex_o=Output(Bool),
            alu_clpx_shift_ex_o=Output(U.w(2)),

            # MUL
            mult_operator_ex_o=Output(U.w(MUL_OP_WIDTH)),
            mult_operand_a_ex_o=Output(U.w(32)),
            mult_operand_b_ex_o=Output(U.w(32)),
            mult_operand_c_ex_o=Output(U.w(32)),
            mult_en_ex_o=Output(Bool),
            mult_sel_subword_ex_o=Output(Bool),
            mult_signed_mode_ex_o=Output(U.w(2)),
            mult_imm_ex_o=Output(U.w(5)),

            # mult dot production deprecated

            # APU deprecated

            # CSR ID/EX
            csr_access_ex_o=Output(Bool),
            csr_op_ex_o=Output(U.w(CSR_OP_WIDTH)),
            current_priv_lvl_i=Input(U.w(PRIV_SEL_WIDTH)),
            csr_irq_sec_i=Output(Bool),
            csr_cause_o=Output(U.w(6)),
            csr_save_if_o=Output(Bool),
            csr_save_id_o=Output(Bool),
            csr_save_ex_o=Output(Bool),
            csr_restore_mret_id_o=Output(Bool),
            csr_restore_uret_id_o=Output(Bool),
            csr_restore_dret_id_o=Output(Bool),
            csr_save_cause_o=Output(Bool),

            # Hwloop deprecated

            # Interface to load/store unit
            data_req_ex_o=Output(Bool),
            data_we_ex_o=Output(Bool),
            data_type_ex_o=Output(U.w(2)),
            data_sign_ext_ex_o=Output(U.w(2)),
            data_reg_offset_ex_o=Output(U.w(2)),
            data_load_event_ex_o=Output(Bool),

            data_misaligned_ex_o=Output(Bool),

            prepost_useincr_ex_o=Output(Bool),
            data_misaligned_i=Input(Bool),
            data_err_i=Input(Bool),
            data_err_ack_o=Output(Bool),

            # Interrupt signals
            irq_i=Input(U.w(32)),
            irq_sec_i=Input(Bool),
            mie_bypass_i=Input(U.w(32)),
            mip_o=Output(U.w(32)),
            m_irq_enable_i=Input(Bool),
            u_irq_enable_i=Input(Bool),
            irq_ack_o=Output(Bool),
            irq_id_o=Output(U.w(5)),
            exc_cause_o=Output(U.w(5)),

            # Debug Signal
            debug_mode_o=Output(Bool),
            debug_cause_o=Output(U.w(3)),
            debug_csr_save_o=Output(Bool),
            debug_req_i=Input(Bool),
            debug_single_step_i=Input(Bool),
            debug_ebreakm_i=Input(Bool),
            debug_ebreaku_i=Input(Bool),
            trigger_match_i=Input(Bool),
            debug_p_elw_no_sleep_o=Output(Bool),
            debug_havereset_o=Output(Bool),
            debug_running_o=Output(Bool),
            debug_halted_o=Output(Bool),

            # Wakeup Signal
            wkae_from_sleep_o=Output(Bool),

            # Forward Signals
            regfile_waddr_wb_i=Input(U.w(6)),
            regfile_we_wb_i=Input(Bool),
            # From wb_stage: selects data from data memory, ex_stage result and sp rdata
            regfile_wdata_wb_i=Input(U.w(32)),

            regfile_alu_waddr_fw_i=Input(U.w(6)),
            regfile_alu_we_fw_i=Input(Bool),
            regfile_alu_wdata_fw_i=Input(U.w(32)),

            # From ALU
            mult_multicycle_i=Input(Bool),  # When we need multiple cycles in the multiplier and use op c as storage

            # Performance Counters
            mhpmevent_minstret_o=Output(Bool),
            mhpmevent_load_o=Output(Bool),
            mhpmevent_store_o=Output(Bool),
            mhpmevent_jump_o=Output(Bool),
            mhpmevent_branch_o=Output(Bool),
            mhpmevent_branch_taken_o=Output(Bool),
            mhpmevent_compressed_o=Output(Bool),
            mhpmevent_jr_stall_o=Output(Bool),
            mhpmevent_imiss_o=Output(Bool),
            mhpmevent_ld_stall_o=Output(Bool),
            mhpmevent_pipe_stall_o=Output(Bool),

            perf_imiss_i=Input(Bool),
            mcounteren_i=Input(U.w(32))
        )

        instr = Wire(U.w(32))

        # Decoder/Controller ID stage internal signals
        deassert_we = Wire(Bool)

        illegal_insn_dec = Wire(Bool)
        ebrk_insn_dec = Wire(Bool)
        mret_insn_dec = Wire(Bool)
        uret_insn_dec = Wire(Bool)

        dret_insn_dec = Wire(Bool)

        ecall_insn_dec = Wire(Bool)
        wfi_insn_dec = Wire(Bool)

        fencei_insn_dec = Wire(Bool)

        rega_used_dec = Wire(Bool)
        regb_used_dec = Wire(Bool)
        regc_used_dec = Wire(Bool)

        branch_taken_ex = Wire(Bool)
        ctrl_transfer_insn_in_id = Wire(U.w(2))
        ctrl_transfer_insn_in_dec = Wire(U.w(2))

        misaligned_stall = Wire(Bool)
        jr_stall = Wire(Bool)
        load_stall = Wire(Bool)
        halt_id = Wire(Bool)
        halt_if = Wire(Bool)

        debug_wfi_no_sleep = Wire(Bool)

        # Immediate decoding and sign extension
        imm_i_type = Wire(U.w(32))
        imm_iz_type = Wire(U.w(32))
        imm_s_type = Wire(U.w(32))
        imm_sb_type = Wire(U.w(32))
        imm_u_type = Wire(U.w(32))
        imm_uj_type = Wire(U.w(32))
        imm_z_type = Wire(U.w(32))
        imm_s2_type = Wire(U.w(32))
        imm_bi_type = Wire(U.w(32))
        imm_s3_type = Wire(U.w(32))
        imm_vs_type = Wire(U.w(32))
        imm_vu_type = Wire(U.w(32))
        imm_shuffleb_type = Wire(U.w(32))
        imm_shuffleh_type = Wire(U.w(32))
        imm_shuffle_type = Wire(U.w(32))
        imm_clip_type = Wire(U.w(32))

        imm_a = Wire(U.w(32))   # Contains the immediate for operand a
        imm_b = Wire(U.w(32))   # Contains the immediate for operand b

        jump_target = Wire(U.w(32))     # Calculated jump target ( -> EX -> IF)

        # Signals running between controller and int_controller
        irq_req_ctrl = Wire(Bool)
        irq_sec_ctrl = Wire(Bool)
        irq_wu_ctrl = Wire(Bool)
        irq_id_ctrl = Wire(U.w(5))

        # Register file interface
        regfile_addr_ra_id = Wire(U.w(6))
        regfile_addr_rb_id = Wire(U.w(6))
        regfile_addr_rc_id = Wire(U.w(6))

        regfile_waddr_id = Wire(U.w(6))
        regfile_alu_waddr_id = Wire(U.w(6))
        regfile_alu_we_id = Wire(Bool)
        regfile_alu_we_dec_id = Wire(Bool)

        regfile_data_ra_id = Wire(U.w(32))
        regfile_data_rb_id = Wire(U.w(32))
        regfile_data_rc_id = Wire(U.w(32))

        # ALU control
        alu_en = Wire(Bool)
        alu_operator = Wire(U.w(ALU_OP_WIDTH))
        alu_op_a_mux_sel = Wire(U.w(3))
        alu_op_b_mux_sel = Wire(U.w(3))
        alu_op_c_mux_sel = Wire(U.w(2))
        regc_mux = Wire(U.w(2))

        imm_a_mux_sel = Wire(Bool)
        imm_b_mux_sel = Wire(U.w(4))
        ctrl_transfer_target_mux_sel = Wire(U.w(2))

        # Multiplier Control
        mult_operator = Wire(U.w(MUL_OP_WIDTH))         # Multiplication operation selection
        mult_en = Wire(Bool)                            # Multiplication is used instead of ALU
        mult_int_en = Wire(Bool)                        # Use integer multiplier
        # mult_sel_subword = Wire(Bool)                  # Select a subword when doing multiplications
        mult_signed_mode = Wire(U.w(2))                 # Signed mode multiplication at the output of the controller,
                                                        # and before the pipe registers

        # Register Write Control
        regfile_we_id = Wire(Bool)
        regfile_alu_waddr_mux_sel = Wire(Bool)

        # Data Memory control
        data_we_id = Wire(Bool)
        data_type_id = Wire(U.w(2))
        data_sign_ext_id = Wire(U.w(2))
        data_reg_offset_id = Wire(U.w(2))
        data_req_id = Wire(Bool)
        data_load_event_id = Wire(Bool)

        # CSR control
        csr_access = Wire(Bool)
        csr_op = Wire(U.w(CSR_OP_WIDTH))
        csr_status = Wire(Bool)

        prepost_useincr = Wire(Bool)

        # Forwarding
        operand_a_fw_mux_sel = Wire(U.w(2))
        operand_b_fw_mux_sel = Wire(U.w(2))
        operand_c_fw_mux_sel = Wire(U.w(2))
        operand_a_fw_id = Wire(U.w(32))
        operand_b_fw_id = Wire(U.w(32))
        operand_c_fw_id = Wire(U.w(32))

        operand_b = Wire(U.w(32))
        operand_c = Wire(U.w(32))
        alu_operand_a, alu_operand_b, alu_operand_c = [Wire(U.w(32)) for _ in range(3)]

        # Immediates for ID
        bmask_a_mux = Wire(Bool)
        bmask_b_mux = Wire(U.w(2))
        alu_bmask_a_mux_sel = Wire(Bool)
        alu_bmask_b_mux_sel = Wire(Bool)
        mult_imm_mux = Wire(Bool)

        bmask_a_id_imm = Wire(U.w(5))
        bmask_b_id_imm = Wire(U.w(5))
        bmask_a_id = Wire(U.w(5))
        bmask_b_id = Wire(U.w(5))
        imm_vec_ext_id = Wire(U.w(2))
        mult_imm_id = Wire(U.w(5))

        # Forwarding detection signals
        reg_d_ex_is_reg_a_id = Wire(Bool)
        reg_d_ex_is_reg_b_id = Wire(Bool)
        reg_d_ex_is_reg_c_id = Wire(Bool)
        reg_d_wb_is_reg_a_id = Wire(Bool)
        reg_d_wb_is_reg_b_id = Wire(Bool)
        reg_d_wb_is_reg_c_id = Wire(Bool)
        reg_d_alu_is_reg_a_id = Wire(Bool)
        reg_d_alu_is_reg_b_id = Wire(Bool)
        reg_d_alu_is_reg_c_id = Wire(Bool)

        is_clpx, is_subrot = [Wire(Bool) for _ in range(2)]

        mret_dec, uret_dec, dret_dec = [Wire(Bool) for _ in range(3)]

        # Performance counters
        id_valid_q = Wire(Bool)
        minstret = Wire(Bool)
        perf_pipeline_stall = Wire(Bool)

        instr <<= io.instr_rdata_i

        # Immediate extraction and sign extension
        imm_i_type <<= CatBits(sign_extension(instr[31], 20), instr[31:20])
        imm_iz_type <<= CatBits(U.w(20)(0), instr[31:20])
        imm_s_type <<= CatBits(sign_extension(instr[31], 20), instr[31:25], instr[11:7])
        imm_sb_type <<= CatBits(sign_extension(instr[31], 19), instr[31], instr[7], instr[30:25], instr[11:8], U.w(1)(0))
        imm_u_type <<= CatBits(instr[31:12], U.w(12)(0))
        imm_uj_type <<= CatBits(sign_extension(instr[31], 12), instr[19:12], instr[20], instr[30:21], U.w(1)(0))

        # Immediate for CSR manipulation (zero extended)
        imm_z_type <<= CatBits(U.w(27)(0), instr[REG_S1_MSB:REG_S1_LSB])

        imm_s2_type <<= CatBits(U.w(27)(0), instr[24:20])
        imm_bi_type <<= CatBits(sign_extension(instr[24], 27), instr[24:20])
        imm_s3_type <<= CatBits(U.w(27)(0), instr[29:25])
        imm_vs_type <<= CatBits(sign_extension(instr[24], 26), instr[24:20], instr[25])
        imm_vu_type <<= CatBits(U.w(26)(0), instr[24:20], instr[25])

        # Same format as RS2 for shuffle needs, expands immediate
        imm_shuffleb_type <<= CatBits(U.w(6)(0), instr[28:27], U.w(6)(0), instr[24:23], U.w(6)(0), instr[22:21],
                                      U.w(6)(0), instr[20], instr[25])
        imm_shuffleh_type <<= CatBits(U.w(15)(0), instr[20], U.w(15)(0), instr[25])

        # clipping immediate, uses a small barrel shifter to pre-process the
        # immediate and an adder to subtract 1
        # The end result is a mask that has 1's set in the lower part
        imm_clip_type <<= (U.w(32)(1) << instr[24:20]) - U(1)

        # Source register selection
        regfile_addr_ra_id <<= CatBits(U.w(1)(0), instr[REG_S1_MSB:REG_S1_LSB])
        regfile_addr_rb_id <<= CatBits(U.w(1)(0), instr[REG_S2_MSB:REG_S2_LSB])

        # Register C mux
        regfile_addr_rc_id <<= LookUpTable(regc_mux, {
            REGC_ZERO: U(0),
            REGC_RD: instr[REG_D_MSB:REG_D_LSB],
            REGC_S1: instr[REG_S1_MSB:REG_S1_LSB],
            REGC_S4: instr[REG_S4_MSB:REG_S4_LSB],
            ...: U(0)
        })

        # Destination registers
        regfile_waddr_id <<= CatBits(U.w(1)(0), instr[REG_D_MSB:REG_D_LSB])

        # Second register write address selection
        # Used for prepost load/store and multiplier
        regfile_alu_waddr_id <<= Mux(regfile_alu_waddr_mux_sel, regfile_waddr_id, regfile_addr_ra_id)

        # Forwarding control signals
        reg_d_ex_is_reg_a_id <<= (io.regfile_waddr_ex_o == regfile_addr_ra_id) & rega_used_dec & (regfile_addr_ra_id != U(0))
        reg_d_ex_is_reg_b_id <<= (io.regfile_waddr_ex_o == regfile_addr_rb_id) & regb_used_dec & (regfile_addr_rb_id != U(0))
        reg_d_ex_is_reg_c_id <<= (io.regfile_waddr_ex_o == regfile_addr_rc_id) & regc_used_dec & (regfile_addr_rc_id != U(0))
        reg_d_wb_is_reg_a_id <<= (io.regfile_waddr_wb_i == regfile_addr_ra_id) & rega_used_dec & (regfile_addr_ra_id != U(0))
        reg_d_wb_is_reg_b_id <<= (io.regfile_waddr_wb_i == regfile_addr_rb_id) & regb_used_dec & (regfile_addr_rb_id != U(0))
        reg_d_wb_is_reg_c_id <<= (io.regfile_waddr_wb_i == regfile_addr_rc_id) & regc_used_dec & (regfile_addr_rc_id != U(0))
        reg_d_alu_is_reg_a_id <<= (io.regfile_alu_waddr_fw_i == regfile_addr_ra_id) & rega_used_dec & (regfile_addr_ra_id != U(0))
        reg_d_alu_is_reg_b_id <<= (io.regfile_alu_waddr_fw_i == regfile_addr_rb_id) & regb_used_dec & (regfile_addr_rb_id != U(0))
        reg_d_alu_is_reg_c_id <<= (io.regfile_alu_waddr_fw_i == regfile_addr_rc_id) & regc_used_dec & (regfile_addr_rc_id != U(0))

        # Kill instruction in the IF/ID stage by setting the instr_valid_id control
        # Signal to 0 for instructions that are done
        io.clear_instr_valid_o <<= io.id_ready_o | halt_id | branch_taken_ex
        branch_taken_ex <<= io.branch_in_ex_o & io.branch_decision_i

        mult_en <<= mult_int_en

        # Jump target
        jump_target <<= LookUpTable(ctrl_transfer_target_mux_sel, {
            JT_JAL: io.pc_id_i + imm_uj_type,
            JT_COND: io.pc_id_i + imm_sb_type,
            JT_JALR: regfile_data_ra_id + imm_i_type,   # Cannot forward RS1, since the path is too long
            ...: regfile_data_ra_id + imm_i_type
        })
        io.jump_target_o <<= jump_target

        # Operand A
        # ALU_Op_a Mux
        alu_operand_a <<= LookUpTable(alu_op_a_mux_sel, {
            OP_A_REGA_OR_FWD: operand_a_fw_id,
            OP_A_REGB_OR_FWD: operand_b_fw_id,
            OP_A_REGC_OR_FWD: operand_c_fw_id,
            OP_A_CURRPC: io.pc_id_i,
            OP_A_IMM: imm_a,
            ...: operand_a_fw_id
        })

        imm_a <<= LookUpTable(imm_a_mux_sel, {
            IMMA_Z: imm_z_type,
            IMMA_ZERO: U(0),
            ...: U(0)
        })

        # Operand a forwarding mux
        operand_a_fw_id <<= LookUpTable(operand_a_fw_mux_sel, {
            SEL_FW_EX: io.regfile_alu_wdata_fw_i,
            SEL_FW_WB: io.regfile_wdata_wb_i,
            SEL_REGFILE: regfile_data_ra_id,
            ...: regfile_data_ra_id
        })

        # Operand B
        # Immediate Mux for operand B
        imm_b <<= LookUpTable(imm_b_mux_sel, {
            IMMB_I: imm_i_type,
            IMMB_S: imm_s_type,
            IMMB_U: imm_u_type,
            IMMB_PCINCR: Mux(io.is_compressed_i, U.w(32)(2), U.w(32)(4)),
            IMMB_S2: imm_s2_type,
            IMMB_BI: imm_bi_type,
            IMMB_S3: imm_s3_type,
            IMMB_VS: imm_vs_type,
            IMMB_VU: imm_vu_type,
            IMMB_SHUF: imm_shuffle_type,
            IMMB_CLIP: CatBits(U.w(1)(0), imm_clip_type[31:1]),
            ...: imm_i_type
        })

        # ALU_Op_b Mux
        operand_b <<= LookUpTable(alu_op_b_mux_sel, {
            OP_B_REGA_OR_FWD: operand_a_fw_id,
            OP_B_REGB_OR_FWD: operand_b_fw_id,
            OP_B_REGC_OR_FWD: operand_c_fw_id,
            OP_B_IMM: imm_b,
            OP_B_BMASK: operand_b_fw_id[4:0].to_uint(),
            ...: operand_b_fw_id
        })

        imm_shuffle_type <<= imm_shuffleh_type
        alu_operand_b <<= operand_b

        # Operand B forwarding Mux
        operand_b_fw_id <<= LookUpTable(operand_b_fw_mux_sel, {
            SEL_FW_EX: io.regfile_alu_wdata_fw_i,
            SEL_FW_WB: io.regfile_wdata_wb_i,
            SEL_REGFILE: regfile_data_rb_id,
            ...: regfile_data_rb_id
        })

        # Operand C
        # ALU OP C Mux
        operand_c <<= LookUpTable(alu_op_c_mux_sel, {
            OP_C_REGC_OR_FWD: operand_c_fw_id,
            OP_C_REGB_OR_FWD: operand_b_fw_id,
            OP_C_JT: jump_target,
            ...: operand_c_fw_id
        })

        alu_operand_c <<= operand_c

        # Operand c forwarding Mux
        operand_a_fw_id <<= LookUpTable(operand_c_fw_mux_sel, {
            SEL_FW_EX: io.regfile_alu_wdata_fw_i,
            SEL_FW_WB: io.regfile_wdata_wb_i,
            SEL_REGFILE: regfile_data_rc_id,
            ...: regfile_data_rc_id
        })

        # Immediates ID
        bmask_a_id_imm <<= LookUpTable(bmask_a_mux, {
            BMASK_A_ZERO: U(0),
            BMASK_A_S3: imm_s3_type[4:0],
            ...: U(0)
        })

        bmask_b_id_imm <<= LookUpTable(bmask_b_mux, {
            BMASK_B_ZERO: U(0),
            BMASK_B_ONE: U.w(5)(1),
            BMASK_B_S2: imm_s2_type[4:0],
            BMASK_B_S3: imm_s3_type[4:0],
            ...: U(0)
        })

        bmask_a_id <<= LookUpTable(alu_bmask_a_mux_sel, {
            BMASK_A_IMM: bmask_a_id_imm,
            BMASK_A_REG: operand_b_fw_id[9:5],
            ...: bmask_a_id_imm
        })

        bmask_b_id <<= LookUpTable(alu_bmask_b_mux_sel, {
            BMASK_B_IMM: bmask_b_id_imm,
            BMASK_B_REG: operand_b_fw_id[4:0],
            ...: bmask_b_id_imm
        })

        imm_vec_ext_id <<= imm_vu_type[1:0]

        mult_imm_id <<= LookUpTable(mult_imm_mux, {
            MIMM_ZERO: U(0),
            MIMM_S3: imm_s3_type[4:0],
            ...: U(0)
        })

        # Deprecated APU

        # Initial modules
        rf = register_file(ADDR_WIDTH=6, DATA_WIDTH=32)
        de = decoder(PULP_SECURE=PULP_SECURE, USE_PMP=USE_PMP, DEBUG_TRIGGER_EN=DEBUG_TRIGGER_EN)
        co = controller()
        int_co = int_controller()

        ##################################################################################
        # Registers
        ##################################################################################
        rf.io.scan_cg_en_i <<= io.scan_cg_en_i

        # Read port a
        rf.io.raddr_a_i <<= regfile_addr_ra_id
        regfile_data_ra_id <<= rf.io.rdata_a_o

        # Read port b
        rf.io.raddr_b_i <<= regfile_addr_rb_id
        regfile_data_rb_id <<= rf.io.rdata_b_o

        # Read port c
        rf.io.raddr_c_i <<= regfile_addr_rc_id
        regfile_data_rc_id <<= rf.io.rdata_c_o

        # Write port a
        rf.io.waddr_a_i <<= io.regfile_waddr_wb_i
        rf.io.wdata_a_i <<= io.regfile_wdata_wb_i
        rf.io.we_a_i <<= io.regfile_we_wb_i

        # Write port b
        rf.io.waddr_b_i <<= io.regfile_alu_waddr_fw_i
        rf.io.wdata_b_i <<= io.regfile_alu_wdata_fw_i
        rf.io.we_b_i <<= io.regfile_alu_we_fw_i

        ##################################################################################
        # Decoder
        ##################################################################################
        # Ref io port
        de_io = de.io

        # Controller related signals
        de_io.deassert_we_i <<= deassert_we

        illegal_insn_dec <<= de_io.illegal_insn_o
        ebrk_insn_dec <<= de_io.ebrk_insn_o

        mret_insn_dec <<= de_io.mret_insn_o
        uret_insn_dec <<= de_io.uret_insn_o
        dret_insn_dec <<= de_io.dret_insn_o

        ecall_insn_dec <<= de_io.call_insn_o
        wfi_insn_dec <<= de_io.wfi_o

        fencei_insn_dec <<= de_io.fencei_insn_o

        rega_used_dec <<= de_io.rega_used_o
        regb_used_dec <<= de_io.regb_used_o
        regc_used_dec <<= de_io.regc_used_o

        # TODO: Temporary set zero
        bmask_a_mux <<= BMASK_A_ZERO
        bmask_b_mux <<= BMASK_B_ZERO
        alu_bmask_a_mux_sel <<= BMASK_A_REG
        alu_bmask_b_mux_sel <<= BMASK_B_REG

        # From IF/ID pipeline
        de_io.instr_rdata_i <<= instr
        de_io.illegal_c_insn_i <<= io.illegal_c_insn_i

        # ALU signals
        alu_en <<= de_io.alu_en_o
        alu_operator <<= de_io.alu_operator_o
        alu_op_a_mux_sel <<= de_io.alu_op_a_mux_sel_o
        alu_op_b_mux_sel <<= de_io.alu_op_b_mux_sel_o
        alu_op_c_mux_sel <<= de_io.alu_op_c_mux_sel_o
        imm_a_mux_sel <<= de_io.imm_a_mux_sel_o
        imm_b_mux_sel <<= de_io.imm_b_mux_sel_o
        regc_mux <<= de_io.regc_mux_o

        mult_operator <<= de_io.mult_operator_o
        mult_int_en <<= de_io.mult_int_en_o
        # mult_sel_subword <<= de_io.mult_sel_subword_o
        mult_signed_mode <<= de_io.mult_signed_mode_o
        mult_imm_mux <<= de_io.mult_imm_mux_o

        # Deprecated FPU / APU signals

        # Register file control signals
        regfile_we_id <<= de_io.regfile_mem_we_o
        regfile_alu_we_id <<= de_io.regfile_alu_we_o
        regfile_alu_we_dec_id <<= de_io.regfile_alu_we_dec_o
        regfile_alu_waddr_mux_sel <<= de_io.regfile_alu_waddr_sel_o

        # CSR control signals
        csr_access <<= de_io.csr_access_o
        csr_status <<= de_io.csr_status_o
        csr_op <<= de_io.csr_op_o
        de_io.current_priv_lvl_i <<= io.current_priv_lvl_i

        # Data bus interface
        data_req_id <<= de_io.data_req_o
        data_we_id <<= de_io.data_we_o
        prepost_useincr <<= de_io.prepost_useincr_o
        data_type_id <<= de_io.data_type_o
        data_sign_ext_id <<= de_io.data_sign_extension_o
        data_reg_offset_id <<= de_io.data_reg_offset_o

        # Debug mode
        de_io.debug_mode_i <<= io.debug_mode_o
        de_io.debug_wfi_no_sleep_i <<= debug_wfi_no_sleep

        # Jump/Branches
        ctrl_transfer_insn_in_dec <<= de_io.ctrl_transfer_insn_in_dec_o
        ctrl_transfer_insn_in_id <<= de_io.ctrl_transfer_insn_in_id_o
        ctrl_transfer_target_mux_sel <<= de_io.ctrl_transfer_target_mux_sel_o

        # HPM related control signals
        de_io.mcounteren_i <<= io.mcounteren_i

        ##################################################################################
        # Controller
        ##################################################################################
        # TODO: Gated clock
        co_io = co.io

        co_io.fetech_enable_i <<= io.fetch_enable_i
        io.ctrl_busy_o <<= co_io.ctrl_busy_o
        io.is_decoding_o <<= co_io.is_decoding_o
        co_io.is_fetch_failed_o <<= io.is_fetch_failed_i

        # Decoder related signals
        deassert_we <<= co_io.deassert_we_o
        co_io.illegal_insn_i <<= illegal_insn_dec
        co_io.ecall_insn_i <<= ecall_insn_dec
        co_io.mret_insn_i <<= mret_insn_dec
        co_io.uret_insn_i <<= uret_insn_dec

        co_io.dret_insn_i <<= dret_insn_dec

        co_io.mret_dec_i <<= mret_dec
        co_io.uret_dec_i <<= uret_dec
        co_io.dret_dec_i <<= dret_dec

        co_io.wfi_i <<= wfi_insn_dec
        co_io.ebrk_insn_i <<= ebrk_insn_dec
        co_io.fencei_insn_i <<= fencei_insn_dec
        co_io.csr_status_i <<= csr_status

        # From IF/ID pipeline
        co_io.instr_valid_i <<= io.instr_valid_i

        # From prefetcher
        io.instr_req_o <<= co_io.instr_req_o

        # To prefetcher
        io.pc_set_o <<= co_io.pc_set_o
        io.pc_mux_o <<= co_io.pc_mux_o
        io.exc_pc_mux_o <<= co_io.exc_pc_mux_o
        io.exc_cause_o <<= co_io.exc_cuase_o
        io.trap_addr_mux_o <<= co_io.trap_addr_mux_o

        # LSU
        co_io.data_req_ex_i <<= io.data_req_ex_o
        co_io.data_we_ex_i <<= io.data_we_ex_o
        co_io.data_misaligned_i <<= io.data_misaligned_i
        co_io.data_load_event_i <<= data_load_event_id
        co_io.data_err_i <<= io.data_err_i
        io.data_err_ack_o <<= co_io.data_err_ack_o

        # ALU
        co_io.mult_multicycle_i <<= io.mult_multicycle_i

        # Jump/Branch control
        co_io.branch_taken_ex_i <<= branch_taken_ex
        co_io.ctrl_transfer_insn_in_id_i <<= ctrl_transfer_insn_in_id
        co_io.ctrl_transfer_insn_in_dec_i <<= ctrl_transfer_insn_in_dec

        # Interrupt signals
        co_io.irq_wu_ctrl_i <<= irq_wu_ctrl
        co_io.irq_req_ctrl_i <<= irq_req_ctrl
        co_io.irq_sec_ctrl_i <<= irq_sec_ctrl
        co_io.irq_id_ctrl_i <<= irq_id_ctrl
        co_io.current_priv_lvl_i <<= io.current_priv_lvl_i
        io.irq_ack_o <<= co_io.irq_ack_o
        io.irq_id_o <<= co_io.irq_id_o

        # Debug signals
        io.debug_mode_o <<= co_io.debug_mode_o
        io.debug_cause_o <<= co_io.debug_cause_o
        io.debug_csr_save_o <<= co_io.debug_csr_save_o
        co_io.debug_req_i <<= io.debug_req_i
        co_io.debug_single_step_i <<= io.debug_single_step_i
        co_io.debug_ebreakm_i <<= io.debug_ebreakm_i
        co_io.debug_ebreaku_i <<= io.debug_ebreaku_i
        co_io.trigger_match_i <<= io.trigger_match_i
        io.debug_p_elw_no_sleep_o <<= co_io.debug_p_elw_no_sleep_o
        debug_wfi_no_sleep <<= co_io.debug_wfi_no_sleep_o
        io.debug_havereset_o <<= co_io.debug_havereset_o
        io.debug_running_o <<= co_io.debug_running_o
        io.debug_halted_o <<= co_io.debug_halted_o

        # Wakeup signal
        io.wake_from_sleep_o <<= co_io.wake_from_sleep_o

        # CSR controller signals
        io.csr_save_cause_o <<= co_io.csr_save_cause_o
        io.csr_cause_o <<= co_io.csr_cause_o
        io.csr_save_if_o <<= co_io.csr_save_if_o
        io.csr_save_id_o <<= co_io.csr_save_id_o
        io.csr_save_ex_o <<= co_io.csr_save_ex_o
        io.csr_restore_mret_id_o <<= co_io.csr_restore_mret_id_o
        io.csr_restore_uret_id_o <<= co_io.csr_restore_uret_id_o

        io.csr_restore_dret_id_o <<= co_io.csr_restore_dret_id_o

        io.csr_irq_sec_o <<= co_io.csr_irq_sec_o

        # Write targets from ID
        co_io.regfile_we_id_i <<= regfile_alu_we_id
        co_io.regfile_alu_waddr_id_i <<= regfile_alu_waddr_id

        # Forwarding signals from regfile
        co_io.regfile_we_ex_i <<= io.regfile_we_ex_o
        co_io.regfile_waddr_ex_i <<= io.regfile_waddr_ex_o
        co_io.regfile_we_wb_i <<= io.regfile_we_wb_i

        # Regfile port 2
        co_io.regfile_alu_we_fw_i <<= io.regfile_alu_we_fw_i

        # Forwarding detection signals
        co_io.reg_d_ex_is_reg_a_i <<= reg_d_ex_is_reg_a_id
        co_io.reg_d_ex_is_reg_b_i <<= reg_d_ex_is_reg_b_id
        co_io.reg_d_ex_is_reg_c_i <<= reg_d_ex_is_reg_c_id
        co_io.reg_d_wb_is_reg_a_i <<= reg_d_wb_is_reg_a_id
        co_io.reg_d_wb_is_reg_b_i <<= reg_d_wb_is_reg_b_id
        co_io.reg_d_wb_is_reg_c_i <<= reg_d_wb_is_reg_c_id
        co_io.reg_d_alu_is_reg_a_i <<= reg_d_alu_is_reg_a_id
        co_io.reg_d_alu_is_reg_b_i <<= reg_d_alu_is_reg_b_id
        co_io.reg_d_alu_is_reg_c_i <<= reg_d_alu_is_reg_c_id

        # Forwarding signals
        operand_a_fw_mux_sel <<= co_io.operand_a_fw_mux_sel_o
        operand_b_fw_mux_sel <<= co_io.operand_b_fw_mux_sel_o
        operand_c_fw_mux_sel <<= co_io.operand_c_fw_mux_sel_o

        # Stall signals
        halt_if <<= co_io.halt_if_o
        halt_id <<= co_io.halt_id_o

        misaligned_stall <<= co_io.misaligned_stall_o
        jr_stall <<= co_io.jr_stall_o
        load_stall <<= co_io.load_stall_o

        co_io.id_ready_i <<= io.id_ready_o
        co_io.id_valid_i <<= io.id_valid_o

        co_io.ex_valid_i <<= io.ex_valid_i
        co_io.wb_ready_i <<= io.wb_ready_i

        perf_pipeline_stall <<= co_io.perf_pipeline_stall_o

        ##################################################################################
        # Interrupt Controller
        ##################################################################################
        # External interrupt lines
        int_co.io.irq_i <<= io.irq_i
        int_co.io.irq_sec_i <<= io.irq_sec_i

        # To controller
        irq_req_ctrl <<= int_co.io.irq_req_ctrl_o
        irq_sec_ctrl <<= int_co.io.irq_sec_ctrl_o
        irq_id_ctrl <<= int_co.io.irq_id_ctrl_o
        irq_wu_ctrl <<= int_co.io.irq_wu_ctrl_o

        # To/from registers
        int_co.io.mie_bypass_i <<= io.mie_bypass_i
        io.mip_o <<= int_co.io.mip_o
        int_co.io.m_ie_i <<= io.m_irq_enable_i
        int_co.io.u_ie_i <<= io.u_irq_enable_i
        int_co.io.current_priv_lvl_i <<= io.current_priv_lvl_i

        ##################################################################################
        # ID/EX pipeline
        ##################################################################################

    return ID_STAGE()
