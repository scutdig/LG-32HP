from .config import *


class HazardDetection(Module):
    io = IO(
        rs1=Input(U.w(RLEN)),
        rs2=Input(U.w(RLEN)),
        ex_rd=Input(U.w(RLEN)),
    #
        Imm_Sel=Input(U.w(IMM_SEL_SIG_WIDTH)),
        ex_Mem_Read=Input(U.w(MEM_READ_SIG_LEN)),
    #
        Bubble=Output(U.w(BUBBLE_SIG_LEN)),
        IF_ID_Write=Output(U.w(IF_ID_WRITE_SIG_WIDTH)),
        PC_Write=Output(U.w(PC_WRITE_SIG_WIDTH))
    )

    # rs1 stall condition
    # only U and UJ type instructions would not use rs1
    rs1_con = io.ex_Mem_Read.to_bool() & (io.Imm_Sel != IMM_U) & \
              (io.Imm_Sel != IMM_UJ) & (io.rs1 == io.ex_rd)

    # rs2 stall condition
    rs2_con = io.ex_Mem_Read.to_bool() & ((io.Imm_Sel == IMM_R) | (io.Imm_Sel == IMM_SB)) \
              & (io.rs2 == io.ex_rd)

    stall_con = rs1_con | rs2_con

    io.Bubble <<= Mux(stall_con, Bubble_True, Bubble_False)
    io.IF_ID_Write <<= Mux(stall_con, IF_ID_Write_False, IF_ID_Write_True)
    io.PC_Write <<= Mux(stall_con, PC_Write_False, PC_Write_True)


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(HazardDetection()), "HazardDetection.fir")
    Emitter.dumpVerilog(f)
