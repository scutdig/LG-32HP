from .config import *
from .instructions import Inst


# csr change start
# Control signal decode map and default case

    #                       Reg_Write      Imm_sel     ALU_Src       ALUOp         Branch         Branch_Src     Mem_Read          Mem_Write         Data_Size     Load_Type         Mem_to_Reg       Jump_Type      CSR_src         Write_CSR          is_Illegal
    #                          |              |           |            |              |              |               |                 |                 |             |                 |               |              |                |                   |
default               = [Reg_Write_False,   IMM_X ,   ALU_B_XXX,   ALU_OP_XXX,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_True]

decode_map            = {
        Inst.ADD      : [Reg_Write_True ,   IMM_R ,   ALU_B_rs2,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SUB      : [Reg_Write_True ,   IMM_R ,   ALU_B_rs2,   ALU_SUB   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.AND      : [Reg_Write_True ,   IMM_R ,   ALU_B_rs2,   ALU_AND   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.OR       : [Reg_Write_True ,   IMM_R ,   ALU_B_rs2,   ALU_OR    ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.XOR      : [Reg_Write_True ,   IMM_R ,   ALU_B_rs2,   ALU_XOR   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],

        Inst.ADDI     : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.ANDI     : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_AND   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.ORI      : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_OR    ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.XORI     : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_XOR   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],

        Inst.SLL      : [Reg_Write_True ,   IMM_R ,   ALU_B_rs2,   ALU_SLL   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SRL      : [Reg_Write_True ,   IMM_R ,   ALU_B_rs2,   ALU_SRL   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SRA      : [Reg_Write_True ,   IMM_R ,   ALU_B_rs2,   ALU_SRA   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],

        Inst.SLLI     : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_SLL   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SRLI     : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_SRL   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SRAI     : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_SRA   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SLT      : [Reg_Write_True ,   IMM_R ,   ALU_B_rs2,   ALU_SLT   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SLTU     : [Reg_Write_True ,   IMM_R ,   ALU_B_rs2,   ALU_SLTU  ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SLTI     : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_SLT   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SLTIU    : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_SLTU  ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ALU,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],

        Inst.LW       : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_True ,   Mem_Write_False,   Data_Size_W,   Load_Signed  ,   RegWrite_Mem,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.LH       : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_True ,   Mem_Write_False,   Data_Size_H,   Load_Signed  ,   RegWrite_Mem,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.LB       : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_True ,   Mem_Write_False,   Data_Size_B,   Load_Signed  ,   RegWrite_Mem,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.LHU      : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_True ,   Mem_Write_False,   Data_Size_H,   Load_Unsigned,   RegWrite_Mem,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.LBU      : [Reg_Write_True ,   IMM_I ,   ALU_B_imm,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_True ,   Mem_Write_False,   Data_Size_B,   Load_Unsigned,   RegWrite_Mem,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SW       : [Reg_Write_False,   IMM_S ,   ALU_B_imm,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_True ,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SH       : [Reg_Write_False,   IMM_S ,   ALU_B_imm,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_True ,   Data_Size_H,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.SB       : [Reg_Write_False,   IMM_S ,   ALU_B_imm,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_True ,   Data_Size_B,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],

        Inst.BEQ      : [Reg_Write_False,   IMM_SB,   ALU_B_rs2,   ALU_BEQ   ,   Branch_True ,   Branch_PC ,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.BNE      : [Reg_Write_False,   IMM_SB,   ALU_B_rs2,   ALU_BNE   ,   Branch_True ,   Branch_PC ,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.BLT      : [Reg_Write_False,   IMM_SB,   ALU_B_rs2,   ALU_BLT   ,   Branch_True ,   Branch_PC ,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.BGE      : [Reg_Write_False,   IMM_SB,   ALU_B_rs2,   ALU_BGE   ,   Branch_True ,   Branch_PC ,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.BLTU     : [Reg_Write_False,   IMM_SB,   ALU_B_rs2,   ALU_BLTU  ,   Branch_True ,   Branch_PC ,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.BGEU     : [Reg_Write_False,   IMM_SB,   ALU_B_rs2,   ALU_BGEU  ,   Branch_True ,   Branch_PC ,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],

        Inst.JAL      : [Reg_Write_True ,   IMM_UJ,   ALU_B_rs2,   ALU_ADD   ,   Branch_True ,   Branch_PC ,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_PC_4, NonConditional, CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.JALR     : [Reg_Write_True ,   IMM_I ,   ALU_B_rs2,   ALU_ADD   ,   Branch_True ,   Branch_Rs1,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_PC_4, NonConditional, CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],

        Inst.LUI      : [Reg_Write_True ,   IMM_U ,   ALU_B_rs2,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_imm ,  Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        Inst.AUIPC    : [Reg_Write_True ,   IMM_U ,   ALU_B_rs2,   ALU_ADD   ,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_ipc ,  Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],

        Inst.NOP      : [Reg_Write_False,   IMM_X ,   ALU_B_XXX,   ALU_OP_XXX,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],

        Inst.CSRRW    : [Reg_Write_True ,   IMM_I ,   ALU_B_XXX,   ALU_OP_XXX,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_CSR,   Conditional,   CSR_src_rs1,   Write_CSR_True_W,  is_Illegal_False],
        Inst.CSRRS    : [Reg_Write_True ,   IMM_I ,   ALU_B_XXX,   ALU_OP_XXX,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_CSR,   Conditional,   CSR_src_rs1,   Write_CSR_True_S,  is_Illegal_False],
        Inst.CSRRC    : [Reg_Write_True ,   IMM_I ,   ALU_B_XXX,   ALU_OP_XXX,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_CSR,   Conditional,   CSR_src_rs1,   Write_CSR_True_C,  is_Illegal_False],
        Inst.CSRRWI   : [Reg_Write_True ,   IMM_I ,   ALU_B_XXX,   ALU_OP_XXX,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_CSR,   Conditional,   CSR_src_imm,   Write_CSR_True_WI, is_Illegal_False],
        Inst.CSRRSI   : [Reg_Write_True ,   IMM_I ,   ALU_B_XXX,   ALU_OP_XXX,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_CSR,   Conditional,   CSR_src_imm,   Write_CSR_True_SI, is_Illegal_False],
        Inst.CSRRCI   : [Reg_Write_True ,   IMM_I ,   ALU_B_XXX,   ALU_OP_XXX,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_CSR,   Conditional,   CSR_src_imm,   Write_CSR_True_CI, is_Illegal_False],

        Inst.MRET     : [Reg_Write_False,   IMM_X ,   ALU_B_XXX,   ALU_OP_XXX,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_Return,  is_Illegal_False],
        Inst.VOID     : [Reg_Write_False,   IMM_X ,   ALU_B_XXX,   ALU_OP_XXX,   Branch_False,   Branch_XXX,   Mem_Read_False,   Mem_Write_False,   Data_Size_W,   Load_XXX     ,   RegWrite_XXX,   Conditional,   CSR_src_XXX,   Write_CSR_False,   is_Illegal_False],
        ...: default
}
# csr change end


class Control(Module):
    io = IO(
        inst=Input(U.w(WLEN)),
        Reg_Write=Output(U.w(REG_WRITE_SIG_WIDTH)),
        Imm_Sel=Output(U.w(IMM_SEL_SIG_WIDTH)),
        ALU_Src=Output(U.w(ALU_SRC_SIG_LEN)),
        ALUOp=Output(U.w(ALUOP_SIG_LEN)),
        Branch=Output(U.w(BRANCH_SIG_LEN)),
        Branch_Src=Output(U.w(BRANCH_SRC_SIG_LEN)),
        Mem_Read=Output(U.w(MEM_READ_SIG_LEN)),
        Mem_Write=Output(U.w(MEM_WRITE_SIG_LEN)),
        Data_Size=Output(U.w(DATA_SIZE_SIG_LEN)),
        Load_Type=Output(U.w(LOAD_TYPE_SIG_LEN)),
        Mem_to_Reg=Output(U.w(REG_SRC_SIG_LEN)),
        Jump_Type=Output(U.w(JUMP_TYPE_SIG_LEN)),
        # csr add start
        CSR_src=Output(U.w(CSR_SRC_SIG_LEN)),
        Write_CSR=Output(U.w(WRITE_CSR_SIG_LEN)),
        is_Illegal=Output(U.w(IS_ILLEGAL_SIG_LEN))
        # csr add end
    )

    ctrlsignals = LookUpTable(io.inst, decode_map)

    # Control signals for ID stage
    io.Imm_Sel <<= ctrlsignals[1]

    # Control signals for EX stage
    io.ALU_Src <<= ctrlsignals[2]
    io.ALUOp <<= ctrlsignals[3]
    io.Branch <<= ctrlsignals[4]
    io.Branch_Src <<= ctrlsignals[5]
    io.Jump_Type <<= ctrlsignals[11]

    # Control signals for MEM stage
    io.Mem_Read <<= ctrlsignals[6]
    io.Mem_Write <<= ctrlsignals[7]
    io.Data_Size <<= ctrlsignals[8]
    io.Load_Type <<= ctrlsignals[9]
    # csr add start
    io.CSR_src <<= ctrlsignals[12]
    io.Write_CSR <<= ctrlsignals[13]
    io.is_Illegal <<= ctrlsignals[14]
    # csr add end

    # Control signals for WB stage
    io.Reg_Write <<= ctrlsignals[0]
    io.Mem_to_Reg <<= ctrlsignals[10]


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(Control()), "Control.fir")
    Emitter.dumpVerilog(f)
