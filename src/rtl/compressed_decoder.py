from pyhcl import *


def compressed_decoder(FPU=0):
    class COMPRESSED_DECODER(Module):
        io = IO(
            instr_i=Input(U.w(32)),
            instr_o=Output(U.w(32)),
            is_compressed_o=Output(Bool),
            illegal_instr_o=Output(Bool)
        )

    return COMPRESSED_DECODER()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(compressed_decoder()), "compressed_decoder.fir"))