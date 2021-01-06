from .config import *
# from control import ControlSignals


class IdExRegister(Module):
    io = IO(
        id_pc=Input(U.w(WLEN)),
        id_pc_4=Input(U.w(WLEN)),
        id_rs1_out=Input(U.w(WLEN)),
        id_rs2_out=Input(U.w(WLEN)),
        id_imm=Input(U.w(WLEN)),
        id_inst=Input(U.w(WLEN)),
        id_rs1=Input(U.w(RLEN)),
        id_rs2=Input(U.w(RLEN)),
    #
        ex_pc=Output(U.w(WLEN)),
        ex_pc_4=Output(U.w(WLEN)),
        ex_rs1_out=Output(U.w(WLEN)),
        ex_rs2_out=Output(U.w(WLEN)),
        ex_rd=Output(U.w(RLEN)),
        ex_imm=Output(U.w(WLEN)),
        ex_rs1=Output(U.w(RLEN)),
        ex_rs2=Output(U.w(RLEN)),
        ex_inst=Output(U.w(WLEN)),
    #
        ID_EX_Flush=Input(U.w(ID_EX_FLUSH_SIG_LEN)),
    #
        # self.id_ctrl_in=ControlSignals().flip()
        # id_ctrl_in=Control.io.flip(),
        # csr change start
        Reg_Write=Input(U.w(REG_WRITE_SIG_WIDTH)),
        Imm_Sel=Input(U.w(IMM_SEL_SIG_WIDTH)),
        ALU_Src=Input(U.w(ALU_SRC_SIG_LEN)),
        ALUOp=Input(U.w(ALUOP_SIG_LEN)),
        Branch=Input(U.w(BRANCH_SIG_LEN)),
        Branch_Src=Input(U.w(BRANCH_SRC_SIG_LEN)),
        Mem_Read=Input(U.w(MEM_READ_SIG_LEN)),
        Mem_Write=Input(U.w(MEM_WRITE_SIG_LEN)),
        Data_Size=Input(U.w(DATA_SIZE_SIG_LEN)),
        Load_Type=Input(U.w(LOAD_TYPE_SIG_LEN)),
        Mem_to_Reg=Input(U.w(REG_SRC_SIG_LEN)),
        Jump_Type=Input(U.w(JUMP_TYPE_SIG_LEN)),
        # csr add start
        CSR_src=Input(U.w(CSR_SRC_SIG_LEN)),
        Write_CSR=Input(U.w(WRITE_CSR_SIG_LEN)),
        is_Illegal=Input(U.w(IS_ILLEGAL_SIG_LEN)),
        # csr add end
        # csr change end
        # self.ex_ctrl_out = ControlSignals()
        # ex_ctrl_out=Control.io
        # csr change start
        ex_Reg_Write=Output(U.w(REG_WRITE_SIG_WIDTH)),
        ex_Imm_Sel=Output(U.w(IMM_SEL_SIG_WIDTH)),
        ex_ALU_Src=Output(U.w(ALU_SRC_SIG_LEN)),
        ex_ALUOp=Output(U.w(ALUOP_SIG_LEN)),
        ex_Branch=Output(U.w(BRANCH_SIG_LEN)),
        ex_Branch_Src=Output(U.w(BRANCH_SRC_SIG_LEN)),
        ex_Mem_Read=Output(U.w(MEM_READ_SIG_LEN)),
        ex_Mem_Write=Output(U.w(MEM_WRITE_SIG_LEN)),
        ex_Data_Size=Output(U.w(DATA_SIZE_SIG_LEN)),
        ex_Load_Type=Output(U.w(LOAD_TYPE_SIG_LEN)),
        ex_Mem_to_Reg=Output(U.w(REG_SRC_SIG_LEN)),
        ex_Jump_Type=Output(U.w(JUMP_TYPE_SIG_LEN)),
        # csr add start
        ex_CSR_src=Output(U.w(CSR_SRC_SIG_LEN)),
        ex_Write_CSR=Output(U.w(WRITE_CSR_SIG_LEN)),
        ex_is_Illegal=Output(U.w(IS_ILLEGAL_SIG_LEN))
        # csr add end
        # csr change end
    )

    # Initial registers
    pc          = RegInit(U.w(WLEN)(0))
    pc_4        = RegInit(U.w(WLEN)(0))
    rs1_out     = RegInit(U.w(WLEN)(0))
    rs2_out     = RegInit(U.w(WLEN)(0))
    imm         = RegInit(U.w(WLEN)(0))
    inst        = RegInit(U.w(WLEN)(0))
    rs1         = RegInit(U.w(RLEN)(0))
    rs2         = RegInit(U.w(RLEN)(0))
    alu_src     = RegInit(U.w(ALU_SRC_SIG_LEN)(0))
    aluop       = RegInit(U.w(ALUOP_SIG_LEN)(0))
    branch      = RegInit(U.w(BRANCH_SIG_LEN)(0))
    branch_src  = RegInit(U.w(BRANCH_SRC_SIG_LEN)(0))
    jump_type   = RegInit(U.w(JUMP_TYPE_SIG_LEN)(0))
    mem_read    = RegInit(U.w(MEM_READ_SIG_LEN)(0))
    mem_write   = RegInit(U.w(MEM_WRITE_SIG_LEN)(0))
    data_size   = RegInit(U.w(DATA_SIZE_SIG_LEN)(0))
    load_type   = RegInit(U.w(LOAD_TYPE_SIG_LEN)(0))
    reg_write   = RegInit(U.w(REG_WRITE_SIG_WIDTH)(0))
    mem_to_reg  = RegInit(U.w(REG_SRC_SIG_LEN)(0))
    imm_sel     = RegInit(U.w(IMM_SEL_SIG_WIDTH)(0))
    # csr add start
    csr_src     = RegInit(U.w(CSR_SRC_SIG_LEN)(0))
    write_csr   = RegInit(U.w(WRITE_CSR_SIG_LEN)(0))
    is_illegal  = RegInit(U.w(IS_ILLEGAL_SIG_LEN)(0))
    # csr add end

    # apply registers
    # pc                <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_pc)
    # pc_4              <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_pc_4)
    # rs1_out           <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_rs1_out)
    # rs2_out           <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_rs2_out)
    # imm               <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_imm)
    # inst              <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_inst)
    # rs1               <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_rs1)
    # rs2               <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_rs2)
    # alu_src           <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.ALU_Src)
    # aluop             <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.ALUOp)
    # branch            <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.Branch)
    # branch_src        <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.Branch_Src)
    # jump_type         <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.Jump_Type)
    # mem_read          <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.Mem_Read)
    # mem_write         <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.Mem_Write)
    # data_size         <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.Data_Size)
    # load_type         <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.Load_Type)
    # reg_write         <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.Reg_Write)
    # mem_to_reg        <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.Mem_to_Reg)
    # imm_sel           <<= Mux(io.ID_EX_Flush.to_bool(), U(0), io.id_ctrl_in.Imm_Sel)

    pc                <<= io.id_pc
    pc_4              <<= io.id_pc_4
    rs1_out           <<= io.id_rs1_out
    rs2_out           <<= io.id_rs2_out
    imm               <<= io.id_imm
    inst              <<= io.id_inst
    rs1               <<= io.id_rs1
    rs2               <<= io.id_rs2
    alu_src           <<= io.ALU_Src
    aluop             <<= io.ALUOp
    branch            <<= io.Branch
    branch_src        <<= io.Branch_Src

    jump_type         <<= Mux(io.ID_EX_Flush.to_bool(), U.w(JUMP_TYPE_SIG_LEN)(0), io.Jump_Type)
    mem_read          <<= Mux(io.ID_EX_Flush.to_bool(), U.w(MEM_READ_SIG_LEN)(0), io.Mem_Read)
    mem_write         <<= Mux(io.ID_EX_Flush.to_bool(), U.w(MEM_WRITE_SIG_LEN)(0), io.Mem_Write)
    data_size         <<= Mux(io.ID_EX_Flush.to_bool(), U.w(DATA_SIZE_SIG_LEN)(0), io.Data_Size)
    load_type         <<= Mux(io.ID_EX_Flush.to_bool(), U.w(LOAD_TYPE_SIG_LEN)(0), io.Load_Type)
    reg_write         <<= Mux(io.ID_EX_Flush.to_bool(), U.w(REG_WRITE_SIG_WIDTH)(0), io.Reg_Write)
    mem_to_reg        <<= Mux(io.ID_EX_Flush.to_bool(), U.w(REG_SRC_SIG_LEN)(0), io.Mem_to_Reg)
    imm_sel           <<= Mux(io.ID_EX_Flush.to_bool(), U.w(IMM_SEL_SIG_WIDTH)(0), io.Imm_Sel)
    csr_src           <<= Mux(io.ID_EX_Flush.to_bool(), U.w(CSR_SRC_SIG_LEN)(0), io.CSR_src)
    write_csr         <<= Mux(io.ID_EX_Flush.to_bool(), U.w(WRITE_CSR_SIG_LEN)(0), io.Write_CSR)
    is_illegal        <<= Mux(io.ID_EX_Flush.to_bool(), U.w(IS_ILLEGAL_SIG_LEN)(0), io.is_Illegal)

    io.ex_pc <<= pc
    io.ex_pc_4 <<= pc_4
    io.ex_rs1_out <<= rs1_out
    io.ex_rs2_out <<= rs2_out
    io.ex_rs1 <<= rs1
    io.ex_rs2 <<= rs2
    io.ex_imm <<= imm
    io.ex_inst <<= inst
    io.ex_rd <<= inst[11:7]

    io.ex_ALU_Src <<= alu_src
    io.ex_ALUOp <<= aluop
    io.ex_Branch <<= branch
    io.ex_Branch_Src <<= branch_src
    io.ex_Jump_Type <<= jump_type
    io.ex_Mem_Read <<= mem_read
    io.ex_Mem_Write <<= mem_write
    io.ex_Reg_Write <<= reg_write
    io.ex_Mem_to_Reg <<= mem_to_reg
    io.ex_Data_Size <<= data_size
    io.ex_Load_Type <<= load_type
    io.ex_Imm_Sel <<= imm_sel
    # csr add start
    io.ex_CSR_src <<= csr_src
    io.ex_Write_CSR <<= write_csr
    io.ex_is_Illegal <<= is_illegal
    # csr add end


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(IdExRegister()), "IdExRegister.fir")
    Emitter.dumpVerilog(f)
