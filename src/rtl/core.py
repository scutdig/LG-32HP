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
            instr_rdata_i=Input(U.w(32)),

            # Data memory interface
            data_req_o=Output(Bool),
            data_gnt_i=Input(Bool),
            data_rvalid_i=Input(Bool),
            data_we_o=Output(Bool),
            data_be_o=Output(U.w(6)),
            data_addr_o=Output(U.w(32)),
            data_wdata_o=Output(U.w(32)),
            data_rdata_i=Input(U.w(32)),

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
        regfile_wdata = Wire(U.w(32))

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
        halt_if, id_ready, ex_ready, id_valid, ex_valid, wb_valid, lsu_ready_ex, lsu_ready_wb = [Wire(Bool) for _ in range(8)]

        # Signals between instruction core interface and pipe (if and id stages)
        instr_req_int = Wire(Bool)      # Id stage asserts a req to instruction core interface

        # Interrupts
        m_irq_enable, u_irq_enable = [Wire(Bool) for _ in range(2)]
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
        debug_csr_save, debug_sigle_Step, debug_ebreakm, debug_ebreaku, trigger_match = [Wire(Bool) for _ in range(5)]

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

        # PMP signals, but no use, just pass through
        data_req_pmp, data_gnt_pmp, data_err_pmp, data_err_ack = [Wire(Bool) for _ in range(4)]
        instr_req_pmp, instr_gnt_pmp, instr_err_pmp = [Wire(Bool) for _ in range(3)]
        data_addr_pmp, instr_addr_pmp = [Wire(U.w(32)) for _ in range(2)]

        ##################################################################################
        # Clock Management
        ##################################################################################

        # PyHCL doesn't support multiple clocks right now
        # We may need to use the blackbox feature to implement Clock Management
        fetch_enable = Wire(Bool)

        io.core_sleep_o <<= Bool(False)
        fetch_enable <<= Bool(True)

        ##################################################################################
        # IF stage
        ##################################################################################
        # Boot address
        if_stage_i.boot_addr_i <<= io.boot_addr_i[31:0]
        if_stage_i.dm_exception_addr_i <<= io.dm_exception_addr_i[31:0]

        # Debug mode halt address
        if_stage_i.dm_halt_addr_i <<= io.dm_halt_addr_i[31:0]

        # Trap vector location
        if_stage_i.m_trap_base_addr_i <<= mtvec
        if_stage_i.u_trap_base_addr_i <<= utvec
        if_stage_i.trap_addr_mux_i <<= trap_addr_mux

        # Instruction request control
        if_stage_i.req_i <<= instr_req_int

        # Instruction cache interface
        instr_req_pmp <<= if_stage_i.instr_req_o
        instr_addr_pmp <<= if_stage_i.instr_addr_o
        if_stage_i.instr_gnt_i <<= instr_gnt_pmp
        if_stage_i.instr_rvalid_i <<= io.instr_rvalid_i
        if_stage_i.instr_rdata_i <<= io.instr_rdata_i
        if_stage_i.instr_err_i <<= Bool(False)
        if_stage_i.instr_err_pmp_i <<= instr_err_pmp

        # Outputs to ID stage
        instr_valid_id <<= if_stage_i.instr_valid_id_o
        instr_rdata_id <<= if_stage_i.instr_rdata_id_o
        is_fetch_failed_id <<= if_stage_i.is_fetch_failed_o

        # Control signals
        if_stage_i.clear_instr_valid_i <<= clear_instr_valid
        if_stage_i.pc_set_i <<= pc_set

        if_stage_i.mepc_i <<= mepc
        if_stage_i.uepc_i <<= uepc

        if_stage_i.depc_i <<= depc

        if_stage_i.pc_mux_i <<= pc_mux_id
        if_stage_i.exc_pc_mux_i <<= exc_pc_mux_id

        pc_id <<= if_stage_i.pc_id_o
        pc_if <<= if_stage_i.pc_if_o

        is_compressed_id <<= if_stage_i.is_compressed_id_o
        illegal_c_insn_id <<= if_stage_i.illegal_c_insn_id_o

        if_stage_i.m_exc_vec_pc_mux_i <<= m_exc_vec_pc_mux_id
        if_stage_i.u_exc_vec_pc_mux_i <<= u_exc_vec_pc_mux_id

        csr_mtvec_init <<= if_stage_i.csr_mtvec_init_o

        # No hwloop support
        if_stage_i.hwlp_jump_i <<= Bool(False)
        if_stage_i.hwlp_target_i <<= U(0)

        # Jump targets
        if_stage_i.jump_target_id_i <<= jump_target_id
        if_stage_i.jump_target_ex_i <<= jump_target_ex

        # Pipeline stalls
        if_stage_i.halt_if_i <<= halt_if
        if_stage_i.id_ready_i <<= id_ready

        if_busy <<= if_stage_i.if_busy_o
        perf_imiss <<= if_stage_i.perf_imiss_o

        ##################################################################################
        # ID stage
        ##################################################################################
        id_stage_i.scan_cg_en_i <<= io.scan_cg_en_i

        # Processor Enable
        id_stage_i.fetch_enable_i <<= fetch_enable
        ctrl_busy <<= id_stage_i.ctrl_busy_o
        is_decoding <<= id_stage_i.is_decoding_o

        # Interface to instruction memory
        id_stage_i.instr_valid_i <<= instr_valid_id
        id_stage_i.instr_rdata_i <<= instr_rdata_id
        instr_req_int <<= id_stage_i.instr_req_o

        # Jumps and branches
        branch_in_ex <<= id_stage_i.branch_in_ex_o
        id_stage_i.branch_decision_i <<= branch_decision
        jump_target_id <<= id_stage_i.jump_target_o

        # IF and ID control signals
        clear_instr_valid <<= id_stage_i.clear_instr_valid_o
        pc_set <<= id_stage_i.pc_set_o
        pc_mux_id <<= id_stage_i.pc_mux_o
        exc_pc_mux_id <<= id_stage_i.exc_pc_mux_o
        exc_cause <<= id_stage_i.exc_cause_o
        trap_addr_mux <<= id_stage_i.trap_addr_mux_o

        id_stage_i.is_fetch_failed_i <<= is_fetch_failed_id

        id_stage_i.pc_id_i <<= pc_id

        id_stage_i.is_compressed_i <<= is_compressed_id
        id_stage_i.illegal_c_insn_i <<= illegal_c_insn_id

        # Stalls
        halt_if <<= id_stage_i.halt_if_o

        id_ready <<= id_stage_i.id_ready_o
        id_stage_i.ex_ready_i <<= ex_ready
        id_stage_i.wb_ready_i <<= lsu_ready_wb

        id_valid <<= id_stage_i.id_valid_o
        id_stage_i.ex_valid_i <<= ex_valid

        # From the pipeline ID/EX
        pc_ex <<= id_stage_i.pc_ex_o

        alu_en_ex <<= id_stage_i.alu_en_ex_o
        alu_operator_ex <<= id_stage_i.alu_operator_ex_o
        alu_operand_a_ex <<= id_stage_i.alu_operand_a_ex_o
        alu_operand_b_ex <<= id_stage_i.alu_operand_b_ex_o
        alu_operand_c_ex <<= id_stage_i.alu_operand_c_ex_o
        imm_vec_ext_ex <<= id_stage_i.imm_vec_ext_ex_o

        regfile_waddr_ex <<= id_stage_i.regfile_waddr_ex_o
        regfile_we_ex <<= id_stage_i.regfile_we_ex_o

        regfile_alu_we_ex <<= id_stage_i.regfile_alu_we_ex_o
        regfile_alu_waddr_ex <<= id_stage_i.regfile_alu_waddr_ex_o

        # MUL
        mult_operator_ex <<= id_stage_i.mult_operator_ex_o
        mult_en_ex <<= id_stage_i.mult_en_ex_o
        mult_signed_mode_ex <<= id_stage_i.mult_signed_mode_ex_o
        mult_operand_a_ex <<= id_stage_i.mult_operand_a_ex_o
        mult_operand_b_ex <<= id_stage_i.mult_operand_b_ex_o
        mult_operand_c_ex <<= id_stage_i.mult_operand_c_ex_o
        mult_imm_ex <<= id_stage_i.mult_imm_ex_o

        # CSR ID/EX
        csr_access_ex <<= id_stage_i.csr_access_ex_o
        csr_op_ex <<= id_stage_i.csr_op_ex_o
        id_stage_i.current_priv_lvl_i <<= current_priv_lvl
        csr_irq_sec <<= id_stage_i.csr_irq_sec_o
        csr_cause <<= id_stage_i.csr_cause_o
        csr_save_if <<= id_stage_i.csr_save_if_o
        csr_save_id <<= id_stage_i.csr_save_id_o
        csr_save_ex <<= id_stage_i.csr_save_ex_o
        csr_restore_mret_id <<= id_stage_i.csr_restore_mret_id_o
        csr_restore_uret_id <<= id_stage_i.csr_restore_uret_id_o
        csr_restore_dret_id <<= id_stage_i.csr_restore_dret_id_o
        csr_save_cause <<= id_stage_i.csr_save_cause_o

        # LSU
        data_req_ex <<= id_stage_i.data_req_ex_o
        data_we_ex <<= id_stage_i.data_we_ex_o
        data_type_ex <<= id_stage_i.data_type_ex_o
        data_sign_ext_ex <<= id_stage_i.data_sign_ext_ex_o
        data_reg_offset_ex <<= id_stage_i.data_reg_offset_ex_o
        data_load_event_ex <<= id_stage_i.data_load_event_ex_o

        data_misaligned_ex <<= id_stage_i.data_misaligned_ex_o

        useincr_addr_ex <<= id_stage_i.prepost_useincr_ex_o
        id_stage_i.data_misaligned_i <<= data_misaligned
        id_stage_i.data_err_i <<= data_err_pmp
        data_err_ack <<= id_stage_i.data_err_ack_o

        # Interrupt Signals
        id_stage_i.irq_i <<= io.irq_i
        id_stage_i.irq_sec_i <<= Bool(False)
        id_stage_i.mie_bypass_i <<= mie_bypass
        mip <<= id_stage_i.mip_o
        id_stage_i.m_irq_enable_i <<= m_irq_enable
        id_stage_i.u_irq_enable_i <<= u_irq_enable
        io.irq_ack_o <<= id_stage_i.irq_ack_o
        io.irq_id_o <<= id_stage_i.irq_id_o

        # Debug signal
        debug_mode <<= id_stage_i.debug_mode_o
        debug_cause <<= id_stage_i.debug_cause_o
        debug_csr_save <<= id_stage_i.debug_csr_save_o
        id_stage_i.debug_req_i <<= io.debug_req_i
        io.debug_havereset_o <<= id_stage_i.debug_havereset_o
        io.debug_running_o <<= id_stage_i.debug_running_o
        io.debug_halted_o <<= id_stage_i.debug_halted_o
        id_stage_i.debug_single_step_i <<= debug_sigle_Step
        id_stage_i.debug_ebreakm_i <<= debug_ebreakm
        id_stage_i.debug_ebreaku_i <<= debug_ebreaku
        id_stage_i.trigger_match_i <<= trigger_match

        # Wakeup Signal
        wake_from_sleep <<= id_stage_i.wake_from_sleep_o

        # Forward Signals
        id_stage_i.regfile_waddr_wb_i <<= regfile_waddr_fw_wb_o
        id_stage_i.regfile_we_wb_i <<= regfile_we_wb
        id_stage_i.regfile_wdata_wb_i <<= regfile_wdata

        id_stage_i.regfile_alu_waddr_fw_i <<= regfile_alu_waddr_fw
        id_stage_i.regfile_alu_we_fw_i <<= regfile_alu_we_fw
        id_stage_i.regfile_alu_wdata_fw_i <<= regfile_alu_wdata_fw

        # From ALU
        id_stage_i.mult_multicycle_i <<= mult_multicycle

        # Performance Counters
        mhpmevent_minstret   <<= id_stage_i.mhpmevent_minstret_o
        mhpmevent_load       <<= id_stage_i.mhpmevent_load_o
        mhpmevent_store      <<= id_stage_i.mhpmevent_store_o
        mhpmevent_jump       <<= id_stage_i.mhpmevent_jump_o
        mhpmevent_branch     <<= id_stage_i.mhpmevent_branch_o
        mhpmevent_branch_taken <<= id_stage_i.mhpmevent_branch_taken_o
        mhpmevent_compressed <<= id_stage_i.mhpmevent_compressed_o
        mhpmevent_jr_stall   <<= id_stage_i.mhpmevent_jr_stall_o
        mhpmevent_imiss      <<= id_stage_i.mhpmevent_imiss_o
        mhpmevent_ld_stall   <<= id_stage_i.mhpmevent_ld_stall_o
        mhpmevent_pipe_stall <<= id_stage_i.mhpmevent_pipe_stall_o

        id_stage_i.perf_imiss_i <<= perf_imiss
        id_stage_i.mcounteren_i <<= mcounteren

        ##################################################################################
        # EX Stage
        ##################################################################################
        # ALU signals from ID stage
        ex_stage_i.alu_en_i <<= alu_en_ex
        ex_stage_i.alu_operator_i <<= alu_operator_ex
        ex_stage_i.alu_operand_a_i <<= alu_operand_a_ex
        ex_stage_i.alu_operand_b_i <<= alu_operand_b_ex
        ex_stage_i.alu_operand_c_i <<= alu_operand_c_ex
        # ex_stage_i.imm_vec_ext_i <<= imm_vec_ext_ex

        # Multiplier
        ex_stage_i.mult_operator_i <<= mult_operator_ex
        ex_stage_i.mult_operand_a_i <<= mult_operand_a_ex
        ex_stage_i.mult_operand_b_i <<= mult_operand_b_ex
        ex_stage_i.mult_operand_c_i <<= mult_operand_c_ex
        ex_stage_i.mult_en_i <<= mult_en_ex
        ex_stage_i.mult_signed_mode_i <<= mult_signed_mode_ex
        ex_stage_i.mult_imm_i <<= mult_imm_ex
        ex_stage_i.mult_sel_subword_i <<= U(0)

        mult_multicycle <<= ex_stage_i.mult_multicycle_o

        ex_stage_i.lsu_en_i <<= data_req_ex
        ex_stage_i.lsu_rdata_i <<= lsu_rdata

        # Interface with CSRs
        ex_stage_i.csr_access_i <<= csr_access_ex
        ex_stage_i.csr_rdata_i <<= csr_rdata

        # From ID Stage: Regfile control signals
        ex_stage_i.branch_in_ex_i <<= branch_in_ex
        ex_stage_i.regfile_alu_waddr_i <<= regfile_alu_waddr_ex
        ex_stage_i.regfile_alu_we_i <<= regfile_alu_we_ex

        ex_stage_i.regfile_waddr_i <<= regfile_waddr_ex
        ex_stage_i.regfile_we_i <<= regfile_we_ex

        # Output of ex stage pipeline
        regfile_waddr_fw_wb_o <<= ex_stage_i.regfile_waddr_wb_o
        regfile_we_wb <<= ex_stage_i.regfile_we_wb_o
        regfile_wdata <<= ex_stage_i.regfile_wdata_wb_o

        # To IF: Jump and branch target and decision
        jump_target_ex <<= ex_stage_i.jump_target_o
        branch_decision <<= ex_stage_i.branch_decision_o

        # To ID: Forwarding signals
        regfile_alu_waddr_fw <<= ex_stage_i.regfile_alu_waddr_fw_o
        regfile_alu_we_fw <<= ex_stage_i.regfile_alu_we_fw_o
        regfile_alu_wdata_fw <<= ex_stage_i.regfile_alu_wdata_fw_o

        # Stall control
        ex_stage_i.is_decoding_i <<= is_decoding
        ex_stage_i.lsu_ready_ex_i <<= lsu_ready_ex
        ex_stage_i.lsu_err_i <<= data_err_pmp

        ex_ready <<= ex_stage_i.ex_ready_o
        ex_valid <<= ex_stage_i.ex_valid_o
        ex_stage_i.wb_ready_i <<= lsu_ready_ex

        ##################################################################################
        # Load Store Unit
        ##################################################################################
        # Output to data memory
        data_req_pmp <<= load_store_unit_i.data_req_o
        load_store_unit_i.data_gnt_i <<= data_gnt_pmp
        load_store_unit_i.data_rvalid_i <<= io.data_rvalid_i
        load_store_unit_i.data_err_i <<= Bool(False)
        load_store_unit_i.data_err_pmp_i <<= data_err_pmp

        data_addr_pmp <<= load_store_unit_i.data_addr_o
        io.data_we_o <<= load_store_unit_i.data_we_o
        io.data_be_o <<= load_store_unit_i.data_be_o
        io.data_wdata_o <<= load_store_unit_i.data_wdata_o
        load_store_unit_i.data_rdata_i <<= io.data_rdata_i

        # Signal from ex stage
        load_store_unit_i.data_we_ex_i <<= data_we_ex
        load_store_unit_i.data_type_ex_i <<= data_type_ex
        load_store_unit_i.data_wdata_ex_i <<= alu_operand_c_ex
        load_store_unit_i.data_reg_offset_ex_i <<= data_reg_offset_ex
        load_store_unit_i.data_load_event_ex_i <<= data_load_event_ex
        load_store_unit_i.data_sign_ext_ex_i <<= data_sign_ext_ex

        lsu_rdata <<= load_store_unit_i.data_rdata_ex_o
        load_store_unit_i.data_req_ex_i <<= data_req_ex
        load_store_unit_i.operand_a_ex_i <<= alu_operand_a_ex
        load_store_unit_i.operand_b_ex_i <<= alu_operand_b_ex
        load_store_unit_i.addr_useincr_ex_i <<= useincr_addr_ex

        load_store_unit_i.data_misaligned_ex_i <<= data_misaligned_ex
        data_misaligned <<= load_store_unit_i.data_misaligned_o

        # Control signals
        lsu_ready_ex <<= load_store_unit_i.lsu_ready_ex_o
        lsu_ready_wb <<= load_store_unit_i.lsu_ready_wb_o

        lsu_busy <<= load_store_unit_i.busy_o

        # Tracer signal
        wb_valid <<= lsu_ready_wb

        ##################################################################################
        # CSR
        ##################################################################################
        # Not implement yet
        mtvec <<= U(0)
        utvec <<= U(0)
        mtvec_mode <<= U(0)
        utvec_mode <<= U(0)

        csr_rdata <<= U(0)

        mie_bypass <<= U(0)
        m_irq_enable <<= U(0)
        u_irq_enable <<= U(0)
        sec_lvl_o <<= U(0)
        mepc <<= U(0)
        uepc <<= U(0)

        mcounteren <<= U(0)

        depc <<= U(0)
        debug_sigle_Step <<= U(0)
        debug_ebreakm <<= U(0)
        debug_ebreaku <<= U(0)
        trigger_match <<= U(0)

        current_priv_lvl <<= U(0)

        csr_addr <<= csr_addr_int
        csr_wdata <<= alu_operand_a_ex
        csr_op <<= csr_op_ex

        csr_addr_int <<= Mux(csr_access_ex, alu_operand_b_ex[11:0], U(0))

        # No pmp support
        io.instr_req_o <<= instr_req_pmp
        io.instr_addr_o <<= instr_addr_pmp
        instr_gnt_pmp <<= io.instr_gnt_i
        instr_err_pmp <<= Bool(False)

        io.data_req_o <<= data_req_pmp
        io.data_addr_o <<= data_addr_pmp
        data_gnt_pmp <<= io.data_gnt_i
        data_err_pmp <<= Bool(False)

    return CORE()


if __name__ == '__main__':
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(core()), "core.fir"))
