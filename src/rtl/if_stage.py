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
from src.include.pkg import *
from src.rtl.prefetch_buffer import prefetch_buffer


def if_stage(PULP_OBI=0, FPU=0):
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
            instr_err_i=Input(Bool),  # not used yet
            instr_err_pmp_i=Input(Bool),  # PMP error (validity defined by instr_gnt_i)

            # Output of If Pipeline stage
            instr_valid_id_o=Output(Bool),  # instruction in IF/ID pipeline is valid
            instr_rdata_id_o=Output(U.w(32)),  # read instruction is sampled and sent to ID stage for decoding
            is_compressed_id_o=Output(Bool),  # compressed decoder thinks this is a compressed instruction
            illegal_c_insn_id_o=Output(Bool),  # compressed decoder thinks this is an incalid instruction
            pc_if_o=Output(U.w(32)),
            pc_id_o=Output(U.w(32)),
            is_fetch_failed_o=Output(Bool),

            # Forwarding ports - control signals
            clear_instr_valid_i=Input(Bool),  # clear instruction valid bit in IF/ID pipe
            pc_set_i=Input(Bool),  # set the program counter to a new value
            mepc_i=Input(U.w(32)),  # address used to restore PC when the interrupt/exception is served
            uepc_i=Input(U.w(32)),  # address used to restore PC when the interrupt/exception is served

            depc_i=Input(U.w(32)),  # address used to restore PC when the debug is served

            pc_mux_i=Input(U.w(4)),  # sel for pc multiplexer
            exc_pc_mux_i=Input(U.w(3)),  # selects ISR address

            m_exc_vec_pc_mux_i=Input(U.w(5)),  # selects ISR address for vectorized interrupt lines
            u_exc_vec_pc_mux_i=Input(U.w(5)),  # selects ISR address for vectorized interrupt lines
            csr_mtvec_init_o=Output(Bool),  # tell CS regfile to init mtvec

            # jump and branch target and decision
            jump_target_id_i=Input(U.w(32)),  # jump target address
            jump_target_ex_i=Input(U.w(32)),  # jump target address

            # pipeline stall
            halt_if_i=Input(Bool),
            id_ready_i=Input(Bool),

            # misc signals
            if_busy_o=Output(Bool),  # is the IF stage busy fetching instructions
            perf_imiss_o=Output(Bool)  # Instruction Fetch Miss
        )
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
        illegal_c_insn = Wire(Bool)
        instr_aligned = Wire(U.w(32))
        instr_decompressed = Wire(U.w(32))
        instr_compressed_int = Wire(Bool)

        # Register define
        instr_valid_id = Reg(U.w(1))
        instr_rdata_id = Reg(U.w(32))
        is_fetch_failed = Reg(Bool)
        pc_id = Reg(U.w(32))
        is_compressed_id = Reg(Bool)
        illegal_c_insn_id = Reg(Bool)

        prefetch_buffer_i = prefetch_buffer(PULP_OBI).io
        aligner_i = aligner().io
        compressed_decoder_i = compressed_decoder(FPU=FPU).io

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
                                          ...: CatBits(io.boot_addr_i[31:2], U.w(2)(0))
                                      })

        # tell CS register file to initialize mtvec on boot
        io.csr_mtvec_init_o <<= (io.pc_mux_i == PC_BOOT) & io.pc_set_i
        # PMP is not supported in m4f
        fetch_failed <<= U.w(1)(0)
        # offset FSM state transition logic
        fetch_ready <<= Mux(~io.pc_set_i & fetch_valid & io.req_i & if_valid, aligner_ready, U.w(1)(0))
        branch_req <<= Mux(io.pc_set_i, U.w(1)(1), U.w(1)(0))

        io.if_busy_o <<= prefetch_busy
        io.perf_imiss_o <<= (~fetch_valid) & (~branch_req)
        # IF-ID pipeline registers, frozen when the ID stage is stalled
        with when(Module.reset):
            instr_valid_id <<= U.w(1)(0)
            instr_rdata_id <<= U.w(32)(0)
            is_fetch_failed <<= U.w(1)(0)
            pc_id <<= U.w(32)(0)
            is_compressed_id <<= U.w(1)(0)
            illegal_c_insn_id <<= U.w(1)(0)
        with otherwise():
            with when(if_valid & instr_valid):
                instr_valid_id <<= U.w(1)(1)
                instr_rdata_id <<= instr_decompressed
                is_compressed_id <<= instr_compressed_int
                illegal_c_insn_id <<= illegal_c_insn
                is_fetch_failed <<= U.w(1)(0)
                pc_id <<= io.pc_if_o
            with elsewhen(io.clear_instr_valid_i):
                instr_valid_id <<= U.w(1)(0)
                is_fetch_failed <<= fetch_failed

        # assign the register to output port
        io.instr_valid_id_o <<= instr_valid_id
        io.instr_rdata_id_o <<= instr_rdata_id
        io.is_fetch_failed_o <<= is_fetch_failed
        io.pc_id_o <<= pc_id
        io.is_compressed_id_o <<= is_compressed_id
        io.illegal_c_insn_id_o <<= illegal_c_insn_id

        if_ready <<= fetch_valid & io.id_ready_i
        if_valid <<= (~io.halt_if_i) & if_ready

        branch_addr <<= CatBits(branch_addr_n[31:1], U.w(1)(0))
        ##################################################################################
        # Prefetch buffer, caches a fixed number of instructions
        ##################################################################################

        prefetch_buffer_i.req_i <<= io.req_i

        prefetch_buffer_i.branch_i <<= branch_req
        prefetch_buffer_i.branch_addr_i <<= branch_addr

        prefetch_buffer_i.fetch_ready_i <<= fetch_ready
        fetch_valid <<= prefetch_buffer_i.fetch_valid_o
        fetch_rdata <<= prefetch_buffer_i.fetch_rdata_o

        io.instr_req_o <<= prefetch_buffer_i.instr_req_o
        io.instr_addr_o <<= prefetch_buffer_i.instr_addr_o
        prefetch_buffer_i.instr_gnt_i <<= io.instr_gnt_i
        prefetch_buffer_i.instr_rvalid_i <<= io.instr_rvalid_i
        prefetch_buffer_i.instr_err_i <<= io.instr_err_i  # not supported yet
        prefetch_buffer_i.instr_err_pmp_i <<= io.instr_err_pmp_i  # not supported yet
        prefetch_buffer_i.instr_rdata_i <<= io.instr_rdata_i

        prefetch_busy <<= prefetch_buffer_i.busy_o  # Prefetch Buffer Status
        ##################################################################################
        # Aligner
        ##################################################################################
        aligner_i.fetch_valid_i <<= fetch_valid
        aligner_ready <<= aligner_i.aligner_ready_o
        aligner_i.if_valid_i <<= if_valid
        aligner_i.fetch_rdata_i <<= fetch_rdata
        instr_aligned <<= aligner_i.instr_aligned_o
        instr_valid <<= aligner_i.instr_valid_o
        aligner_i.branch_addr_i <<= branch_addr
        aligner_i.branch_i <<= branch_req
        io.pc_if_o <<= aligner_i.pc_o
        ##################################################################################
        # Compressed decoder
        ##################################################################################
        compressed_decoder_i.instr_i <<= instr_aligned
        instr_decompressed <<= compressed_decoder_i.instr_o
        instr_compressed_int <<= compressed_decoder_i.is_compressed_o
        illegal_c_insn <<= compressed_decoder_i.illegal_instr_o

    return IF_STAGE()


if __name__ == '__main__':
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(if_stage()), "if_stage.fir"))
