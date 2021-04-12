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
   Date: 2021-04-12
   File Name: core.py
   Description: Top level module of the RISC-V core.
"""
from pyhcl import *
from src.include.pkg import *
from src.rtl.if_stage import *
from src.rtl.id_stage import *
from src.rtl.ex_stage import *
from src.rtl.load_store_unit import *


def core(NUM_MHPMCOUNTERS=1):
    class CORE(Module):
        io = IO(
            scan_cg_en_i=Input(Bool),                           # Enable all clock gates for testing

            # Core ID, Cluster ID, debug mode halt address and boot address are considered more or less static
            boot_addr_i=Input(U.w(32)),
            mtvec_addr_i=Input(U.w(32)),
            dm_halt_addr_i=Input(U.w(32)),
            hart_id_i=Input(U.w(32)),
            dm_exception_addr_i=Input(U.w(32)),

            # Instruction memory interface
            instr_req_o=Output(Bool),
            instr_gnt_i=Input(Bool),
            instr_rvalid_i=Input(Bool),
            instr_addr_o=Output(U.w(32)),

            # Data memory interface
            data_req_o=Output(Bool),
            data_gnt_i=Input(Bool),
            data_rvalid_i=Input(Bool),
            data_we_o=Output(Bool),
            data_be_o=Output(U.w(6)),
            data_addr_o=Output(U.w(32)),
            data_wdata_o=Output(U.w(32)),
            data_rdata_o=Output(U.w(32)),

            # Interrupt inputs
            irq_i=Input(U.w(32)),
            irq_ack_o=Output(Bool),
            irq_id_o=Output(U.w(5)),

            # Debug Interface
            debug_req_i=Input(Bool),
            debug_havereset_o=Output(Bool),
            debug_running_o=Output(Bool),
            debug_halted_o=Output(Bool),

            # CPU Control signals
            fetch_enable_i=Input(Bool),
            core_sleep_o=Output(Bool)
        )
        if_stage_i = if_stage().io
        id_stage_i = id_stage().io
        ex_stage_i = ex_stage().io
        load_store_unit_i = load_store_unit().io

        irq_sec_i = Wire(Bool)
        sec_lvl_o = Wire(Bool)

        # IF/ID signals
        instr_valid_id = Wire(Bool)
        instr_rdata_id = Wire(U.w(32))                  # Instruction sampled inside IF stage
        is_compressed_id = Wire(Bool)
        illegal_c_insn_id = Wire(Bool)
        is_fetch_failed_id = Wire(Bool)

        clear_instr_valid = Wire(Bool)
        pc_set = Wire(Bool)

        pc_mux_id = Wire(U.w(4))                        # Mux selector for next PC
        exc_pc_mux_id = Wire(U.w(3))                    # Mux selector for exception PC
        m_exc_vec_pc_mux_id = Wire(U.w(5))              # Mux selector for vectored IRQ PC
        u_exc_vec_pc_mux_id = Wire(U.w(5))              # Mux selector for vectored IRQ PC
        exc_cause = Wire(U.w(5))

        trap_addr_mux = Wire(U.w(2))

        pc_if = Wire(U.w(32))                           # Program counter in IF stage
        pc_id = Wire(U.w(32))                           # Program counter in ID stage

        # ID performance counter signals
        is_decoding = Wire(Bool)

        useincr_addr_ex = Wire(Bool)                    # Active when post increment
        data_misaligned = Wire(Bool)

        mult_multicycle = Wire(Bool)

        # Jump and branch target and decision (EX->IF)
        jump_target_id, jump_target_ex = [Wire(U.w(32)) for _ in range(2)]
        branch_in_ex = Wire(Bool)
        branch_decision = Wire(Bool)

        ctrl_busy = Wire(Bool)
        if_busy = Wire(Bool)
        lsu_busy = Wire(Bool)

        pc_ex = Wire(U.w(32))                           # PC of last executed branch

        # ALU control
        alu_en_ex = Wire(Bool)
        alu_operator_ex = Wire(U.w(ALU_OP_WIDTH))
        alu_operand_a_ex = Wire(U.w(32))
        alu_operand_b_ex = Wire(U.w(32))
        alu_operand_c_ex = Wire(U.w(32))
        imm_vec_ext_ex = Wire(U.w(2))

        # Multiplier control
        mult_operator_ex = Wire(U.w(MUL_OP_WIDTH))
        mult_operand_a_ex = Wire(U.w(32))
        mult_operand_b_ex = Wire(U.w(32))
        mult_operand_c_ex = Wire(U.w(32))
        mult_en_ex = Wire(Bool)
        mult_signed_mode_ex = Wire(U.w(2))
        mult_imm_ex = Wire(U.w(5))

        # Register Write Control
        regfile_waddr_ex = Wire(U.w(6))
        regfile_we_ex = Wire(Bool)
        regfile_waddr_fw_wb_o = Wire(U.w(6))
        regfile_we_wb = Wire(Bool)
        regfile_wdata - Wire(U.w(32))

        regfile_alu_waddr_ex = Wire(U.w(6))
        regfile_alu_we_ex = Wire(Bool)

        regfile_alu_waddr_fw = Wire(U.w(6))
        regfile_alu_we_fw = Wire(Bool)
        regfile_alu_wdata_fw = Wire(U.w(32))

        # CSR control
        csr_access_ex = Wire(Bool)
        csr_op_ex = Wire(U.w(CSR_OP_WIDTH))
        mtvec, utvec = [Wire(U.w(24)) for _ in range(2)]
        mtvec_mode, utvec_mode = [Wire(U.w(2)) for _ in range(2)]

        csr_op = Wire(U.w(CSR_OP_WIDTH))
        csr_addr = Wire(U.w(CSR_NUM_WIDTH))
        csr_addr_int = Wire(U.w(CSR_NUM_WIDTH))
        csr_rdata, csr_wdata = [Wire(U.w(32)) for _ in range(2)]
        current_priv_lvl = Wire(U.w(PRIV_SEL_WIDTH))

        # Data Memory Control: From ID stage (id-ex pipe <--> load store unit)
        data_we_ex = Wire(Bool)
        data_type_ex = Wire(U.w(2))
        data_sign_ext_ex = Wire(U.w(2))
        data_reg_offset_ex = Wire(U.w(2))
        data_req_ex = Wire(Bool)
        data_load_event_ex = Wire(Bool)
        data_misaligned_ex = Wire(Bool)

        p_elw_start, p_elw_finish = [Wire(Bool) for _ in range(2)]

        lsu_rdata = Wire(U.w(32))

        # Stall control
        halt_if, id_ready, ex_ready, id_valid, ex_valid, wb_valid, lsu_ready_ex, lsy_ready_wb = [Wire(Bool) for _ in range(8)]

        # Signals between instruction core interface and pipe (if and id stages)
        instr_req_int = Wire(Bool)      # Id stage asserts a req to instruction core interface

        # Interrupts
        m_irq_enable, u_ir_enable = [Wire(Bool) for _ in range(2)]
        csr_irq_sec = Wire(Bool)
        mepc, uepc, depc = [Wire(U.w(32)) for _ in range(3)]
        mie_bypass = Wire(U.w(32))
        mip = Wire(U.w(32))

        csr_save_cause, csr_save_if, csr_save_id, csr_save_ex = [Wire(Bool) for _ in range(4)]
        csr_cause = Wire(U.w(6))
        csr_restore_mret_id, csr_restore_uret_id, csr_restore_dret_id = [Wire(Bool) for _ in range(3)]
        csr_mtvec_init = Wire(Bool)

        # HPM related control signals
        mcounteren = Wire(U.w(32))

        # Debug mode and dcsr configuration
        debug_mode = Wire(Bool)
        debug_cause = Wire(U.w(3))
        debug_csr_save, debug_sigle_Step, debug_ebreakm, debug_ebreaku, trigger_match = [Wire(bool) for _ in range(5)]

        # Performance Counters
        mhpmevent_minstret = Wire(Bool)
        mhpmevent_load = Wire(Bool)
        mhpmevent_store = Wire(Bool)
        mhpmevent_jump = Wire(Bool)
        mhpmevent_branch = Wire(Bool)
        mhpmevent_branch_taken = Wire(Bool)
        mhpmevent_compressed = Wire(Bool)
        mhpmevent_jr_stall = Wire(Bool)
        mhpmevent_imiss = Wire(Bool)
        mhpmevent_ld_stall = Wire(Bool)
        mhpmevent_pipe_stall = Wire(Bool)
        
        perf_imiss = Wire(Bool)

        # Wake signal
        wake_from_sleep = Wire(Bool)

        # Mux selector for vectored IRQ PC
        m_exc_vec_pc_mux_id <<= Mux(mtvec_mode == U(0), U(0), exc_cause)
        u_exc_vec_pc_mux_id <<= Mux(mtvec_mode == U(0), U(0), exc_cause)

        # PULP_SECURE == 0
        irq_sec_i <<= Bool(False)

    return CORE()
