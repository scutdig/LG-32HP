"""
Author:         Ruohui Chen
Date:           2020-01-06
Design Name:    Instruction Fetch Stage
"""
from pyhcl import *


def if_stage(PULP_XPULP=0, PULP_OBI=0, PULP_SCORE=0, FPU=0):
    class IF_STAGE(Module):
        io = IO(
            # Used to calculate the exception offsets
            m_trap_base_addr_i=Input(U.w(24)),
            u_trap_base_addr_i=Input(U.w(24)),
            trap_addr_mux_i=Input(U.w(2)),
            # Boot address
            boot_addr_i=Input(U.w(32)),
            dm_exception_addr_i=Input(U.w(32)),
            # Debug mode halt address
            dm_halt_addr_i=Input(U.w(32)),
            # instruction request control
            req_i=Input(Bool),
            # instruction cache interface
            insrt_req_o=Output(Bool),
            insrt_addr_o=Output(U.w(32)),
            instr_gnt_i=Input(Bool),
            instr_rvalid_i=Input(Bool),
            instr_rdata_i=Input(U.w(32)),
            instr_err_i=Input(Bool),
            instr_err_pmp_i=Input(Bool),
            # Output of If Pipeline stage
            instr_valid_id_o=Output(Bool),
            instr_rdata_id_o=Output(U.w(32)),
            is_compressed_id_o=Output(Bool),
            illegal_c_insn_id_o=Output(Bool),
            pc_if_o=Output(U.w(32)),
            pc_id_o=Output(U.w(32)),
            is_fetch_failed_o=Output(Bool),
            # Forwarding ports - control signals
            clear_instr_valid_i=Input(Bool),
            pc_set_i=Input(Bool),
            mepc_i=Input(U.w(32)),
            uepc_i=Input(U.w(32)),
            depc_i=Input(U.w(32)),
            pc_mux_i=Input(U.w(4)),
            exc_pc_mux_i=Input(U.w(3)),
            m_exc_vec_pc_mux_i=Input(U.w(5)),
            u_exc_vec_pc_mux_i=Input(U.w(5)),
            csr_mtvec_init_o=Output(Bool),
            # jump and branch target and decision
            jump_target_id_i=Input(U.w(32)),
            jump_target_ex_i=Input(U.w(32)),
            # from hwloop controller
            hwlp_jump_i=Input(Bool),
            hwlp_target_i=Input(U.w(32)),
            # pipeline stall
            halt_if_i=Input(Bool),
            id_ready_i=Input(Bool),
            # misc signals
            if_busy_o=Output(Bool),
            perf_imiss_o=Output(Bool)
        )

        if_valid=Wire(Bool)
        if_ready=Wire(Bool)
        # prefetch buffer related signals
        prefetch_busy =Wire(Bool)
        branch_req    =Wire(Bool)
        branch_addr_n =Wire(U.w(32))
        fetch_valid   =Wire(Bool)
        fetch_ready   =Wire(Bool)
        fetch_rdata   =Wire(U.w(32))
        exc_pc        =Wire(U.w(32))
        trap_base_addr=Wire(U.w(24))
        exc_vec_pc_mux=Wire(U.w(5))
        aligner_ready =Wire(Bool)
        instr_valid   =Wire(Bool)
        # i am not sure if the data type is wire
        illegal_c_insn=Wire(Bool)
        instr_aligned =Wire(U.w(32))
        instr_decompressed = Wire(U.w(32))
        instr_compressed_int = Wire(Bool)


    return IF_STAGE()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(if_stage()), "if_stage.fir"))
