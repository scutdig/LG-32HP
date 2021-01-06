from .config import *
# from control import Control


class Datapath(Module):
    io = IO(
    # IF_IO
        if_pc=Input(U.w(WLEN)),
        PC_Sel=Input(U.w(PC_SEL_SIG_WIDTH)),
        new_addr=Input(U.w(WLEN)),
        pc_recover=Input(U.w(WLEN)),
        #
        if_new_pc=Output(U.w(WLEN)),
        if_pc_4=Output(U.w(WLEN)),
    # ID_IO
        Bubble=Input(U.w(BUBBLE_SIG_LEN)),
        # self.ctrl_in = ControlSignals().flip(),
        # ctrl_in=Control.io.flip(),
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
        # self.ctrl_out = ControlSignals(),
        # ctrl_out=Control.io,
        # csr change start
        id_Reg_Write=Output(U.w(REG_WRITE_SIG_WIDTH)),
        id_Imm_Sel=Output(U.w(IMM_SEL_SIG_WIDTH)),
        id_ALU_Src=Output(U.w(ALU_SRC_SIG_LEN)),
        id_ALUOp=Output(U.w(ALUOP_SIG_LEN)),
        id_Branch=Output(U.w(BRANCH_SIG_LEN)),
        id_Branch_Src=Output(U.w(BRANCH_SRC_SIG_LEN)),
        id_Mem_Read=Output(U.w(MEM_READ_SIG_LEN)),
        id_Mem_Write=Output(U.w(MEM_WRITE_SIG_LEN)),
        id_Data_Size=Output(U.w(DATA_SIZE_SIG_LEN)),
        id_Load_Type=Output(U.w(LOAD_TYPE_SIG_LEN)),
        id_Mem_to_Reg=Output(U.w(REG_SRC_SIG_LEN)),
        id_Jump_Type=Output(U.w(JUMP_TYPE_SIG_LEN)),
        # csr add start
        id_CSR_src=Output(U.w(CSR_SRC_SIG_LEN)),
        id_Write_CSR=Output(U.w(WRITE_CSR_SIG_LEN)),
        id_is_Illegal=Output(U.w(IS_ILLEGAL_SIG_LEN)),
        # csr add end
        # csr change end
        # EX_IO
        ex_rs1_out=Input(U.w(WLEN)),
        ex_rs2_out=Input(U.w(WLEN)),
        ex_imm=Input(U.w(WLEN)),
        ex_pc=Input(U.w(WLEN)),
        ex_ALU_Src=Input(U.w(ALU_SRC_SIG_LEN)),
        ex_Branch=Input(U.w(BRANCH_SRC_SIG_LEN)),
        ex_alu_conflag=Input(U.w(CONFLAG_SIG_LEN)),
        ex_Branch_Src=Input(U.w(BRANCH_SRC_SIG_LEN)),
        ex_Jump_Type=Input(U.w(JUMP_TYPE_SIG_LEN)),
        ex_Imm_Sel=Input(U.w(IMM_SEL_SIG_WIDTH)),
        #
        Forward_A=Input(U.w(FORWARD_A_SIG_LEN)),
        Forward_B=Input(U.w(FORWARD_B_SIG_LEN)),

        alu_a_src=Output(U.w(WLEN)),
        alu_b_src=Output(U.w(WLEN)),
        ex_aui_pc=Output(U.w(WLEN)),
        forward_rs2_out=Output(U.w(WLEN)),
        #
        PC_Src=Output(U.w(PC_SRC_SIG_LEN)),
        branch_addr=Output(U.w(WLEN)),
    # MEM_IO
        mem_rs2_out=Input(U.w(WLEN)),
        MemWrite_Src=Input(U.w(MEMWRITE_SRC_SIG_LEN)),
        # csr change start
        # mem_Mem_to_Reg=Input(U.w(REG_SRC_SIG_LEN)),
        mem_Mem_to_Reg_In=Input(U.w(REG_SRC_SIG_LEN)),
        # csr change end
        mem_alu_sum=Input(U.w(WLEN)),
        mem_pc_4=Input(U.w(WLEN)),
        mem_imm=Input(U.w(WLEN)),
        mem_aui_pc=Input(U.w(WLEN)),
        #
        mem_writedata=Output(U.w(WLEN)),
    # WB_IO
        wb_alu_sum=Input(U.w(WLEN)),
        wb_dataout=Input(U.w(WLEN)),
        wb_pc_4=Input(U.w(WLEN)),
        wb_imm=Input(U.w(WLEN)),
        wb_aui_pc=Input(U.w(WLEN)),
        wb_Mem_to_Reg=Input(U.w(REG_SRC_SIG_LEN)),
        wb_reg_writedata=Output(U.w(WLEN)),
    # CSR
    # csr add start
        # IF_IO
        is_Exception=Input(U.w(IS_EXCEPTION_SIG_LEN)),
        mepc=Input(U.w(WLEN)),
        mtvec=Input(U.w(WLEN)),
        # ID_IO
        # CSR_src=Input(U.w(CSR_SRC_SIG_LEN)),
        # Write_CSR=Input(U.w(WRITE_CSR_SIG_LEN)),
        # is_Illegal=Input(U.w(IS_ILLEGAL_SIG_LEN)),
        # id_CSR_src=Output(U.w(CSR_SRC_SIG_LEN)),
        # id_Write_CSR=Output(U.w(WRITE_CSR_SIG_LEN)),
        # id_is_Illegal=Output(U.w(IS_ILLEGAL_SIG_LEN)),
        # EX_IO
        ex_CSR_src=Input(U.w(CSR_SRC_SIG_LEN)),
        Exception_Flush=Input(U.w(EXCEPTION_FLUSH_SIG_LEN)),
        csr_data_in=Output(U.w(WLEN)),
        # // Exception Flush
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
        # csr change start
        # mem_Mem_to_Reg=Output(U.w(REG_SRC_SIG_LEN))
        mem_Mem_to_Reg_Out=Output(U.w(REG_SRC_SIG_LEN)),
        # csr change end
        # WB_IO
        wb_csr_data_out=Input(U.w(WLEN))

    # csr add end
    )

    # ------------------------------------------------------------------------- #
    # IF Stage
    # ------------------------------------------------------------------------- #

    # Generate increment PC
    # Condition: is JALR
    is_JALR = (io.ex_Imm_Sel == IMM_I) & (io.ex_Jump_Type == NonConditional)

    PC_4 = io.if_pc + U(4)
    io.if_pc_4 <<= PC_4

    shift_imm = Mux(is_JALR, io.ex_imm, io.ex_imm << U(1))
    ex_branch_addr = Mux(io.ex_Branch_Src.to_bool(), io.alu_a_src, io.ex_pc) \
                     + shift_imm.to_uint()
    io.ex_aui_pc <<= Mux(io.ex_Branch_Src.to_bool(),
                         io.alu_a_src, io.ex_pc) + io.ex_imm
    io.branch_addr <<= ex_branch_addr

    # Next PC
    PC_Src = Mux(io.ex_Jump_Type.to_bool(), U(1), io.ex_alu_conflag).to_bool() \
             & io.ex_Branch.to_bool()
    io.PC_Src <<= PC_Src

    normal_pc = LookUpTable(io.PC_Sel, {
        PC_Sel_pc_4: PC_4,
        PC_Sel_new_addr: io.new_addr,
        PC_Sel_pc_recover: io.pc_recover,
        ...: PC_4
    })

    io.if_new_pc <<= LookUpTable(io.is_Exception, {
        is_Exception_False: normal_pc,
        is_Exception_MEPC: io.mepc,
        is_Exception_MTVEC: io.mtvec,
        ...: normal_pc
    })

    # ------------------------------------------------------------------------- #
    # ID Stage
    # ------------------------------------------------------------------------- #

    # # These code should work when a bundle is flip from other bundle
    # ctrlsignal_list = filter(lambda x: not x.startswith("_") and not x.startswith("__"),
    #                          list([k for k in io.ctrl_out.__dict__]))
    # for k in ctrlsignal_list:
    #     io.ctrl_out.__dict__[k] <<= Mux(io.Bubble.to_bool(), U(0),
    #                                     io.ctrl_in.__dict__[k])
    io.id_Reg_Write <<= Mux(io.Bubble.to_bool(), U(0), io.Reg_Write)
    io.id_ALU_Src <<= Mux(io.Bubble.to_bool(), U(0), io.ALU_Src)
    io.id_ALUOp <<= Mux(io.Bubble.to_bool(), U(0), io.ALUOp)
    io.id_Branch <<= Mux(io.Bubble.to_bool(), U(0), io.Branch)
    io.id_Branch_Src <<= Mux(io.Bubble.to_bool(), U(0), io.Branch_Src)
    io.id_Mem_Read <<= Mux(io.Bubble.to_bool(), U(0), io.Mem_Read)
    io.id_Mem_Write <<= Mux(io.Bubble.to_bool(), U(0), io.Mem_Write)
    io.id_Data_Size <<= Mux(io.Bubble.to_bool(), U(0), io.Data_Size)
    io.id_Load_Type <<= Mux(io.Bubble.to_bool(), U(0), io.Load_Type)
    io.id_Mem_to_Reg <<= Mux(io.Bubble.to_bool(), U(0), io.Mem_to_Reg)
    io.id_Jump_Type <<= Mux(io.Bubble.to_bool(), U(0), io.Jump_Type)
    io.id_Imm_Sel <<= Mux(io.Bubble.to_bool(), U(0), io.Imm_Sel)
    io.id_CSR_src <<= Mux(io.Bubble.to_bool(), U(0), io.CSR_src)
    io.id_Write_CSR <<= Mux(io.Bubble.to_bool(), U(0), io.Write_CSR)
    io.id_is_Illegal <<= Mux(io.Bubble.to_bool(), U(0), io.is_Illegal)

    # ------------------------------------------------------------------------- #
    # EX Stage
    # ------------------------------------------------------------------------- #

    # Forward unit
    mem_forward_value = LookUpTable(io.mem_Mem_to_Reg_In, {
        RegWrite_ALU: io.mem_alu_sum,
        RegWrite_PC_4: io.mem_pc_4,
        RegWrite_imm: io.mem_imm,
        RegWrite_ipc: io.mem_aui_pc,
        ...: RegWrite_XXX
    })

    io.alu_a_src <<= LookUpTable(io.Forward_A, {
        Forward_A_rs1: io.ex_rs1_out,
        Forward_A_mem_wb_rd: io.wb_reg_writedata,
        Forward_A_ex_mem_rd: mem_forward_value,
        ...: io.ex_rs1_out
    })

    operand_b = LookUpTable(io.Forward_B, {
        Forward_B_rs1: io.ex_rs2_out,
        Forward_B_mem_wb_rd: io.wb_reg_writedata,
        Forward_B_ex_mem_rd: mem_forward_value,
        ...: io.ex_rs2_out
    })

    # Select ALU operand B source
    io.alu_b_src <<= Mux(io.ex_ALU_Src.to_bool(), io.ex_imm, operand_b)
    io.forward_rs2_out <<= operand_b

    io.csr_data_in <<= Mux(io.ex_CSR_src.to_bool(), io.ex_imm, io.alu_a_src)
    # // Exception flush
    io.mem_Data_Size <<= Mux(io.Exception_Flush.to_bool(), U(0), io.ex_Data_Size)
    io.mem_Load_Type <<= Mux(io.Exception_Flush.to_bool(), U(0), io.ex_Load_Type)
    io.mem_Mem_Read <<= Mux(io.Exception_Flush.to_bool(), U(0), io.ex_Mem_Read)
    io.mem_Mem_Write <<= Mux(io.Exception_Flush.to_bool(), U(0), io.ex_Mem_Write)
    io.mem_Mem_to_Reg_Out <<= Mux(io.Exception_Flush.to_bool(), U(0), io.ex_Mem_to_Reg)
    io.mem_Reg_Write <<= Mux(io.Exception_Flush.to_bool(), U(0), io.ex_Reg_Write)
    # ------------------------------------------------------------------------- #
    # MEM Stage
    # ------------------------------------------------------------------------- #
    io.mem_writedata <<= Mux(io.MemWrite_Src.to_bool(), io.wb_reg_writedata, io.mem_rs2_out)

    # ------------------------------------------------------------------------- #
    # WB Stage
    # ------------------------------------------------------------------------- #
    io.wb_reg_writedata <<= LookUpTable(
        io.wb_Mem_to_Reg, {
            RegWrite_ALU: io.wb_alu_sum,
            RegWrite_Mem: io.wb_dataout,
            RegWrite_PC_4: io.wb_pc_4,
            RegWrite_imm: io.wb_imm,
            RegWrite_ipc: io.wb_aui_pc,
            RegWrite_CSR: io.wb_csr_data_out,
            ...: io.wb_alu_sum
        }
    )


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(Datapath()), "Datapath.fir")
    Emitter.dumpVerilog(f)
