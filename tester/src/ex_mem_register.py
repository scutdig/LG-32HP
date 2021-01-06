from .config import *


class ExMemRegister(Module):
    io = IO(
        ex_alu_sum=Input(U.w(WLEN)),
        ex_rs2_out=Input(U.w(WLEN)),
        ex_rd=Input(U.w(RLEN)),
        ex_pc_4=Input(U.w(WLEN)),
        ex_imm=Input(U.w(WLEN)),
        ex_aui_pc=Input(U.w(WLEN)),
        ex_rs2=Input(U.w(WLEN)),
        # csr add start
        ex_inst=Input(U.w(WLEN)),
        ex_csr_data_out=Input(U.w(WLEN)),
        # csr add end
        # Control signals
        ex_Mem_Read=Input(U.w(MEM_READ_SIG_LEN)),
        ex_Mem_Write=Input(U.w(MEM_WRITE_SIG_LEN)),
        ex_Data_Size=Input(U.w(DATA_SIZE_SIG_LEN)),
        ex_Load_Type=Input(U.w(LOAD_TYPE_SIG_LEN)),
        ex_Reg_Write=Input(U.w(REG_WRITE_SIG_WIDTH)),
        ex_Mem_to_Reg=Input(U.w(REG_SRC_SIG_LEN)),
        #
        mem_Mem_Read=Output(U.w(MEM_READ_SIG_LEN)),
        mem_Mem_Write=Output(U.w(MEM_WRITE_SIG_LEN)),
        mem_Data_Size=Output(U.w(DATA_SIZE_SIG_LEN)),
        mem_Load_Type=Output(U.w(LOAD_TYPE_SIG_LEN)),
        mem_Reg_Write=Output(U.w(REG_WRITE_SIG_WIDTH)),
        mem_Mem_to_Reg=Output(U.w(REG_SRC_SIG_LEN)),
        #
        mem_alu_sum=Output(U.w(WLEN)),
        mem_rs2_out=Output(U.w(WLEN)),
        mem_rd=Output(U.w(RLEN)),
        mem_pc_4=Output(U.w(WLEN)),
        mem_imm=Output(U.w(WLEN)),
        mem_aui_pc=Output(U.w(WLEN)),
        mem_rs2=Output(U.w(WLEN)),
        # csr add start
        mem_csr_data_out=Output(U.w(WLEN))
        # csr add end
    )

    alu_sum = RegInit(U.w(WLEN)(0))
    rs2_out = RegInit(U.w(WLEN)(0))
    rd = RegInit(U.w(RLEN)(0))
    pc_4 = RegInit(U.w(WLEN)(0))
    imm = RegInit(U.w(WLEN)(0))
    aui_pc = RegInit(U.w(WLEN)(0))
    rs2 = RegInit(U.w(RLEN)(0))
    # csr add start
    branch_addr = RegInit(U.w(WLEN)(0))
    rs1_out = RegInit(U.w(WLEN)(0))
    inst = RegInit(U.w(WLEN)(0))
    csr_data_out = RegInit(U.w(WLEN)(0))
    # csr add end

    mem_read = RegInit(U.w(MEM_READ_SIG_LEN)(0))
    mem_write = RegInit(U.w(MEM_WRITE_SIG_LEN)(0))
    data_size = RegInit(U.w(DATA_SIZE_SIG_LEN)(0))
    load_type = RegInit(U.w(LOAD_TYPE_SIG_LEN)(0))
    reg_write = RegInit(U.w(REG_WRITE_SIG_WIDTH)(0))
    mem_to_reg = RegInit(U.w(REG_SRC_SIG_LEN)(0))
    # csr add start
    csr_src = RegInit(U.w(CSR_SRC_SIG_LEN)(0))
    write_csr = RegInit(U.w(WRITE_CSR_SIG_LEN)(0))
    is_illegal = RegInit(U.w(IS_ILLEGAL_SIG_LEN)(0))
    branch = RegInit(U.w(BRANCH_SIG_LEN)(0))
    # csr add end

    alu_sum       <<= io.ex_alu_sum
    rs2_out       <<= io.ex_rs2_out
    rd            <<= io.ex_rd
    pc_4          <<= io.ex_pc_4
    imm           <<= io.ex_imm
    aui_pc        <<= io.ex_aui_pc
    rs2           <<= io.ex_rs2
    mem_read      <<= io.ex_Mem_Read
    mem_write     <<= io.ex_Mem_Write
    data_size     <<= io.ex_Data_Size
    load_type     <<= io.ex_Load_Type
    reg_write     <<= io.ex_Reg_Write
    mem_to_reg    <<= io.ex_Mem_to_Reg
    # csr add start
    # inst is an useless signal? because it is not passing to the following mem stage and wb stage???
    inst          <<= io.ex_inst
    csr_data_out  <<= io.ex_csr_data_out
    # csr add end

    io.mem_alu_sum      <<= alu_sum
    io.mem_rs2_out      <<= rs2_out
    io.mem_rd           <<= rd
    io.mem_pc_4         <<= pc_4
    io.mem_imm          <<= imm
    io.mem_aui_pc       <<= aui_pc
    io.mem_rs2          <<= rs2
    # csr add start
    io.mem_csr_data_out <<= csr_data_out
    # csr add end
    io.mem_Mem_Read     <<= mem_read
    io.mem_Mem_Write    <<= mem_write
    io.mem_Data_Size    <<= data_size
    io.mem_Load_Type    <<= load_type
    io.mem_Reg_Write    <<= reg_write
    io.mem_Mem_to_Reg   <<= mem_to_reg


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(ExMemRegister()), "ExMemRegister.fir")
    Emitter.dumpVerilog(f)
