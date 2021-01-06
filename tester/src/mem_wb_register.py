from .config import *


class MemWbRegister(Module):
    io = IO(
        mem_dataout=Input(U.w(WLEN)),
        mem_alu_sum=Input(U.w(WLEN)),
        mem_rd=Input(U.w(RLEN)),
        mem_pc_4=Input(U.w(WLEN)),
        mem_imm=Input(U.w(WLEN)),
        mem_aui_pc=Input(U.w(WLEN)),
        # csr add start
        mem_csr_data_out=Input(U.w(WLEN)),
        # csr add end
    #
        mem_Mem_to_Reg=Input(U.w(REG_SRC_SIG_LEN)),
        mem_Reg_Write=Input(U.w(REG_WRITE_SIG_WIDTH)),
    #
        wb_Mem_to_Reg=Output(U.w(REG_SRC_SIG_LEN)),
        wb_Reg_Write=Output(U.w(REG_WRITE_SIG_WIDTH)),
    #
        wb_dataout=Output(U.w(WLEN)),
        wb_alu_sum=Output(U.w(WLEN)),
        wb_rd=Output(U.w(RLEN)),
        wb_pc_4=Output(U.w(WLEN)),
        wb_imm=Output(U.w(WLEN)),
        wb_aui_pc=Output(U.w(WLEN)),
        # csr add start
        wb_csr_data_out=Output(U.w(WLEN))
        # csr add end
    )

    dataout = RegInit(U.w(WLEN)(0))
    alu_sum = RegInit(U.w(WLEN)(0))
    rd = RegInit(U.w(RLEN)(0))
    pc_4 = RegInit(U.w(WLEN)(0))
    imm = RegInit(U.w(WLEN)(0))
    aui_pc = RegInit(U.w(WLEN)(0))
    # csr add start
    csr_data_out = RegInit(U.w(WLEN)(0))
    # csr add start
    mem_to_reg = RegInit(U.w(REG_SRC_SIG_LEN)(0))
    reg_write = RegInit(U.w(REG_WRITE_SIG_WIDTH)(0))

    # // apply regs
    dataout       <<= io.mem_dataout
    alu_sum       <<= io.mem_alu_sum
    rd            <<= io.mem_rd
    pc_4          <<= io.mem_pc_4
    imm           <<= io.mem_imm
    aui_pc        <<= io.mem_aui_pc
    # csr add start
    csr_data_out  <<= io.mem_csr_data_out
    # csr add start
    mem_to_reg    <<= io.mem_Mem_to_Reg
    reg_write     <<= io.mem_Reg_Write

    # // output
    io.wb_Mem_to_Reg   <<= mem_to_reg
    io.wb_Reg_Write    <<= reg_write
    io.wb_dataout      <<= dataout
    io.wb_alu_sum      <<= alu_sum
    io.wb_rd           <<= rd
    io.wb_pc_4         <<= pc_4
    io.wb_imm          <<= imm
    io.wb_aui_pc       <<= aui_pc
    # csr add start
    io.wb_csr_data_out <<= csr_data_out
    # csr add start


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(MemWbRegister()), "MemWbRegister.fir")
    Emitter.dumpVerilog(f)
