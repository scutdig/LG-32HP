from .config import *


class Forward(Module):
    io = IO(
        ex_mem_Reg_Write=Input(U.w(REG_WRITE_SIG_WIDTH)),
        ex_mem_rd=Input(U.w(RLEN)),
        ex_mem_Mem_Write=Input(U.w(MEM_WRITE_SIG_LEN)),
        ex_mem_rs2=Input(U.w(RLEN)),
        mem_wb_Reg_Write=Input(U.w(REG_WRITE_SIG_WIDTH)),
        mem_wb_rd=Input(U.w(RLEN)),
        id_ex_rs1=Input(U.w(RLEN)),
        id_ex_rs2=Input(U.w(RLEN)),
        #
        Forward_A=Output(U.w(FORWARD_A_SIG_LEN)),
        Forward_B=Output(U.w(FORWARD_B_SIG_LEN)),
        MemWrite_Src=Output(U.w(MEMWRITE_SRC_SIG_LEN))
    )

    ex_mem_a_con = io.ex_mem_Reg_Write.to_bool() & (io.ex_mem_rd != U(0)) & \
                        (io.ex_mem_rd == io.id_ex_rs1)
    ex_wb_a_con = io.mem_wb_Reg_Write.to_bool() & (io.mem_wb_rd != U(0)) & \
                        (~ex_mem_a_con) & (io.mem_wb_rd == io.id_ex_rs1)

    ex_mem_b_con = io.ex_mem_Reg_Write.to_bool() & (io.ex_mem_rd != U(0)) & \
                        (io.ex_mem_rd == io.id_ex_rs2)
    ex_wb_b_con = io.mem_wb_Reg_Write.to_bool() & (io.mem_wb_rd != U(0)) & \
                        (~ex_mem_b_con) & (io.mem_wb_rd == io.id_ex_rs2)

    io.Forward_A <<= CatBits(ex_mem_a_con, ex_wb_a_con)
    io.Forward_B <<= CatBits(ex_mem_b_con, ex_wb_b_con)

    # Memory forward
    mem_forward_con = io.mem_wb_Reg_Write.to_bool() & io.ex_mem_Mem_Write.to_bool() & \
                           (io.ex_mem_rs2 == io.mem_wb_rd)

    io.MemWrite_Src <<= Mux(mem_forward_con, MemWrite_Src_wb, MemWrite_Src_rs2)


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(Forward()), "Forward.fir")
    Emitter.dumpVerilog(f)