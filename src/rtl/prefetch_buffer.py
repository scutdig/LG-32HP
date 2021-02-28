from pyhcl import *


def prefetch_buffer(PULP_OBI=0, PULP_XPULP=1):
    class PREFETCH_BUFFER(Module):
        io = IO(
            req_i=Input(Bool),
            branch_i=Input(Bool),
            branch_addr_i=Input(U.w(32)),
            hwlp_jump_i=Input(Bool),
            hwlp_target_i=Input(U.w(32)),
            fetch_ready_i=Input(Bool),
            fetch_valid_o=Output(Bool),
            fetch_rdata_o=Output(U.w(32)),
            # goes to instruction memory / instruction cache
            instr_req_o=Output(Bool),
            instr_gnt_i=Input(Bool),
            instr_addr_o=Output(U.w(32)),
            instr_rdata_i=Input(U.w(32)),
            instr_rvalid_i=Input(Bool),
            instr_err_i=Input(Bool),
            instr_err_pmp_i=Input(Bool),
            # Prefetch Buffer Status
            busy_o=Output(Bool)
        )

    return PREFETCH_BUFFER()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(prefetch_buffer()), "prefetch_buffer.fir"))
