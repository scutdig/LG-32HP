from .config import *


class IfIdRegister(Module):
    io = IO(
        if_pc=Input(U.w(WLEN)),
        if_pc_4=Input(U.w(WLEN)),
        if_inst=Input(U.w(WLEN)),
    #
        id_pc=Output(U.w(WLEN)),
        id_pc_4=Output(U.w(WLEN)),
        id_rs1=Output(U.w(RLEN)),
        id_rs2=Output(U.w(RLEN)),
        id_inst=Output(U.w(WLEN)),
    #
        IF_ID_Write=Input(U.w(IF_ID_WRITE_SIG_WIDTH)),
        IF_ID_Flush=Input(U.w(IF_IF_FLUSH_SIG_WIDTH))
    )

    pc = RegInit(U.w(WLEN)(0))
    pc_4 = RegInit(U.w(WLEN)(0))
    inst = RegInit(U.w(WLEN)(0))

    pc <<= Mux(io.IF_ID_Flush.to_bool(), U(0),
               Mux(io.IF_ID_Write.to_bool(), io.if_pc, pc))
    pc_4 <<= Mux(io.IF_ID_Flush.to_bool(), U(0),
                 Mux(io.IF_ID_Write.to_bool(), io.if_pc_4, pc_4))
    inst <<= Mux(io.IF_ID_Flush.to_bool(), U(0),
                 Mux(io.IF_ID_Write.to_bool(), io.if_inst, inst))

    io.id_pc <<= pc
    io.id_pc_4 <<= pc_4
    io.id_inst <<= inst
    io.id_rs1 <<= inst[19:15]
    io.id_rs2 <<= inst[24:20]


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(IfIdRegister()), "IfIdRegister.fir")
    Emitter.dumpVerilog(f)
