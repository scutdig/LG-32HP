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
   Date: 2021-03-12
   File Name: controller.py
   Description: "Main CPU controller of the processor" -- original RI5CY annotation
"""
from pyhcl import *
from src.include.pkg import *


# PULP_CLUSTER, PULP_XPULP not used in our implementation
# @Groupsun: WARNING: This module contains gate clock port, we need to modify the generated
# FIRRTL file to implement it.
def controller():
    class CONTROLLER(Module):
        io = IO(
            # clk_ungated_i -> implement in FIRRTL code

            fetch_enable_i=Input(Bool),             # Start the decoding
            ctrl_busy_o=Output(Bool),               # Core is busy processing instructions
            is_decoding_o=Output(Bool),             # Core is in decoding state
            is_fetch_failed_i=Input(Bool),

            # decoder related signals
            deassert_we_o=Output(Bool),             # Deassert write enable for next instruction

            illegal_insn_i=Input(Bool),             # Decoder encountered an invalid instruction
            ecall_insn_i=Input(Bool),               # Decoder encountered an ecall instruction
            mret_insn_i=Input(Bool),                # Decoder encountered an mret instruction
            uret_insn_i=Input(Bool),                # Decoder encountered an uret instruction

            dret_insn_i=Input(Bool),                # Decoder encountered an dret instruction

            mret_dec_i=Input(Bool),
            uret_dec_i=Input(Bool),
            dret_dec_i=Input(Bool),

            wfi_i=Input(Bool),                      # Decoder wants to execute a WFI
            ebrk_insn_i=Input(Bool),                # Decoder encountered an ebreak instruction
            fencei_insn_i=Input(Bool),              # Decoder encountered an fence.i instruction
            csr_status_i=Input(Bool),               # Decoder encountered an csr status instruction

            # From IF/ID pipeline
            instr_valid_i=Input(Bool),              # Instruction coming from IF/ID pipeline is valid

            # From prefetcher
            instr_req_o=Output(Bool),               # Start fetching instructions

            # To prefetcher
            pc_set_o=Output(Bool),                  # Jump to address set by pc_mux
            pc_mux_o=Output(U.w(4)),                # Selector in the Fetch stage to select the right PC(normal,jump...)
            exc_pc_mux_o=Output(U.w(3)),            # Selects target PC for exception
            trap_addr_mux_o=Output(U.w(2)),         # Selects trap address base

            # Hwloop deprecated

            # LSU
            data_req_ex_i=Input(Bool),              # Data memory access is currently performed in EX stage
            data_we_ex_i=Input(Bool),
            data_misaligned_i=Input(Bool),
            data_load_event_i=Input(Bool),
            data_err_i=Input(Bool),
            data_err_ack_o=Output(Bool),

            # From ALU
            mult_multicycle_i=Input(Bool),

            # APU deprecated

            # Jump/Branch signals
            branch_taken_ex_i=Input(Bool),          # branch taken signal from EX ALU
            ctrl_transfer_insn_in_id_i=Input(U.w(2)),   # Jump is being calculated in ALU
            ctrl_transfer_insn_in_dec_i=Input(U.w(2)),  # Jump is being calculated in ALU

            # Interrupt Controller Signals
            irq_req_ctrl_i=Input(Bool),
            irq_sec_ctrl_i=Input(Bool),
            irq_id_ctrl_i=Input(U.w(5)),
            irq_wu_ctrl_i=Input(Bool),
            current_priv_lvl_i=Input(U.w(PRIV_SEL_WIDTH)),

            irq_ack_o=Output(Bool),
            irq_id_o=Output(U.w(5)),

            exc_cause_o=Output(U.w(5)),

            # Debug Signal
            debug_mode_o=Output(Bool),
            debug_cause_o=Output(U.w(2)),
            debug_csr_save_o=Output(Bool),
            debug_req_i=Input(Bool),
            debug_single_step_i=Input(Bool),
            debug_ebreakm_i=Input(Bool),
            debug_ebreaku_i=Input(Bool),
            trigger_match_i=Input(Bool),
            debug_p_elw_no_sleep_o=Output(Bool),
            debug_wfi_no_sleep_o=Output(Bool),
            debug_havereset_o=Output(Bool),
            debug_running_o=Output(Bool),
            debug_halted_o=Output(Bool),

            # Wakeup Signal
            wake_from_sleep_o=Output(Bool),

            csr_save_if_o=Output(Bool),
            csr_save_id_o=Output(Bool),
            csr_save_ex_o=Output(Bool),
            csr_cause_o=Output(U.w(6)),
            csr_irq_sec_o=Output(Bool),
            csr_restore_mret_id_o=Output(Bool),
            csr_restore_uret_id_o=Output(Bool),

            csr_restore_dret_id_o=Output(Bool),

            csr_save_cause_o=Output(Bool),

            # Regfile target
            regfile_we_id_i=Input(Bool),            # Currently decoded we enable
            regfile_alu_waddr_id_i=Input(U.w(6)),   # Currently decoded target address

            # Forwarding signals from regfile
            # TODO: forward signals here has ex/wb
            regfile_we_ex_i=Input(Bool),            # FW: write enable form EX stage
            regfile_waddr_ex_i=Input(U.w(6)),       # FW: write address from EX stage
            regfile_we_wb_i=Input(Bool),            # FW: write enable form WB stage
            regfile_alu_we_fw_i=Input(Bool),        # FW: ALU/MUL write enable from EX stage

            # Forwarding signals
            operand_a_fw_mux_sel_o=Output(U.w(2)),  # Regfile ra data selector from ID stage
            operand_b_fw_mux_sel_o=Output(U.w(2)),  # Regfile rb data selector from ID stage
            operand_c_fw_mux_sel_o=Output(U.w(2)),  # Regfile rc data selector from ID stage

            # Forwarding detection signals
            # TODO: forward detection signals has ex/wb
            reg_d_ex_is_reg_a_i=Input(Bool),
            reg_d_ex_is_reg_b_i=Input(Bool),
            reg_d_ex_is_reg_c_i=Input(Bool),
            reg_d_wb_is_reg_a_i=Input(Bool),
            reg_d_wb_is_reg_b_i=Input(Bool),
            reg_d_wb_is_reg_c_i=Input(Bool),
            reg_d_alu_is_reg_a_i=Input(Bool),
            reg_d_alu_is_reg_b_i=Input(Bool),
            reg_d_alu_is_reg_c_i=Input(Bool),

            # Stall signals
            halt_if_o=Output(Bool),
            halt_id_o=Output(Bool),

            misaligned_stall_o=Output(Bool),
            jr_stall_o=Output(Bool),
            load_stall_o=Output(Bool),

            id_ready_i=Input(Bool),                 # ID stage is ready
            id_valid_i=Input(Bool),                 # ID stage is valid

            ex_valid_i=Input(Bool),                 # EX stage is done

            # TODO: WB stage ready signal here
            wb_ready_i=Input(Bool),                 # WB stage is ready

            # Performance Counters
            perf_pipeline_stall_o=Output(Bool)      # Stall due to elw extra cycles
        )

        # FSM state encoding
        ctrl_fsm_cs = RegInit(U.w(CTRL_STATE_WIDTH)(0))     # RESET
        ctrl_fsm_ns = Wire(U.w(CTRL_STATE_WIDTH))

        # Debug state
        debug_fsm_cs = RegInit(U.w(DEBUG_STATE_WIDTH)(1))   # HAVERSET
        debug_fsm_ns = Wire(U.w(DEBUG_STATE_WIDTH))

        jump_done_q = RegInit(Bool(False))
        jump_done, jump_in_dec, branch_in_id_dec, branch_in_id = [Wire(Bool) for _ in range(4)]

        data_err_q = RegInit(Bool(False))

        debug_mode_q = RegInit(Bool(False))
        debug_mode_n = Wire(Bool)

        ebrk_force_debug_mode = Wire(Bool)
        illegal_insn_q = RegInit(Bool(False))
        illegal_insn_n = Wire(Bool)
        debug_req_entry_q = RegInit(Bool(False))
        debug_req_entry_n = Wire(Bool)
        debug_force_wakeup_q = RegInit(Bool(False))
        debug_force_wakeup_n = Wire(Bool)

        debug_req_q = RegInit(Bool(False))      # ungate clock
        debug_req_pending = Wire(Bool)

        # Qualify wfi vs nosleep locally
        wfi_active = Wire(Bool)

        ##################################################################################
        # Core Controller
        ##################################################################################
        # Default values
        io.instr_req_o <<= Bool(True)

        io.data_err_ack_o <<= Bool(False)

        io.csr_save_if_o <<= Bool(False)
        io.csr_save_id_o <<= Bool(False)
        io.csr_save_ex_o <<= Bool(False)
        io.csr_restore_mret_id_o <<= Bool(False)
        io.csr_restore_uret_id_o <<= Bool(False)

        io.csr_restore_dret_id_o <<= Bool(False)

        io.csr_save_cause_o <<= Bool(False)

        io.exc_cause_o <<= U(0)
        io.exc_pc_mux_o <<= EXC_PC_IRQ
        io.trap_addr_mux_o <<= TRAP_MACHINE

        io.csr_cause_o <<= U(0)
        io.csr_irq_sec_o <<= Bool(False)

        io.pc_mux_o <<= PC_BOOT
        io.pc_set_o <<= Bool(False)
        jump_done <<= jump_done_q

        ctrl_fsm_ns <<= ctrl_fsm_cs

        io.ctrl_busy_o <<= Bool(True)

        io.halt_if_o <<= Bool(False)
        io.halt_id_o <<= Bool(False)
        io.is_decoding_o <<= Bool(False)
        io.irq_ack_o <<= Bool(False)
        io.irq_id_o <<= U.w(5)(0)

        jump_in_dec <<= (io.ctrl_transfer_insn_in_dec_i == BRANCH_JALR) | \
                        (io.ctrl_transfer_insn_in_dec_i == BRANCH_JAL)

        branch_in_id <<= io.ctrl_transfer_insn_in_id_i == BRANCH_COND
        branch_in_id_dec <<= io.ctrl_transfer_insn_in_dec_i == BRANCH_COND

        ebrk_force_debug_mode <<= (io.debug_ebreakm_i & (io.current_priv_lvl_i == PRIV_LVL_M)) | \
                                  (io.debug_ebreaku_i & (io.current_priv_lvl_i == PRIV_LVL_U))
        io.debug_csr_save_o <<= Bool(False)
        io.debug_cause_o <<= DBG_CAUSE_EBREAK
        debug_mode_n <<= debug_mode_q

        illegal_insn_n <<= illegal_insn_q
        # A trap towards the debug unit is generated when one of the following conditions are true:
        # - ebreak instruction encountered
        # - single-stepping mode enabled
        # - illegal instruction exception and IIE bit is set
        # - IRQ and INTE bit is set and no exception is currently running
        # - Debugger requests halt

        debug_req_entry_n <<= debug_req_entry_q

        debug_force_wakeup_n <<= debug_force_wakeup_q

        io.perf_pipeline_stall_o <<= Bool(False)

        # FSM
        with when(ctrl_fsm_cs == RESET):
            # We were just reset, wait for fetch_enable
            io.is_decoding_o <<= Bool(False)
            io.instr_req_o <<= Bool(False)
            with when(io.fetch_enable_i):
                ctrl_fsm_ns <<= BOOT_SET

        with elsewhen(ctrl_fsm_cs == BOOT_SET):
            # Copy boot address to instr fetch address
            io.is_decoding_o <<= Bool(False)
            io.instr_req_o <<= Bool(True)
            io.pc_mux_o <<= PC_BOOT
            io.pc_set_o <<= Bool(True)
            with when(debug_req_pending):
                ctrl_fsm_ns <<= DBG_TAKEN_IF
                debug_force_wakeup_n <<= Bool(True)
            with otherwise():
                ctrl_fsm_ns <<= FIRST_FETCH

        with elsewhen(ctrl_fsm_cs == WAIT_SLEEP):
            io.is_decoding_o <<= Bool(False)
            io.ctrl_busy_o <<= Bool(False)
            io.instr_req_o <<= Bool(False)
            io.halt_if_o <<= Bool(True)
            io.halt_id_o <<= Bool(True)
            ctrl_fsm_ns <<= SLEEP

        with elsewhen(ctrl_fsm_cs == SLEEP):
            # Instruction in if_stage is already valid
            # We begin execution when an interrupt has arrived
            io.is_decoding_o <<= Bool(False)
            io.instr_req_o <<= Bool(False)
            io.halt_if_o <<= Bool(True)
            io.halt_id_o <<= Bool(True)

            # Normal execution flow
            # In debug mode or single step mode we leave immediately (wfi=nop)
            with when(io.wake_from_sleep_o):
                with when(debug_req_pending):
                    ctrl_fsm_ns <<= DBG_TAKEN_IF
                    debug_force_wakeup_n <<= Bool(True)
                with otherwise():
                    ctrl_fsm_ns <<= FIRST_FETCH
            with otherwise():
                io.ctrl_busy_o <<= Bool(False)

        with elsewhen(ctrl_fsm_cs == FIRST_FETCH):
            io.is_decoding_o <<= Bool(False)

            # ID stage is always ready
            ctrl_fsm_ns <<= DECODE

            # Handle interrupts
            with when(io.irq_req_ctrl_i & (~(debug_req_pending | debug_mode_q))):
                # This assumes that the pipeline is always flushed before going to sleep.
                # Debug mode takes precedence over irq (see DECODE)

                # Taken IRQ
                io.halt_if_o <<= Bool(True)
                io.halt_id_o <<= Bool(True)

                io.pc_set_o <<= Bool(True)
                io.pc_mux_o <<= PC_EXCEPTION
                io.exc_pc_mux_o <<= EXC_PC_IRQ
                io.exc_cause_o <<= io.irq_id_ctrl_i
                io.csr_irq_sec_o <<= io.irq_sec_ctrl_i

                # IRQ interface
                io.irq_ack_o <<= Bool(True)
                io.irq_id_o <<= io.irq_id_ctrl_i

                with when(io.irq_sec_ctrl_i):
                    io.trap_addr_mux_o <<= TRAP_MACHINE
                with otherwise():
                    io.trap_addr_mux_o <<= Mux(io.current_priv_lvl_i == PRIV_LVL_U, TRAP_USER, TRAP_MACHINE)

                io.csr_save_cause_o <<= Bool(True)
                io.csr_cause_o <<= CatBits(U.w(1)(1), io.irq_id_ctrl_i)
                io.csr_save_if_o <<= Bool(True)

        with elsewhen(ctrl_fsm_cs == DECODE):
            with when(io.branch_taken_ex_i):
                # Taken branch
                # There is a branch in the EX stage that is taken
                io.is_decoding_o <<= Bool(False)

                io.pc_mux_o <<= PC_BRANCH
                io.pc_set_o <<= Bool(True)

            with elsewhen(io.data_err_i):
                # Data error
                # The current LW or SW have been blocked by the PMP
                io.is_decoding_o <<= Bool(False)
                io.halt_if_o <<= Bool(True)
                io.halt_id_o <<= Bool(True)
                io.csr_save_ex_o <<= Bool(True)
                io.csr_save_cause_o <<= Bool(True)
                io.data_err_ack_o <<= Bool(True)

                # No jump in this stage as we have to wait one cycle to go to Machine Mode
                io.csr_cause_o <<= CatBits(U.w(1)(0), Mux(io.data_we_ex_i, EXC_CAUSE_STORE_FAULT, EXC_CAUSE_LOAD_FAULT))
                ctrl_fsm_ns <<= FLUSH_WB

            with elsewhen(io.is_fetch_failed_i):
                # The current instruction has been blocked by the PMP
                io.is_decoding_o <<= Bool(False)
                io.halt_id_o <<= Bool(True)
                io.halt_if_o <<= Bool(True)
                io.csr_save_if_o <<= Bool(True)
                io.csr_save_cause_o <<= ~debug_mode_q

                # No jump in this stage as we have to wait one cycle to go to Machine Mode
                io.csr_cause_o <<= CatBits(U.w(1)(0), EXC_CAUSE_INSTR_FAULT)
                ctrl_fsm_ns <<= FLUSH_WB

            with elsewhen(io.instr_valid_i):
                # Valid block, now analyze the current instruction in the ID stage
                # Decode and execute instructions only if the current conditional branch in the EX stage
                # is either not taken, or there is no conditional branch in the EX stage
                io.is_decoding_o <<= Bool(True)
                illegal_insn_n <<= Bool(False)

                with when((debug_req_pending | io.trigger_match_i) & (~debug_mode_q)):
                    # Serving the debug
                    io.halt_if_o <<= Bool(True)
                    io.halt_id_o <<= Bool(True)
                    ctrl_fsm_ns <<= DBG_FLUSH
                    debug_req_entry_n <<= Bool(True)
                with elsewhen(io.irq_req_ctrl_i & (~debug_mode_q)):
                    # Taken IRQ
                    io.is_decoding_o <<= Bool(False)
                    io.halt_if_o <<= Bool(True)
                    io.halt_id_o <<= Bool(True)

                    io.pc_set_o <<= Bool(True)
                    io.pc_mux_o <<= PC_EXCEPTION
                    io.exc_pc_mux_o <<= EXC_PC_IRQ
                    io.exc_cause_o <<= io.irq_id_ctrl_i
                    io.csr_irq_sec_o <<= io.irq_sec_ctrl_i

                    # IRQ interface
                    io.irq_ack_o <<= Bool(True)
                    io.irq_id_o <<= io.irq_id_ctrl_i

                    with when(io.irq_sec_ctrl_i):
                        io.trap_addr_mux_o <<= TRAP_MACHINE
                    with otherwise():
                        io.trap_addr_mux_o <<= Mux(io.current_priv_lvl_i == PRIV_LVL_U, TRAP_USER, TRAP_MACHINE)

                    io.csr_save_cause_o <<= Bool(True)
                    io.csr_cause_o <<= CatBits(U.w(1)(1), io.irq_id_ctrl_i)
                    io.csr_save_id_o <<= Bool(True)

                with otherwise():
                    with when(io.illegal_insn_i):
                        io.halt_if_o <<= Bool(True)
                        io.halt_id_o <<= Bool(False)
                        ctrl_fsm_ns <<= Mux(io.id_ready_i, FLUSH_EX, DECODE)
                        illegal_insn_n <<= Bool(True)
                    with otherwise():
                        # Decoding block
                        with when(jump_in_dec):
                            # Handle unconditional jumps
                            # We can jump directly since we know the address already
                            # We don't need to worry about conditional branches here as they
                            # will be evaluated in the EX stage
                            io.pc_mux_o <<= PC_JUMP
                            # If there is a jr stall, wait for it to be gone
                            with when((~io.jr_stall_o) & (~jump_done_q)):
                                io.pc_set_o <<= Bool(True)
                                jump_done <<= Bool(True)
                        with elsewhen(io.ebrk_insn_i):
                            io.halt_if_o <<= Bool(True)
                            io.halt_id_o <<= Bool(False)

                            with when(debug_mode_q):
                                # We got back to the park loop in the debug ROM
                                ctrl_fsm_ns <<= DBG_FLUSH
                            with elsewhen(ebrk_force_debug_mode):
                                # Debug module commands us to enter debug mode anyway
                                ctrl_fsm_ns <<= DBG_FLUSH
                            with otherwise():
                                ctrl_fsm_ns <<= Mux(io.id_ready_i, FLUSH_EX, DECODE)
                        with elsewhen(wfi_active):
                            io.halt_if_o <<= Bool(True)
                            io.halt_id_o <<= Bool(False)
                            ctrl_fsm_ns <<= Mux(io.id_ready_i, FLUSH_EX, DECODE)
                        with elsewhen(io.ecall_insn_i):
                            io.halt_if_o <<= Bool(True)
                            io.halt_id_o <<= Bool(False)
                            ctrl_fsm_ns <<= Mux(io.id_ready_i, FLUSH_EX, DECODE)
                        with elsewhen(io.fencei_insn_i):
                            io.halt_if_o <<= Bool(True)
                            io.halt_id_o <<= Bool(False)
                            ctrl_fsm_ns <<= Mux(io.id_ready_i, FLUSH_EX, DECODE)
                        with elsewhen(io.mret_insn_i | io.uret_insn_i | io.dret_insn_i):
                            io.halt_if_o <<= Bool(True)
                            io.halt_id_o <<= Bool(False)
                            ctrl_fsm_ns <<= Mux(io.id_ready_i, FLUSH_EX, DECODE)
                        with elsewhen(io.csr_status_i):
                            io.halt_if_o <<= Bool(True)
                            ctrl_fsm_ns <<= Mux(io.id_ready_i, FLUSH_EX, DECODE)
                        with elsewhen(io.data_load_event_i):
                            io.halt_if_o <<= Bool(True)
                            ctrl_fsm_ns <<= Mux(io.id_ready_i, ELW_EXE, DECODE)

                    with when(io.debug_single_step_i & (~debug_mode_q)):
                        # Prevent any more instructions from executing
                        io.halt_if_o <<= Bool(True)

                        # We don't handle dret here because its should be illegal
                        # anyway in this context

                        # Illegal, ecall, ebrk and xrettransition to later to a DBG
                        # state since we need the return address which is determined later

                        # Make sure the current instruction has been executed
                        with when(io.id_ready_i):
                            with when(io.illegal_insn_i | io.ecall_insn_i):
                                ctrl_fsm_ns <<= FLUSH_EX
                            with elsewhen((~ebrk_force_debug_mode) & io.ebrk_insn_i):
                                ctrl_fsm_ns <<= FLUSH_EX
                            with elsewhen(io.mret_insn_i | io.uret_insn_i):
                                ctrl_fsm_ns <<= FLUSH_EX
                            with elsewhen(branch_in_id):
                                ctrl_fsm_ns <<= DBG_WAIT_BRANCH
                            with otherwise():
                                ctrl_fsm_ns <<= DBG_FLUSH

            with otherwise():
                io.is_decoding_o <<= Bool(False)
                io.perf_pipeline_stall_o <<= io.data_load_event_i

        # Flush the pipeline, insert NOP into EX stage
        with elsewhen(ctrl_fsm_cs == FLUSH_EX):
            io.is_decoding_o <<= Bool(False)

            io.halt_if_o <<= Bool(True)
            io.halt_id_o <<= Bool(True)

            with when(io.data_err_i):
                # Data error
                # The current LW or SW have been blocked by PMP
                io.csr_save_ex_o <<= Bool(True)
                io.csr_save_cause_o <<= Bool(True)
                io.data_err_ack_o <<= Bool(True)
                # No jump in this stage as we have to wait one cycle to go to machine mode
                io.csr_cause_o <<= CatBits(U.w(1)(0), Mux(io.data_we_ex_i, EXC_CAUSE_STORE_FAULT, EXC_CAUSE_LOAD_FAULT))
                ctrl_fsm_ns <<= FLUSH_WB
                # Putting illegal to 0 as if it was 1, the core is going to jump to the exception of the EX stage,
                # So the illegal was never executed
                illegal_insn_n <<= Bool(False)
            with elsewhen(io.ex_valid_i):
                # Check done to prevent data hazard in the CSR registers
                ctrl_fsm_ns <<= FLUSH_WB

                with when(illegal_insn_q):
                    io.csr_save_id_o <<= Bool(True)
                    io.csr_save_cause_o <<= ~debug_mode_q
                    io.csr_cause_o <<= CatBits(U.w(1)(0), EXC_CAUSE_ILLEGAL_INSN)
                with otherwise():
                    with when(io.ebrk_insn_i):
                        io.csr_save_id_o <<= Bool(True)
                        io.csr_save_cause_o <<= Bool(True)
                        io.csr_cause_o <<= CatBits(U.w(1)(0), EXC_CAUSE_BREAKPOINT)
                    with elsewhen(io.ecall_insn_i):
                        io.csr_save_id_o <<= Bool(True)
                        io.csr_save_cause_o <<= ~debug_mode_q
                        io.csr_cause_o <<= CatBits(U.w(1)(0), Mux(io.current_priv_lvl_i == PRIV_LVL_U,
                                                                  EXC_CAUSE_ECALL_UMODE, EXC_CAUSE_ECALL_MMODE))

        with elsewhen(ctrl_fsm_cs == FLUSH_WB):
            # Flush the pipeline, insert NOP into EX and WB stage
            io.is_decoding_o <<= Bool(False)

            io.halt_if_o <<= Bool(True)
            io.halt_id_o <<= Bool(True)

            ctrl_fsm_ns <<= DECODE

            with when(data_err_q):
                # PMP data_error
                io.pc_mux_o <<= PC_EXCEPTION
                io.pc_set_o <<= Bool(True)
                io.trap_addr_mux_o <<= TRAP_MACHINE
                # Little hack during testing
                io.exc_pc_mux_o <<= EXC_PC_EXCEPTION
                io.exc_cause_o <<= Mux(io.data_we_ex_i, EXC_CAUSE_LOAD_FAULT, EXC_CAUSE_STORE_FAULT)
            with elsewhen(io.is_fetch_failed_i):
                # Instruction fetch error
                io.pc_mux_o <<= PC_EXCEPTION
                io.pc_set_o <<= Bool(True)
                io.trap_addr_mux_o <<= TRAP_MACHINE
                io.exc_pc_mux_o <<= Mux(debug_mode_q, EXC_PC_DBE, EXC_PC_EXCEPTION)
                io.exc_cause_o <<= EXC_CAUSE_INSTR_FAULT
            with otherwise():
                with when(illegal_insn_q):
                    io.pc_mux_o <<= PC_EXCEPTION
                    io.pc_set_o <<= Bool(True)
                    io.trap_addr_mux_o <<= TRAP_MACHINE
                    io.exc_pc_mux_o <<= Mux(debug_mode_q, EXC_PC_DBE, EXC_PC_EXCEPTION)
                    illegal_insn_n <<= Bool(True)
                    with when(io.debug_single_step_i & (~debug_mode_q)):
                        ctrl_fsm_ns <<= DBG_TAKEN_IF
                with otherwise():
                    with when(io.ebrk_insn_i):
                        # ebreak
                        io.pc_mux_o <<= PC_EXCEPTION
                        io.pc_set_o <<= Bool(True)
                        io.trap_addr_mux_o <<= TRAP_MACHINE
                        io.exc_pc_mux_o <<= EXC_PC_EXCEPTION

                        with when(io.debug_single_step_i & (~debug_mode_q)):
                            ctrl_fsm_ns <<= DBG_TAKEN_IF
                    with elsewhen(io.ecall_insn_i):
                        # ecall
                        io.pc_mux_o <<= PC_EXCEPTION
                        io.pc_set_o <<= Bool(True)
                        io.trap_addr_mux_o <<= TRAP_MACHINE
                        io.exc_pc_mux_o <<= Mux(debug_mode_q, EXC_PC_DBE, EXC_PC_EXCEPTION)

                        with when(io.debug_single_step_i & (~debug_mode_q)):
                            ctrl_fsm_ns <<= DBG_TAKEN_IF
                    with elsewhen(io.mret_insn_i):
                        io.csr_restore_mret_id_o <<= ~debug_mode_q
                        ctrl_fsm_ns <<= XRET_JUMP
                    with elsewhen(io.uret_insn_i):
                        io.csr_restore_mret_id_o <<= ~debug_mode_q
                        ctrl_fsm_ns <<= XRET_JUMP
                    with elsewhen(io.dret_insn_i):
                        io.csr_restore_dret_id_o <<= Bool(True)
                        ctrl_fsm_ns <<= XRET_JUMP
                    # Skip csr_status_i
                    with elsewhen(io.wfi_i):
                        with when(debug_req_pending):
                            ctrl_fsm_ns <<= DBG_TAKEN_IF
                            debug_force_wakeup_n <<= Bool(True)
                        with otherwise():
                            ctrl_fsm_ns <<= WAIT_SLEEP
                    with elsewhen(io.fencei_insn_i):
                        io.pc_mux_o <<= PC_FENCEI
                        io.pc_set_o <<= Bool(True)

        with elsewhen(ctrl_fsm_cs == XRET_JUMP):
            io.is_decoding_o <<= Bool(False)
            ctrl_fsm_ns <<= DECODE
            with when(io.mret_dec_i):
                io.pc_mux_o <<= Mux(debug_mode_q, PC_EXCEPTION, PC_MRET)
                io.pc_set_o <<= Bool(True)
                io.exc_pc_mux_o <<= EXC_PC_DBE
            with elsewhen(io.uret_dec_i):
                io.pc_mux_o <<= Mux(debug_mode_q, PC_EXCEPTION, PC_URET)
                io.pc_set_o <<= Bool(True)
                io.exc_pc_mux_o <<= EXC_PC_DBE
            with elsewhen(io.dret_dec_i):
                io.pc_mux_o <<= PC_DRET
                io.pc_set_o <<= Bool(True)
                debug_mode_n <<= Bool(False)

            with when(io.debug_single_step_i & (~debug_mode_q)):
                ctrl_fsm_ns <<= DBG_TAKEN_IF

        # A branch was in ID when trying to go to debug rom. Wait until we can
        # determine branch target address (for saving into dpc) before proceeding
        with elsewhen(ctrl_fsm_cs == DBG_WAIT_BRANCH):
            io.is_decoding_o <<= Bool(False)
            io.halt_if_o <<= Bool(True)

            with when(io.branch_taken_ex_i):
                # There is a branch in the EX stage that is taken
                io.pc_mux_o <<= PC_BRANCH
                io.pc_set_o <<= Bool(True)

            ctrl_fsm_ns <<= DBG_FLUSH

        # We enter this state when we encounter
        # 1. ebreak during debug mode
        # 2. trigger match
        # 3. ebreak with forced entry into debug mode (ebreakm or ebreaku set).
        # 4. halt request during decode
        # Regular ebreak's go through FLUSH_EX and FLUSH_WB.
        # For 1. we don't update dcsr and dpc while for 2., 3., & 4. we do
        # dpc is set to the address of ebreak and trigger match
        # not to the next instruction's (which is why we save the pc in id).
        with elsewhen(ctrl_fsm_cs == DBG_TAKEN_ID):
            io.is_decoding_o <<= Bool(False)
            io.pc_set_o <<= Bool(True)
            io.pc_mux_o <<= PC_EXCEPTION
            io.exc_pc_mux_o <<= EXC_PC_DBD
            # If not in debug mode then save cause and dpc csrs
            # else it was an ebreak in debug mode, so don't update csrs
            with when(~debug_mode_q):
                io.csr_save_cause_o <<= Bool(True)
                io.csr_save_id_o <<= Bool(True)
                io.debug_csr_save_o <<= Bool(True)
                with when(io.trigger_match_i):
                    io.debug_cause_o <<= DBG_CAUSE_TRIGGER  # pri 4 (highest)
                with elsewhen(ebrk_force_debug_mode & io.ebrk_insn_i):
                    io.debug_cause_o <<= DBG_CAUSE_EBREAK
                with elsewhen(debug_req_entry_q):
                    io.debug_cause_o <<= DBG_CAUSE_HALTREQ

            debug_req_entry_n <<= Bool(False)
            ctrl_fsm_ns <<= DECODE
            debug_mode_n <<= Bool(True)

        # We enter this state for single stepping
        # DPC is set the next instruction to be executed/fetched
        with elsewhen(ctrl_fsm_cs == DBG_TAKEN_IF):
            io.is_decoding_o <<= Bool(False)
            io.pc_set_o <<= Bool(True)
            io.pc_mux_o <<= PC_EXCEPTION
            io.exc_pc_mux_o <<= EXC_PC_DBD
            io.csr_save_cause_o <<= Bool(True)
            io.debug_csr_save_o <<= Bool(True)
            with when(debug_force_wakeup_q):
                io.debug_cause_o <<= DBG_CAUSE_HALTREQ
            with elsewhen(io.debug_single_step_i):
                io.debug_cause_o <<= DBG_CAUSE_STEP
            io.csr_save_if_o <<= Bool(True)
            ctrl_fsm_ns <<= DECODE
            debug_mode_n <<= Bool(True)
            debug_force_wakeup_n <<= Bool(False)

        with elsewhen(ctrl_fsm_cs == DBG_FLUSH):
            io.is_decoding_o <<= Bool(False)

            io.halt_if_o <<= Bool(True)
            io.halt_id_o <<= Bool(True)

            io.perf_pipeline_stall_o <<= io.data_load_event_i

            with when(io.data_err_i):
                io.csr_save_ex_o <<= Bool(True)
                io.csr_save_cause_o <<= Bool(True)
                io.data_err_ack_o <<= Bool(True)
                # No jump in this stage as we have to wait one cycle to go to Machine Mode
                io.csr_cause_o <<= CatBits(U.w(1)(0), Mux(io.data_we_ex_i, EXC_CAUSE_STORE_FAULT, EXC_CAUSE_LOAD_FAULT))
                ctrl_fsm_ns <<= FLUSH_WB
            with otherwise():
                with when(debug_mode_q | io.trigger_match_i | (ebrk_force_debug_mode & io.ebrk_insn_i) |
                          io.data_load_event_i | debug_req_entry_q):
                    ctrl_fsm_ns <<= DBG_TAKEN_ID
                with otherwise():
                    ctrl_fsm_ns <<= DBG_TAKEN_IF

        with otherwise():
            io.is_decoding_o <<= Bool(False)
            io.instr_req_o <<= Bool(False)
            ctrl_fsm_ns <<= RESET

        ##################################################################################
        # Stall Control
        ##################################################################################
        io.load_stall_o <<= Bool(False)
        io.deassert_we_o <<= Bool(False)

        # Deassert WE when the core is not decoding instructions
        with when(~io.is_decoding_o):
            io.deassert_we_o <<= Bool(True)

        # Deassert WE in case fof illegal instruction
        with when(io.illegal_insn_i):
            io.deassert_we_o <<= Bool(True)

        # Stall because of load operation
        with when(
                (((io.data_req_ex_i == Bool(True) & (io.regfile_we_ex_i == Bool(True))) |
                 ((io.wb_ready_i == Bool(False)) & (io.regfile_we_wb_i == Bool(True)))) &
                 ((io.reg_d_ex_is_reg_a_i == Bool(True)) | (io.reg_d_ex_is_reg_b_i == Bool(True)) |
                  (io.reg_d_ex_is_reg_c_i == Bool(True)) | (io.is_decoding_o & (io.regfile_we_id_i &
                                                           (~io.data_misaligned_i)) &
                                                           (io.regfile_waddr_ex_i == io.regfile_alu_waddr_id_i))))
        ):
            io.deassert_we_o <<= Bool(True)
            io.load_stall_o <<= Bool(True)

        # Stall because of jr path
        # - always stall if a result is to be forwarded to the PC
        # we don't care about in which state the ctrl_fsm is as we deassert_we
        # anyway when we are not in DECODE
        with when((io.ctrl_transfer_insn_in_dec_i == BRANCH_JALR) &
                  (((io.regfile_we_wb_i == Bool(True)) & (io.reg_d_wb_is_reg_a_i == Bool(True))) |
                   ((io.regfile_we_ex_i == Bool(True)) & (io.reg_d_ex_is_reg_a_i == Bool(True))) |
                   ((io.regfile_alu_we_fw_i == Bool(True)) & (io.reg_d_alu_is_reg_a_i == Bool(True))))):
            io.jr_stall_o <<= Bool(True)
            io.deassert_we_o <<= Bool(True)
        with otherwise():
            io.jr_stall_o <<= Bool(False)

        # Stall because of misaligned data access
        io.misaligned_stall_o <<= io.data_misaligned_i

        # Forwarding control unit
        # default
        io.operand_a_fw_mux_sel_o <<= SEL_REGFILE
        io.operand_b_fw_mux_sel_o <<= SEL_REGFILE
        io.operand_c_fw_mux_sel_o <<= SEL_REGFILE

        # Forwarding WB -> ID
        with when(io.regfile_we_wb_i):
            with when(io.reg_d_wb_is_reg_a_i):
                io.operand_a_fw_mux_sel_o <<= SEL_FW_WB
            with elsewhen(io.reg_d_wb_is_reg_b_i):
                io.operand_b_fw_mux_sel_o <<= SEL_FW_WB
            with elsewhen(io.reg_d_wb_is_reg_c_i):
                io.operand_c_fw_mux_sel_o <<= SEL_FW_WB

        # Forwarding EX -> ID
        with when(io.regfile_alu_we_fw_i):
            with when(io.reg_d_alu_is_reg_a_i):
                io.operand_a_fw_mux_sel_o <<= SEL_FW_EX
            with elsewhen(io.reg_d_alu_is_reg_b_i):
                io.operand_b_fw_mux_sel_o <<= SEL_FW_EX
            with elsewhen(io.reg_d_alu_is_reg_c_i):
                io.operand_c_fw_mux_sel_o <<= SEL_FW_EX

        # For misaligned memory access
        with when(io.data_misaligned_i):
            io.operand_a_fw_mux_sel_o <<= SEL_FW_EX
            io.operand_b_fw_mux_sel_o <<= SEL_REGFILE
        with elsewhen(io.mult_multicycle_i):
            io.operand_c_fw_mux_sel_o <<= SEL_FW_EX

        # Update registers
        ctrl_fsm_cs <<= ctrl_fsm_ns

        # Clear when id is valid (no instruction incoming)
        jump_done_q <<= jump_done & (~io.id_ready_i)

        data_err_q <<= io.data_err_i

        debug_mode_q <<= debug_mode_n

        illegal_insn_q <<= illegal_insn_n

        debug_req_entry_q <<= debug_req_entry_n
        debug_force_wakeup_q <<= debug_force_wakeup_n

        # Wakeup from sleep conditions
        io.wake_from_sleep_o <<= io.irq_wu_ctrl_i | debug_req_pending | debug_mode_q

        # Debug mode
        io.debug_mode_o <<= debug_mode_q
        # TODO: Modify in FIRRTL code
        debug_req_pending <<= io.debug_req_i | debug_req_q
        io.debug_p_elw_no_sleep_o <<= debug_mode_q | debug_req_q | io.debug_single_step_i | io.trigger_match_i;

        io.debug_wfi_no_sleep_o <<= debug_mode_q | debug_req_pending | io.debug_single_step_i | io.trigger_match_i

        # Gate off wfi
        wfi_active <<= io.wfi_i & (~io.debug_wfi_no_sleep_o)

        # ungated clk
        # TODO: Modigy in FIRRTL code
        # always_ff @(posedge clk_ungated_i, negedge rst_n)
        #     if ( !rst_n )
        #         debug_req_q <= 1'b0;
        #     else
        #         if( debug_req_i )
        #             debug_req_q <= 1'b1;
        #         else if( debug_mode_q )
        #         debug_req_q <= 1'b0;

        # Debug state FSM
        debug_fsm_cs <<= debug_fsm_ns

        with when(debug_fsm_cs == HAVERESET):
            with when(debug_mode_n | (ctrl_fsm_ns == FIRST_FETCH)):
                with when(debug_mode_n):
                    debug_fsm_ns <<= HALTED
                with otherwise():
                    debug_fsm_ns <<= RUNNING
            with otherwise():
                debug_fsm_ns <<= HAVERESET

        with elsewhen(debug_fsm_cs == RUNNING):
            with when(debug_mode_n):
                debug_fsm_ns <<= HALTED
            with otherwise():
                debug_fsm_ns <<= RUNNING

        with elsewhen(debug_fsm_cs == HALTED):
            with when(~debug_mode_n):
                debug_fsm_ns <<= RUNNING
            with otherwise():
                debug_fsm_ns <<= HALTED

        with otherwise():
            debug_fsm_ns <<= HAVERESET

        io.debug_havereset_o <<= debug_fsm_cs[HAVERESET_INDEX]
        io.debug_running_o <<= debug_fsm_cs[RUNNING_INDEX]
        io.debug_halted_o <<= debug_fsm_cs[HALTED_INDEX]

    return CONTROLLER()


if __name__ == '__main__':
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(controller()), "controller.fir"))
