from .config import *


class RegFile(Module):
    io = IO(
        rs1=Input(U.w(RLEN)),       # 读出寄存器索引
        rs2=Input(U.w(RLEN)),
        rd=Input(U.w(RLEN)),        # 写入寄存器索引
        wdata=Input(U.w(WLEN)),     # 写入数据
        rs1_out=Output(U.w(WLEN)),
        rs2_out=Output(U.w(WLEN)),

        Reg_Write=Input(U.w(REG_WRITE_SIG_WIDTH))
    )

    regfile = Mem(REGFILE_LEN, U.w(WLEN))

    # Read and write in the same cycle
    inside_forward_1 = io.Reg_Write.to_bool() & (io.rs1 == io.rd)
    inside_forward_2 = io.Reg_Write.to_bool() & (io.rs2 == io.rd)

    io.rs1_out <<= Mux(inside_forward_1, io.wdata, regfile[io.rs1])
    io.rs2_out <<= Mux(inside_forward_2, io.wdata, regfile[io.rs2])

    regfile[io.rd] <<= Mux(io.Reg_Write.to_bool(), Mux(io.rd == U(0), U(0), io.wdata), regfile[io.rd])


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(RegFile()), "RegFile.fir")
    Emitter.dumpVerilog(f)