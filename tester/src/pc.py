from .config import *


class PC(Module):
    io = IO(
        next_pc=Input(U.w(WLEN)),
        PC_Write=Input(U.w(PC_WRITE_SIG_WIDTH)),
        pc_out=Output(U.w(WLEN))
    )

    pc_reg = RegInit(U.w(WLEN)(0))
    pc_reg <<= Mux(io.PC_Write.to_bool(), io.next_pc, pc_reg)
    io.pc_out <<= pc_reg


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(PC()), "PC.fir")
    Emitter.dumpVerilog(f)
