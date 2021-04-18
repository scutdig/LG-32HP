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

   Author Name:
   Date:
   File Name:
   Description:
"""

from pyhcl import *
from src.rtl.aligner import aligner
from src.rtl.compressed_decoder import compressed_decoder

from src.rtl.prefetch_buffer import prefetch_buffer

# Trap mux selector
TRAP_MACHINE = U.w(2)(0)
TRAP_USER = U.w(2)(1)
# EXception PC mux selector defines
EXC_PC_EXCEPTION = U.w(3)(0)
EXC_PC_IRQ = U.w(3)(1)
EXC_PC_DBD = U.w(3)(2)
EXC_PC_DBE = U.w(3)(3)
# PC mux selector defines
PC_BOOT = U.w(4)(0)
PC_FENCEI = U.w(4)(1)
PC_JUMP = U.w(4)(2)
PC_BRANCH = U.w(4)(3)
PC_EXCEPTION = U.w(4)(4)
PC_MRET = U.w(4)(5)
PC_URET = U.w(4)(6)
PC_DRET = U.w(4)(7)
PC_HWLOOP = U.w(4)(8)


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
            instr_req_o=Output(Bool),
            instr_addr_o=Output(U.w(32)),
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
        prefetch_buffer_i = prefetch_buffer(PULP_OBI).io
        aligner_i = aligner().io
        compressed_decoder_i = compressed_decoder(FPU).io

        if_valid = Wire(Bool)
        if_ready = Wire(Bool)
        # prefetch buffer related signals
        prefetch_busy = Wire(Bool)
        branch_req = Wire(Bool)
        branch_addr_n = Wire(U.w(32))
        branch_addr = Wire(U.w(32))
        fetch_valid = Wire(Bool)
        fetch_ready = Wire(Bool)
        fetch_rdata = Wire(U.w(32))
        exc_pc = Wire(U.w(32))
        trap_base_addr = Wire(U.w(24))
        exc_vec_pc_mux = Wire(U.w(5))
        fetch_failed = Wire(Bool)
        aligner_ready = Wire(Bool)
        instr_valid = Wire(Bool)
        # i am not sure if the data type is wire
        illegal_c_insn = Wire(Bool)
        instr_aligned = Wire(U.w(32))
        instr_decompressed = Wire(U.w(32))
        instr_compressed_int = Wire(Bool)

        # exception PC selection mux
        trap_base_addr <<= LookUpTable(io.trap_addr_mux_i,
                                       {
                                           TRAP_MACHINE: io.m_trap_base_addr_i,
                                           TRAP_USER: io.u_trap_base_addr_i,
                                           ...: io.m_trap_base_addr_i
                                       })
        exc_vec_pc_mux <<= LookUpTable(io.trap_addr_mux_i,
                                       {
                                           TRAP_MACHINE: io.m_exc_vec_pc_mux_i,
                                           TRAP_USER: io.u_exc_vec_pc_mux_i,
                                           ...: io.m_exc_vec_pc_mux_i
                                       })
        exc_pc <<= LookUpTable(io.exc_pc_mux_i,
                               {
                                   EXC_PC_EXCEPTION: CatBits(trap_base_addr, U.w(8)(0)),
                                   EXC_PC_IRQ: CatBits(trap_base_addr, U.w(1)(0), exc_vec_pc_mux, U.w(2)(0)),
                                   EXC_PC_DBD: CatBits(io.dm_halt_addr_i[31:2], U.w(2)(0)),
                                   EXC_PC_DBE: CatBits(io.dm_exception_addr_i[31:2], U.w(2)(0)),
                                   ...: CatBits(trap_base_addr, U.w(8)(0))
                               })
        # fetch address selection
        # branch_addr_n <<= CatBits(io.boot_addr_i[31:2], U.w(2)(0))
        branch_addr_n <<= LookUpTable(io.pc_mux_i,
                                      {
                                          PC_BOOT: CatBits(io.boot_addr_i[31:2], U.w(2)(0)),
                                          PC_JUMP: io.jump_target_id_i,
                                          PC_BRANCH: io.jump_target_ex_i,
                                          PC_EXCEPTION: exc_pc,
                                          PC_MRET: io.mepc_i,
                                          PC_URET: io.uepc_i,
                                          PC_DRET: io.depc_i,
                                          PC_FENCEI: io.pc_id_o + U(4),
                                          PC_HWLOOP: io.hwlp_target_i,
                                          ...: CatBits(io.boot_addr_i[31:2], U.w(2)(0))
                                      })
        # tell CS register file to initialize mtvec on boot
        io.csr_mtvec_init_o <<= (io.pc_mux_i == PC_BOOT) & io.pc_set_i
        # PMP is not supported in m4f
        fetch_failed <<= U.w(1)(0)
        # offset FSM state transition logic
        fetch_ready <<= Mux(~(io.pc_set_i) & fetch_valid & io.req_i & if_valid, aligner_ready, U.w(1)(0))
        branch_req <<= Mux(io.pc_set_i, U.w(1)(1), U.w(1)(0))
        io.if_busy_o <<= prefetch_busy
        io.perf_imiss_o <<= (~fetch_valid) & (~branch_req)

        # IF-ID pipeline registers, frozen when the ID stage is stalled
        instr_valid_id_o = RegInit(Bool(False))
        instr_rdata_id_o = RegInit(U.w(32)(0))
        is_fetch_failed_o = RegInit(Bool(False))
        pc_id_o = RegInit(U.w(32)(0))
        is_compressed_id_o = RegInit(Bool(False))
        illegal_c_insn_id_o = RegInit(Bool(False))

        # with when(~Module.reset):
        #     io.instr_valid_id_o <<= U.w(1)(0)
        #     io.instr_rdata_id_o <<= U.w(32)(0)
        #     io.is_fetch_failed_o <<= U.w(1)(0)
        #     io.pc_id_o <<= U.w(32)(0)
        #     io.is_compressed_id_o <<= U.w(1)(0)
        #     io.illegal_c_insn_id_o <<= U.w(1)(0)
        # with otherwise():
        with when(if_valid & instr_valid):
            instr_valid_id_o <<= U.w(1)(1)
            instr_rdata_id_o <<= instr_decompressed
            is_compressed_id_o <<= instr_compressed_int
            illegal_c_insn_id_o <<= illegal_c_insn
            is_fetch_failed_o <<= U.w(1)(0)
            pc_id_o <<= io.pc_if_o
        with elsewhen(io.clear_instr_valid_i):
            instr_valid_id_o <<= U.w(1)(0)
            is_fetch_failed_o <<= fetch_failed

        # Connnect to Output
        io.instr_valid_id_o <<= instr_valid_id_o
        io.instr_rdata_id_o <<= instr_rdata_id_o
        io.is_compressed_id_o <<= is_compressed_id_o
        io.illegal_c_insn_id_o <<= illegal_c_insn_id_o
        io.is_fetch_failed_o <<= is_fetch_failed_o
        io.pc_id_o <<= pc_id_o

        if_ready <<= fetch_valid & io.id_ready_i
        if_valid <<= (~io.halt_if_i) & if_ready

        branch_addr <<= CatBits(branch_addr_n[31:1], U.w(1)(0))
        # prefetch buffer, caches a fiexed number of instructions
        prefetch_buffer_i.req_i <<= io.req_i
        prefetch_buffer_i.branch_i <<= branch_req
        prefetch_buffer_i.branch_addr_i <<= branch_addr
        # prefetch_buffer_i.hwlp_jump_i <<= io.hwlp_jump_i
        # prefetch_buffer_i.hwlp_target_i <<= io.hwlp_target_i
        prefetch_buffer_i.fetch_ready_i <<= fetch_ready
        fetch_valid <<= prefetch_buffer_i.fetch_valid_o
        fetch_rdata <<= prefetch_buffer_i.fetch_rdata_o
        io.instr_req_o <<= prefetch_buffer_i.instr_req_o
        io.instr_addr_o <<= prefetch_buffer_i.instr_addr_o
        prefetch_buffer_i.instr_gnt_i <<= io.instr_gnt_i
        prefetch_buffer_i.instr_rvalid_i <<= io.instr_rvalid_i
        prefetch_buffer_i.instr_err_i <<= io.instr_err_i
        prefetch_buffer_i.instr_err_pmp_i <<= io.instr_err_pmp_i
        prefetch_buffer_i.instr_rdata_i <<= io.instr_rdata_i
        prefetch_busy <<= prefetch_buffer_i.busy_o

        aligner_i.fetch_valid_i <<= fetch_valid
        aligner_ready <<= aligner_i.aligner_ready_o
        aligner_i.if_valid_i <<= if_valid
        aligner_i.fetch_rdata_i <<= fetch_rdata
        instr_aligned <<= aligner_i.instr_aligned_o
        instr_valid <<= aligner_i.instr_valid_o
        aligner_i.branch_addr_i <<= branch_addr
        aligner_i.branch_i <<= branch_req
        # aligner_i.hwlp_addr_i <<= io.hwlp_target_i
        # aligner_i.hwlp_update_pc_i <<= io.hwlp_jump_i
        io.pc_if_o <<= aligner_i.pc_o

        compressed_decoder_i.instr_i <<= instr_aligned
        instr_decompressed <<= compressed_decoder_i.instr_o
        instr_compressed_int <<= compressed_decoder_i.is_compressed_o
        illegal_c_insn <<= compressed_decoder_i.illegal_instr_o

    return IF_STAGE()


if __name__ == '__main__':
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(if_stage()), "if_stage.fir"))
