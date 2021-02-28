from pyhcl import *


def aligner():
    class ALIGNER(Module):
        io = IO(
            fetch_valid_i=Input(Bool),
            aligner_ready_o=Output(Bool),
            if_valid_i=Input(Bool),
            fetch_rdata_i=Input(U.w(32)),
            instr_aligned_o=Output(U.w(32)),
            instr_valid_o=Output(Bool),
            branch_addr_i=Input(U.w(32)),
            branch_i=Input(Bool),
            hwlp_addr_i=Input(U.w(32)),
            hwlp_update_pc_i=Input(Bool),
            pc_o=Output(U.w(32))
        )

    return ALIGNER()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(aligner()), "aligner.fir"))
