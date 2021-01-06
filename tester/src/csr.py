# from config import *
from .instructions import *
from .control import decode_map
from pyhcl.dsl.infra import LookUpTableList
from .e203_defines import *


class CSR(Module):
    io = IO(
        ex_Mem_Read=Input(U.w(MEM_READ_SIG_LEN)),
        ex_Mem_Write=Input(U.w(MEM_WRITE_SIG_LEN)),
        ex_branch_addr=Input(U.w(WLEN)),
        ex_addr=Input(U.w(WLEN)),
        ex_inst=Input(U.w(WLEN)),
        csr_data_in=Input(U.w(WLEN)),
        ex_pc_4=Input(U.w(WLEN)),
        ex_Write_CSR=Input(U.w(WRITE_CSR_SIG_LEN)),
        ex_is_Illegal=Input(U.w(IS_ILLEGAL_SIG_LEN)),
        ex_Branch=Input(U.w(BRANCH_SIG_LEN)),
        PC_Sel=Input(U.w(PC_SEL_SIG_WIDTH)),
        new_addr=Input(U.w(WLEN)),
        pc_recover=Input(U.w(WLEN)),
        Bubble=Input(U.w(BUBBLE_SIG_LEN)),
        if_inst=Input(U.w(WLEN)),
        is_Waiting_Resolved=Input(U.w(1)),

        # BIU input
        rsp_valid=Input(U.w(1)),
        rsp_rdata=Input(U.w(E203_XLEN)),

        mepc_out=Output(U.w(WLEN)),
        mtvec_out=Output(U.w(WLEN)),
        csr_data_out=Output(U.w(WLEN)),
        IF_ID_Flush=Output(U.w(IF_ID_FLUSH_SIG_LEN)),
        ID_EX_Flush=Output(U.w(ID_EX_FLUSH_SIG_LEN)),
        is_Exception=Output(U.w(IS_EXCEPTION_SIG_LEN)),
        Exception_Flush=Output(U.w(EXCEPTION_FLUSH_SIG_LEN))
    )

    csr_addr = io.ex_inst[31:20]
    imm_data = CatBits(U.w(27)(0), io.ex_inst[19:15]).to_uint()

    if_inst_ctrl = LookUpTableList(io.if_inst, decode_map)
    if_is_Branch = if_inst_ctrl[4].to_bool()

    pipeline_not_stable = (io.is_Waiting_Resolved == U(1))

    # CSR registers

    # initial mstatus
    MPP   = RegInit(U.w(2)(3))
    MPIE  = RegInit(U.w(1)(1))
    MIE   = RegInit(U.w(1)(1))

    mstatus = CatBits(U.w(19)(0), MPP, U.w(3)(0), MPIE, U.w(3)(0), MIE, U.w(3)(0))

    # initial mip and mie
    MEIP  = RegInit(U.w(1)(0))
    MTIP  = RegInit(U.w(1)(0))
    MSIP  = RegInit(U.w(1)(0))

    mip   = CatBits(U.w(20)(0), MEIP, U.w(3)(0), MTIP, U.w(3)(0), MSIP, U.w(3)(0))

    MEIE  = RegInit(U.w(1)(1))
    MTIE  = RegInit(U.w(1)(1))
    MSIE  = RegInit(U.w(1)(1))

    mie   = CatBits(U.w(20)(0), MEIE, U.w(3)(0), MTIE, U.w(3)(0), MSIE, U.w(3)(0))

    # Exception handle program address
    mtvec  = RegInit(U.w(WLEN)(164))
    mepc   = RegInit(U.w(WLEN)(0))
    mcause = RegInit(U.w(WLEN)(0))
    mtval  = RegInit(U.w(WLEN)(0))

    mtime         = RegInit(U.w(WLEN)(0))
    mtimeh        = RegInit(U.w(WLEN)(0))
    mtimecmp      = RegInit(U.w(WLEN)(0))
    mtimecmph     = RegInit(U.w(WLEN)(0))
    mcycle        = RegInit(U.w(WLEN)(0))
    mcycleh       = RegInit(U.w(WLEN)(0))
    minstret      = RegInit(U.w(WLEN)(0))
    minstreth     = RegInit(U.w(WLEN)(0))

    time = CatBits(mtimeh, mtime).to_uint()
    timecmp = CatBits(mtimecmph, mtimecmp).to_uint()

    csr_list = {

        # replace
        U.w(12)(0x300): mstatus,
        U.w(12)(0x341): mepc,
        U.w(12)(0x305): mtvec,
        U.w(12)(0x343): mtval,
        U.w(12)(0x304): mie,
        U.w(12)(0x344): mip,
        U.w(12)(0x342): mcause,
        U.w(12)(0xB00): mcycle,
        U.w(12)(0xB80): mcycleh,
        U.w(12)(0x700): mtime,
        U.w(12)(0x701): mtimeh,
        U.w(12)(0xB02): minstret,
        U.w(12)(0xB82): minstreth,
        U.w(12)(0x702): mtimecmp,
        U.w(12)(0x703): mtimecmph,
        ...: U(0)
    }
    # need to rely on Control.py(or config.py), lack of '||'
    is_CSR_Instruction = (io.ex_Write_CSR == Write_CSR_True_W) | (io.ex_Write_CSR == Write_CSR_True_S) \
                         | (io.ex_Write_CSR == Write_CSR_True_C) | (io.ex_Write_CSR == Write_CSR_True_WI) \
                         | (io.ex_Write_CSR == Write_CSR_True_SI) | (io.ex_Write_CSR == Write_CSR_True_CI)
    io.csr_data_out <<= Mux(is_CSR_Instruction, LookUpTable(csr_addr, csr_list), U(0)).to_uint()
    s_val = io.csr_data_out | io.csr_data_in
    si_val = io.csr_data_out | imm_data
    c_val = io.csr_data_out & (~io.csr_data_in).to_uint()
    ci_val = io.csr_data_out & (~imm_data).to_uint()
    csr_write_data = LookUpTable(io.ex_Write_CSR, {
        Write_CSR_True_W: io.csr_data_in,
        Write_CSR_True_WI: imm_data,
        Write_CSR_True_S: s_val,
        Write_CSR_True_SI: si_val,
        Write_CSR_True_C: c_val,
        Write_CSR_True_CI: ci_val,
        ...: U(0)
    })

    biu_rsp_valid = RegInit(U.w(1)(0))
    biu_rsp_valid_to_CSR = RegInit(U.w(1)(0))

    biu_rsp_valid <<= io.rsp_valid

    # exceptions condition
    InstructionAddressMisaligned_con = ((io.ex_branch_addr & U.w(WLEN)(3)) != U.w(WLEN)(0)) \
                                       & (io.ex_Branch == Branch_True)
    IllegalInstruction_con           = io.ex_is_Illegal.to_bool()
    LoadAddressMisaligned_con        = ((io.ex_addr & U.w(WLEN)(3)) != U.w(WLEN)(0)) \
                                       & (io.ex_Mem_Read == Mem_Read_True)
    StoreAddressMisaligned_con       = ((io.ex_addr & U.w(WLEN)(3)) != U.w(WLEN)(0)) \
                                       & (io.ex_Mem_Write == Mem_Write_True)
    MachineTimerInterrupt_con        = (timecmp != U(0)) & (time > timecmp)
    ExternalInterrupt_con            = io.rsp_valid & (~biu_rsp_valid)

    exception_raise                  = InstructionAddressMisaligned_con | IllegalInstruction_con \
                                       | LoadAddressMisaligned_con | StoreAddressMisaligned_con \
                                       | MachineTimerInterrupt_con | ExternalInterrupt_con
    is_a_exception                   = InstructionAddressMisaligned_con | IllegalInstruction_con \
                                       | LoadAddressMisaligned_con | StoreAddressMisaligned_con
    is_a_interrupt                   = MachineTimerInterrupt_con | ExternalInterrupt_con
    enable_machinetimerinterrupt     = (MTIE == U(1))
    enable_interrupt                 = enable_machinetimerinterrupt
    enable_exception                 = (MIE == U(1)) & (is_a_exception | (is_a_interrupt & enable_interrupt)) \
                                       & (~pipeline_not_stable)

    # update mcycle, mtime and mintret
    mcycle_overflow     = mcycle == U.w(32)(0xffffffff)
    mcycleh_overflow    = mcycleh == U.w(32)(0xffffffff)
    mtime_overflow      = mtime == U.w(32)(0xffffffff)
    mtimeh_overflow     = mtimeh == U.w(32)(0xffffffff)
    minstret_overflow   = minstret == U.w(32)(0xffffffff)
    minstreth_overflow  = minstreth == U.w(32)(0xffffffff)

    with when(mcycle_overflow & mcycleh_overflow):
        mcycle <<= U.w(32)(0)
        mcycleh <<= U.w(32)(0)
    with elsewhen(mcycle_overflow):
        mcycle <<= U.w(32)(0)
        mcycleh <<= mcycleh + U(1)
    with otherwise():
        mcycle <<= mcycle + U(1)

    with when((mtime_overflow & mtimeh_overflow) | ((time > timecmp) & enable_exception)):
        mtime <<= U.w(32)(0)
        mtimeh <<= U.w(32)(0)
    with elsewhen(mtime_overflow):
        mtime <<= U.w(32)(0)
        mtimeh <<= mtimeh + U(1)
    with otherwise():
        mtime <<= mtime + U(1)
    # need to rely on instruction.py
    with when((io.ex_inst != U.w(32)(0x00000013)) & (io.ex_inst != U.w(32)(0x30200073))):
        with when(minstret_overflow & minstreth_overflow):
            minstret <<= U.w(32)(0)
            minstreth <<= U.w(32)(0)
        with elsewhen(minstret_overflow):
            minstret <<= U.w(32)(0)
            minstreth <<= minstreth + U(1)
        with otherwise():
            minstret <<= minstret + U(1)

    # Handling exceptions

    # mepc_out and mtvec_out
    io.mepc_out     <<= mepc
    io.mtvec_out    <<= mtvec

    # flush signal
    with when((exception_raise & enable_exception) | (io.ex_Write_CSR == Write_CSR_Return)):
        io.IF_ID_Flush  <<= U(1)
        io.ID_EX_Flush  <<= U(1)
    with otherwise():
        io.IF_ID_Flush  <<= U(0)
        io.ID_EX_Flush  <<= U(0)

    # is_Exception signal
    with when(exception_raise & enable_exception):
        io.is_Exception <<= is_Exception_MTVEC
    with elsewhen(io.ex_Write_CSR == Write_CSR_Return):
        io.is_Exception <<= is_Exception_MEPC
    with otherwise():
        io.is_Exception <<= is_Exception_False

    with when(exception_raise & enable_exception & is_a_exception):
        io.Exception_Flush <<= U(1)
    with otherwise():
        io.Exception_Flush <<= U(0)

    # csr_data_out update
    io.csr_data_out <<= LookUpTable(csr_addr, csr_list)

    # Deal with predict unit
    is_predict_recover      = RegInit(U.w(2)(0))
    true_addr               = RegInit(U.w(WLEN)(0))
    predict_recover_period  = RegInit(U.w(2)(0))
    backup_recover_addr     = RegInit(U.w(WLEN)(0))
    normal_pc               = Mux(is_a_exception, io.ex_pc_4 - U(4), io.ex_pc_4)
    _mepc                   = LookUpTable(io.PC_Sel, {
        PC_Sel_pc_4: normal_pc,
        PC_Sel_new_addr: io.new_addr,
        PC_Sel_pc_recover: io.pc_recover,
        ...: normal_pc
    })

    backup_recover_addr <<= Mux(io.PC_Sel != U(0), _mepc, backup_recover_addr)

    # update predict_recover_period
    with when(io.PC_Sel != U(0)):
        is_predict_recover <<= U(1)
    with elsewhen(is_predict_recover != U(0)):
        with when(is_predict_recover == U(2)):
            is_predict_recover <<= U(0)
        with elsewhen(io.Bubble.to_bool()):
            is_predict_recover <<= is_predict_recover
        with otherwise():
            is_predict_recover <<= is_predict_recover + U(1)
    with otherwise():
        is_predict_recover <<= U(0)

    with when(exception_raise & enable_exception):
        # /* If exception raise, handling exception */
        # /* 1. update mepc */
        #
        # // If branch predicit unit is going to recover or jump, need to store the differect address
        # /*
        # mepc := _mepc
        # when(io.PC_Sel =/= 0.U) {
        #
        #   when(if_is_Branch) {
        #     mepc := normal_pc
        #   } .otherwise {
        #     mepc := _mepc
        #   }
        #
        #   mepc := _mepc
        # } .elsewhen(is_predict_recover =/= 0.U) {
        #   mepc := backup_recover_addr
        # } .otherwise {
        #   mepc := normal_pc
        # }
        # */
        mepc <<= normal_pc


        # /* 2. update mcause
        # *
        # * exception priority level
        # * exceptions > interrupts
        # * The smaller the encoding, the higher the priority
        # *
        # * */

        mcause <<= Mux(InstructionAddressMisaligned_con, InstructionAddrMisaligned,
                       Mux(IllegalInstruction_con, IllegalInstruction,
                           Mux(LoadAddressMisaligned_con, LoadAddressMisaligned,
                               Mux(StoreAddressMisaligned_con, StoreAddressMisaligned,
                                   Mux(MachineTimerInterrupt_con, MachineTimerInterrupt,
                                       Mux(ExternalInterrupt_con, ExternalInterrupt, mcause))))))

        # /* 3. update mtval
        # *
        # * mtval stores the misaligned address or illegal instructions
        # *
        # * */
        mtval <<= Mux(InstructionAddressMisaligned_con, io.ex_branch_addr,
                      Mux(IllegalInstruction_con, io.ex_inst,
                          Mux(LoadAddressMisaligned_con | StoreAddressMisaligned_con, io.ex_addr,
                              Mux(ExternalInterrupt_con, io.rsp_rdata, mtval))))

        # /* 4. update mstatus */
        MPIE <<= MIE
        MPP <<= U(3)
        MIE <<= U(0)

        # /* 5. Trap to mtvec */

    with elsewhen(io.ex_Write_CSR == Write_CSR_Return):
        # /* Return form trap */

        # /* 1. update mstatus */
        MIE   <<= MPIE
        MPIE  <<= U(1)
        MPP   <<= U(3)

        # /* 2. Recover PC from mepc */
    with elsewhen(is_CSR_Instruction):
        with when(csr_addr == mstatus_addr):
            MIE   <<= csr_write_data[3]
            MPIE  <<= csr_write_data[7]
            MPP   <<= csr_write_data[12:11]
        with elsewhen(csr_addr == mepc_addr):
            mepc <<= csr_write_data
        with elsewhen(csr_addr == mcause_addr):
            mcause <<= csr_write_data
        with elsewhen(csr_addr == mip_addr):
            MSIP  <<= csr_write_data[3]
            MTIP  <<= csr_write_data[7]
            MEIP  <<= csr_write_data[11]
        with elsewhen(csr_addr == mie_addr):
            MSIE  <<= csr_write_data[3]
            MTIE  <<= csr_write_data[7]
            MEIE  <<= csr_write_data[11]
        with elsewhen(csr_addr == mcycle_addr):
            mcycle <<= csr_write_data
        with elsewhen(csr_addr == mcycleh_addr):
            mcycleh <<= csr_write_data
        with elsewhen(csr_addr == minstret_addr):
            minstret <<= csr_write_data
        with elsewhen(csr_addr == minstreth_addr):
            minstreth <<= csr_write_data
        with elsewhen(csr_addr == mtimecmp_addr):
            mtimecmp <<= csr_write_data
        with elsewhen(csr_addr == mtimecmph_addr):
            mtimecmph <<= csr_write_data


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(CSR()), "CSR.fir")
    Emitter.dumpVerilog(f)


