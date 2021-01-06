from .config import *
from .control import default, decode_map
from .addr_buffer import AddrBuffer
from pyhcl.dsl.infra import LookUpTableList


class BranchPredictor(Module):
    io = IO(
        inst=Input(U.w(WLEN)),
        branch_addr=Input(U.w(WLEN)),
        PC_Src=Input(U.w(PC_SRC_SIG_LEN)),
        pc=Input(U.w(WLEN)),
        ex_Branch=Input(U.w(BRANCH_SRC_SIG_LEN)),
        ex_Jump_Type=Input(U.w(JUMP_TYPE_SIG_LEN)),
    
        PC_Sel=Output(U.w(PC_SEL_SIG_WIDTH)),
        new_addr=Output(U.w(WLEN)),
        pc_recover=Output(U.w(WLEN)),
        IF_ID_Flush=Output(U.w(IF_ID_FLUSH_SIG_LEN)),
        ID_EX_Flush=Output(U.w(ID_EX_FLUSH_SIG_LEN)),

        # csr add start
        # Handling exception
        is_Exception=Input(U.w(IS_EXCEPTION_SIG_LEN)),
        is_Waiting_Resolved=Output(U.w(1))
        # csr add end
    )

    addr_buffer = AddrBuffer()

    current_inst_ctrl = LookUpTableList(io.inst, decode_map)

    dynamic_counter_status = RegInit(U.w(2)(0))

    # csr add start
    wait_for_resolving     = RegInit(U.w(1)(0))
    resolving_processed    = RegInit(U.w(2)(0))
    # csr add start

    pc_4 = io.pc + U(4)

    # Conditions
    is_nonconditional_jump = current_inst_ctrl[4].to_bool() & (current_inst_ctrl[11] == NonConditional)
    is_conditional_jump = current_inst_ctrl[4].to_bool() & (current_inst_ctrl[11] == Conditional)
    noncon_addr_is_resolved = io.ex_Branch.to_bool() & (io.ex_Jump_Type == NonConditional)
    con_addr_is_resolved = io.ex_Branch.to_bool() & (io.ex_Jump_Type == Conditional)
    noncon_flush = noncon_addr_is_resolved
    need_record_pc_4 = is_conditional_jump & ((dynamic_counter_status == Strong_Taken) |
                                              (dynamic_counter_status == Weak_Taken))

    # csr add start
    is_a_jump_also_an_exception       = (is_nonconditional_jump | is_conditional_jump) \
                                        & io.is_Exception == is_Exception_MTVEC
    target_resolve_also_an_exception  = (noncon_addr_is_resolved | con_addr_is_resolved) \
                                        & io.is_Exception == is_Exception_MTVEC

    # // update status
    with when((is_nonconditional_jump | is_conditional_jump) & (io.is_Exception == U(0))):
        wait_for_resolving <<= U(1)
    with elsewhen(noncon_addr_is_resolved | con_addr_is_resolved):
        wait_for_resolving <<= U(0)
    with otherwise():
        wait_for_resolving <<= wait_for_resolving

    with when(noncon_addr_is_resolved | con_addr_is_resolved):
        resolving_processed <<= U(2)
    with elsewhen(resolving_processed != U(0)):
        resolving_processed <<= resolving_processed - U(1)
    with otherwise():
        resolving_processed <<= U(0)

    io.is_Waiting_Resolved <<= Mux((wait_for_resolving == U(1)) | (resolving_processed != U(0)), U(1), U(0))
    # //io.is_Waiting_Resolved := Mux(wait_for_resolving === 1.U, 1.U, 0.U)
    # csr add end

    addr_buffer.io.record <<= need_record_pc_4
    addr_buffer.io.addr_input <<= pc_4

    # Non-conditional jump
    noncon_address = Mux(noncon_addr_is_resolved, io.branch_addr, U(0))
    noncon_PC_Sel = Mux(noncon_addr_is_resolved, PC_Sel_new_addr, PC_Sel_pc_4)

    # Conditional jump
    update_status = Mux(con_addr_is_resolved,
                        Mux(io.PC_Src.to_bool(),
                            LookUpTable(dynamic_counter_status, {
                                Strong_Nottaken: Weak_Nottaken,
                                Weak_Nottaken: Weak_Taken,
                                Weak_Taken: Strong_Taken,
                                Strong_Taken: Strong_Taken,
                                ...: dynamic_counter_status
                            }), LookUpTable(dynamic_counter_status, {
                                Strong_Nottaken: Strong_Nottaken,
                                Weak_Nottaken: Strong_Nottaken,
                                Weak_Taken: Weak_Nottaken,
                                Strong_Taken: Weak_Taken,
                                ...: dynamic_counter_status
                            })), dynamic_counter_status)

    # csr change start
    # dynamic_counter_status <<= update_status
    dynamic_counter_status <<= Mux(is_a_jump_also_an_exception, dynamic_counter_status, update_status)
    # csr change end

    predict_fail = con_addr_is_resolved & ((update_status == Weak_Taken) | (update_status == Weak_Nottaken))
    # predict_success = con_addr_is_resolved & ((update_status == Strong_Taken) | (update_status == Strong_Nottaken))
    need_recover_pc = predict_fail & (((update_status == Weak_Taken) & (dynamic_counter_status == Strong_Taken)) |
                                      ((update_status == Weak_Nottaken) & (dynamic_counter_status == Weak_Taken)))

    flush = noncon_flush | predict_fail

    addr_buffer.io.flush <<= flush

    predict_PC_Sel = LookUpTable(dynamic_counter_status, {
        Strong_Nottaken: PC_Sel_pc_4,
        Weak_Nottaken: PC_Sel_pc_4,
        Weak_Taken: PC_Sel_new_addr,
        Strong_Taken: PC_Sel_new_addr,
        ...: PC_Sel_pc_4
    })

    predict_addr = (io.pc.to_sint() + CatBits(io.inst[31], io.inst[7], io.inst[30:25],
                                             io.inst[11:8], U.w(2)(0)).to_sint()).to_uint()

    con_PC_Sel = Mux(predict_fail, Mux(need_recover_pc, PC_Sel_pc_recover, PC_Sel_new_addr), PC_Sel_pc_4)

    # Output
    io.PC_Sel <<= Mux(noncon_addr_is_resolved, noncon_PC_Sel,
                      Mux(con_addr_is_resolved & predict_fail, con_PC_Sel,
                          Mux(is_conditional_jump, predict_PC_Sel, PC_Sel_pc_4)))

    io.new_addr <<= Mux(noncon_addr_is_resolved, io.branch_addr,
                        Mux(con_addr_is_resolved, io.branch_addr,
                            Mux(is_conditional_jump, predict_addr, U(0))))

    io.pc_recover <<= addr_buffer.io.front

    # Flush signal
    io.IF_ID_Flush <<= Mux(flush, IF_ID_Flush_True, IF_ID_Flush_False)
    io.ID_EX_Flush <<= Mux(flush, ID_EX_Flush_True, ID_EX_Flush_False)


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(BranchPredictor()), "BranchPredictor.fir")
    Emitter.dumpVerilog(f)
