from .config import *


class ImmGen(Module):
    io = IO(
        inst=Input(U.w(WLEN)),
        imm=Output(U.w(WLEN)),

        Imm_Sel=Input(U.w(IMM_SEL_SIG_WIDTH))
    )

    Rimm = U.w(WLEN)(0).to_sint()
    Iimm = io.inst[31:20].to_sint()
    Simm = CatBits(io.inst[31:25], io.inst[11:7]).to_sint()
    SBimm = CatBits(io.inst[31], io.inst[7], io.inst[30:25], io.inst[11:8], U.w(1)(0)).to_sint()
    Uimm = CatBits(io.inst[31:12], U.w(12)(0)).to_sint()
    UJimm = CatBits(io.inst[31], io.inst[19:12], io.inst[20], io.inst[30:21], U.w(1)(0)).to_sint()

    io.imm <<= LookUpTable(io.Imm_Sel, {
        IMM_R: Rimm,
        IMM_I: Iimm,
        IMM_S: Simm,
        IMM_SB: SBimm,
        IMM_U: Uimm,
        IMM_UJ: UJimm,
        ...: S.w(32)(0)
    }).to_uint()


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(ImmGen()), "ImmGen.fir")
    Emitter.dumpVerilog(f)
