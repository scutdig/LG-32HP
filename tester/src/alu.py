from .config import *


class ALU(Module):
    io = IO(
        src_a=Input(U.w(WLEN)),
        src_b=Input(U.w(WLEN)),
        ALUOp=Input(U.w(ALUOP_SIG_LEN)),
        sum=Output(U.w(WLEN)),
        conflag=Output(U.w(CONFLAG_SIG_LEN))
    )

    shamt = io.src_b[5:0]
    io.sum <<= LookUpTable(io.ALUOp, {
        ALU_ADD: (io.src_a + io.src_b),
        ALU_SUB: (io.src_a - io.src_b),
        ALU_AND: (io.src_a & io.src_b),
        ALU_OR: (io.src_a | io.src_b),
        ALU_XOR: (io.src_a ^ shamt),
        ALU_SLL: (io.src_a << shamt),
        ALU_SRL: (io.src_a >> shamt),
        ALU_SRA: (io.src_a.to_sint() >> shamt).to_uint(),
        ALU_SLT: (io.src_a.to_sint() < io.src_b.to_sint()),
        ALU_SLTU: (io.src_a < io.src_b),
        ...: io.src_b
    })

    io.conflag <<= LookUpTable(io.ALUOp, {
        ALU_BEQ: (io.src_a.to_sint() == io.src_b.to_sint()),
        ALU_BNE: (io.src_a.to_sint() != io.src_b.to_sint()),
        ALU_BLT: (io.src_a.to_sint() < io.src_b.to_sint()),
        ALU_BGE: (io.src_a.to_sint() >= io.src_b.to_sint()),
        ALU_BLTU: (io.src_a < io.src_b),
        ALU_BGEU: (io.src_a >= io.src_b),
        ...: U(0)
    }).to_uint()


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(ALU()), "ALU.fir")
    Emitter.dumpVerilog(f)
