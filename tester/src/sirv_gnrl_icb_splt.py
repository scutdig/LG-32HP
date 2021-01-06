from pyhcl import *

from .sirv_gnrl_pipe_stage import sirv_gnrl_pipe_stage
from .sirv_gnrl_fifo import sirv_gnrl_fifo


def carray(el, len):
    ary = []
    for i in range(len):
        ary.append(el)
    return ary


def sirv_gnrl_icb_splt(ALLOW_DIFF = 1,
                       ALLOW_0CYCL_RSP: int = 1,
                       FIFO_OUTS_NUM: int = 8,
                       FIFO_CUT_READY: int = 0,
                       # SPLT_NUM 必须与 SPLT_PTR_W等长！！！（因为后面会进行两者变量的&，(o_icb_rsp_valid & o_icb_rsp_port_id)）
                       SPLT_NUM: int = 4,
                       SPLT_PTR_W: int = 4,
                       SPLT_PTR_1HOT: int = 1,
                       USR_W: int = 1,
                       AW: int = 32,
                       DW: int = 64,
                       # not use !!!
                       VLD_MSK_PAYLOAD: int = 0):
    class SirvGnrlIcbSplt(Module):

        # # /////////////////////////////////////////
        # # default parameters
        # ALLOW_DIFF = 1
        # ALLOW_0CYCL_RSP = 1
        # FIFO_OUTS_NUM = 8
        # FIFO_CUT_READY = 0
        # SPLT_NUM = 4
        # SPLT_PTR_W = 4
        # SPLT_PTR_1HOT = 1
        # USR_W = 1
        # AW = 32
        # DW = 64
        # not use !!!
        # VLD_MSK_PAYLOAD = 0
        # # /////////////////////////////////////////

        io = IO(

            # clk=Input(U.w(1)),
            # rst_n=Input(U.w(1)),
            i_icb_splt_indic=Input(U.w(SPLT_NUM)),

            i_icb_cmd_valid=Input(U.w(1)),
            i_icb_cmd_ready=Output(U.w(1)),
            i_icb_cmd_read=Input(U.w(1)),
            i_icb_cmd_addr=Input(U.w(AW)),
            i_icb_cmd_wdata=Input(U.w(DW)),
            i_icb_cmd_wmask=Input(U.w(int(DW/8))),
            i_icb_cmd_burst=Input(U.w(2)),
            i_icb_cmd_beat=Input(U.w(2)),
            i_icb_cmd_lock=Input(U.w(1)),
            i_icb_cmd_excl=Input(U.w(1)),
            i_icb_cmd_size=Input(U.w(2)),
            i_icb_cmd_usr=Input(U.w(USR_W)),

            i_icb_rsp_valid=Output(U.w(1)),
            i_icb_rsp_ready=Input(U.w(1)),
            i_icb_rsp_err=Output(U.w(1)),
            i_icb_rsp_excl_ok=Output(U.w(1)),
            i_icb_rsp_rdata=Output(U.w(DW)),
            i_icb_rsp_usr=Output(U.w(USR_W)),

            o_bus_icb_cmd_ready=Input(U.w(SPLT_NUM)),
            o_bus_icb_cmd_valid=Output(U.w(SPLT_NUM)),
            o_bus_icb_cmd_read=Output(U.w(SPLT_NUM)),
            o_bus_icb_cmd_addr=Output(U.w(SPLT_NUM*AW)),
            o_bus_icb_cmd_wdata=Output(U.w(SPLT_NUM*DW)),
            o_bus_icb_cmd_wmask=Output(U.w(int(SPLT_NUM*DW/8))),
            o_bus_icb_cmd_burst=Output(U.w(SPLT_NUM*2)),
            o_bus_icb_cmd_beat=Output(U.w(SPLT_NUM*2)),
            o_bus_icb_cmd_lock=Output(U.w(SPLT_NUM)),
            o_bus_icb_cmd_excl=Output(U.w(SPLT_NUM)),
            o_bus_icb_cmd_size=Output(U.w(SPLT_NUM*2)),
            o_bus_icb_cmd_usr=Output(U.w(SPLT_NUM*USR_W)),

            o_bus_icb_rsp_valid=Input(U.w(SPLT_NUM)),
            o_bus_icb_rsp_ready=Output(U.w(SPLT_NUM)),
            o_bus_icb_rsp_err=Input(U.w(SPLT_NUM)),
            o_bus_icb_rsp_excl_ok=Input(U.w(SPLT_NUM)),
            o_bus_icb_rsp_rdata=Input(U.w(SPLT_NUM*DW)),
            o_bus_icb_rsp_usr=Input(U.w(SPLT_NUM*USR_W))

        )

        # ///////////////////////////////////////////////////////////////////////////////////////////////
        # Intermediate variables' definition
        # cmd
        o_icb_cmd_valid = Wire(Vec(SPLT_NUM, U.w(1)))
        o_icb_cmd_ready = Wire(Vec(SPLT_NUM, U.w(1)))
        o_icb_cmd_read  = Wire(Vec(SPLT_NUM, U.w(1)))
        o_icb_cmd_addr  = Wire(Vec(SPLT_NUM, U.w(AW)))
        o_icb_cmd_wdata = Wire(Vec(SPLT_NUM, U.w(DW)))
        o_icb_cmd_wmask = Wire(Vec(SPLT_NUM, U.w(int(DW/8))))
        o_icb_cmd_burst = Wire(Vec(SPLT_NUM, U.w(2)))
        o_icb_cmd_beat  = Wire(Vec(SPLT_NUM, U.w(2)))
        o_icb_cmd_lock  = Wire(Vec(SPLT_NUM, U.w(1)))
        o_icb_cmd_excl  = Wire(Vec(SPLT_NUM, U.w(1)))
        o_icb_cmd_size  = Wire(Vec(SPLT_NUM, U.w(2)))
        o_icb_cmd_usr   = Wire(Vec(SPLT_NUM, U.w(USR_W)))
        # rsp
        o_icb_rsp_valid   = Wire(Vec(SPLT_NUM, U.w(1)))
        o_icb_rsp_ready   = Wire(Vec(SPLT_NUM, U.w(1)))
        o_icb_rsp_err     = Wire(Vec(SPLT_NUM, U.w(1)))
        o_icb_rsp_excl_ok = Wire(Vec(SPLT_NUM, U.w(1)))
        o_icb_rsp_rdata   = Wire(Vec(SPLT_NUM, U.w(DW)))
        o_icb_rsp_usr     = Wire(Vec(SPLT_NUM, U.w(USR_W)))

        o_icb_rsp_port_id = Wire(U.w(SPLT_PTR_W))
        # o_icb_rsp_port_id_vec = Wire(Vec(SPLT_PTR_W, U.w(1)))
        # o_icb_rsp_port_id   <<= CatVecH2L(o_icb_rsp_port_id_vec)

        # 方便两个if之间相互传值
        i_icb_rsp_valid_pre = Wire(U.w(1))
        i_icb_rsp_ready_pre = Wire(U.w(1))

        # mid_temp = Wire(U.w(SPLT_PTR_W))
        # ///////////////////////////////////////////////////////////////////////////////////////////////

        if SPLT_NUM == 1:
            io.i_icb_cmd_ready     <<= io.o_bus_icb_cmd_ready
            io.o_bus_icb_cmd_valid <<= io.i_icb_cmd_valid
            io.o_bus_icb_cmd_read  <<= io.i_icb_cmd_read
            io.o_bus_icb_cmd_addr  <<= io.i_icb_cmd_addr
            io.o_bus_icb_cmd_wdata <<= io.i_icb_cmd_wdata
            io.o_bus_icb_cmd_wmask <<= io.i_icb_cmd_wmask
            io.o_bus_icb_cmd_burst <<= io.i_icb_cmd_burst
            io.o_bus_icb_cmd_beat  <<= io.i_icb_cmd_beat
            io.o_bus_icb_cmd_lock  <<= io.i_icb_cmd_lock
            io.o_bus_icb_cmd_excl  <<= io.i_icb_cmd_excl
            io.o_bus_icb_cmd_size  <<= io.i_icb_cmd_size
            io.o_bus_icb_cmd_usr   <<= io.i_icb_cmd_usr

            io.o_bus_icb_rsp_ready <<= io.i_icb_rsp_ready
            io.i_icb_rsp_valid     <<= io.o_bus_icb_rsp_valid
            io.i_icb_rsp_err       <<= io.o_bus_icb_rsp_err
            io.i_icb_rsp_excl_ok   <<= io.o_bus_icb_rsp_excl_ok
            io.i_icb_rsp_rdata     <<= io.o_bus_icb_rsp_rdata
            io.i_icb_rsp_usr       <<= io.o_bus_icb_rsp_usr
        else:


            # ///////////////////////////////////////////////////////////////////////////////////////////////
            # Instantiate 2 submodules and their called parameters

            if FIFO_OUTS_NUM == 1:
                u_sirv_gnrl_rspid_fifo = sirv_gnrl_pipe_stage(FIFO_CUT_READY, 1, SPLT_PTR_W)
                # u_sirv_gnrl_rspid_fifo = sirv_gnrl_pipe_stage(1, 1, 6)
            else:
                u_sirv_gnrl_rspid_fifo = sirv_gnrl_fifo(FIFO_CUT_READY, 0, FIFO_OUTS_NUM, SPLT_PTR_W)


            # ///////////////////////////////////////////////////////////////////////////////////////////////

            for i in range(0, SPLT_NUM):
                # cmd
                o_icb_cmd_ready[i]                 <<= io.o_bus_icb_cmd_ready[(i+1)*1-1:(i)*1]
                # rsp
                o_icb_rsp_valid[i]                 <<= io.o_bus_icb_rsp_valid[(i+1)*1-1:i*1]
                o_icb_rsp_err[i]                   <<= io.o_bus_icb_rsp_err[(i+1)*1-1:i*1]
                o_icb_rsp_excl_ok[i]               <<= io.o_bus_icb_rsp_excl_ok[(i+1)*1-1:i*1]
                o_icb_rsp_rdata[i]                 <<= io.o_bus_icb_rsp_rdata[(i+1)*DW-1:i*DW]
                o_icb_rsp_usr[i]                   <<= io.o_bus_icb_rsp_usr[(i+1)*USR_W-1:i*USR_W]

            sel_o_apb_cmd_ready = U.w(1)(0)
            for j in range(0, SPLT_NUM):
                sel_o_apb_cmd_ready = sel_o_apb_cmd_ready | (io.i_icb_splt_indic[j] & o_icb_cmd_ready[j])

            i_icb_cmd_ready_pre = sel_o_apb_cmd_ready

            rspid_fifo_empty = (~u_sirv_gnrl_rspid_fifo.io.o_vld)
            rspid_fifo_full = (~u_sirv_gnrl_rspid_fifo.io.i_rdy)
            if ALLOW_DIFF == 1:
                i_icb_cmd_valid_pre = io.i_icb_cmd_valid & (~rspid_fifo_full)
                io.i_icb_cmd_ready <<= i_icb_cmd_ready_pre & (~rspid_fifo_full)
            else:
                cmd_diff_branch = (~rspid_fifo_empty) & (~(u_sirv_gnrl_rspid_fifo.io.i_dat == u_sirv_gnrl_rspid_fifo.io.o_dat))
                i_icb_cmd_valid_pre = io.i_icb_cmd_valid & (~cmd_diff_branch) & (~rspid_fifo_full)
                io.i_icb_cmd_ready <<= i_icb_cmd_ready_pre & (~cmd_diff_branch) & (~rspid_fifo_full)

            if SPLT_PTR_1HOT == 1:
                i_splt_indic_id = io.i_icb_splt_indic
            else:
                ary_0 = carray(U.w(1)(0), SPLT_PTR_W)
                i_splt_indic_id = CatBits(*ary_0)
                for j in range(0, SPLT_NUM):
                    ary_1 = carray(io.i_icb_splt_indic[j], SPLT_PTR_W)
                    i_splt_indic_id = i_splt_indic_id | (CatBits(*ary_1) & U.w(SPLT_PTR_W)(j))

            rspid_fifo_wen = io.i_icb_cmd_valid & io.i_icb_cmd_ready
            rspid_fifo_ren = io.i_icb_rsp_valid & io.i_icb_rsp_ready

            if ALLOW_0CYCL_RSP == 1:
                rspid_fifo_bypass = rspid_fifo_empty & rspid_fifo_wen & rspid_fifo_ren
                o_icb_rsp_port_id <<= Mux(rspid_fifo_empty == U.w(1)(1), u_sirv_gnrl_rspid_fifo.io.i_dat, u_sirv_gnrl_rspid_fifo.io.o_dat)

                io.i_icb_rsp_valid <<= i_icb_rsp_valid_pre
                i_icb_rsp_ready_pre <<= io.i_icb_rsp_ready
            else:
                rspid_fifo_bypass = U.w(1)(0)
                ary_2 = carray(U.w(1)(0), SPLT_PTR_W)
                o_icb_rsp_port_id <<= Mux(rspid_fifo_empty == U.w(1)(1), CatBits(*ary_2), u_sirv_gnrl_rspid_fifo.io.o_dat)
                io.i_icb_rsp_valid <<= (~rspid_fifo_empty) & i_icb_rsp_valid_pre
                i_icb_rsp_ready_pre <<= (~rspid_fifo_empty) & io.i_icb_rsp_ready

            u_sirv_gnrl_rspid_fifo.io.i_vld <<= rspid_fifo_wen & (~rspid_fifo_bypass)
            u_sirv_gnrl_rspid_fifo.io.o_rdy <<= rspid_fifo_ren & (~rspid_fifo_bypass)
            u_sirv_gnrl_rspid_fifo.io.i_dat <<= i_splt_indic_id

            for i in range(0, SPLT_NUM):
                o_icb_cmd_valid[i] <<= io.i_icb_splt_indic[i] & i_icb_cmd_valid_pre
                if VLD_MSK_PAYLOAD == 0:
                    o_icb_cmd_read [i] <<= io.i_icb_cmd_read
                    o_icb_cmd_addr [i] <<= io.i_icb_cmd_addr
                    o_icb_cmd_wdata[i] <<= io.i_icb_cmd_wdata
                    o_icb_cmd_wmask[i] <<= io.i_icb_cmd_wmask
                    o_icb_cmd_burst[i] <<= io.i_icb_cmd_burst
                    o_icb_cmd_beat [i] <<= io.i_icb_cmd_beat
                    o_icb_cmd_lock [i] <<= io.i_icb_cmd_lock
                    o_icb_cmd_excl [i] <<= io.i_icb_cmd_excl
                    o_icb_cmd_size [i] <<= io.i_icb_cmd_size
                    o_icb_cmd_usr  [i] <<= io.i_icb_cmd_usr
                else:
                    ary_3  = carray(o_icb_cmd_valid[i], 1)
                    ary_4  = carray(o_icb_cmd_valid[i], AW)
                    ary_5  = carray(o_icb_cmd_valid[i], DW)
                    ary_6  = carray(o_icb_cmd_valid[i], int(DW/8))
                    ary_7  = carray(o_icb_cmd_valid[i], 2)
                    ary_8  = carray(o_icb_cmd_valid[i], 2)
                    ary_9  = carray(o_icb_cmd_valid[i], 1)
                    ary_10 = carray(o_icb_cmd_valid[i], 1)
                    ary_11 = carray(o_icb_cmd_valid[i], 2)
                    ary_12 = carray(o_icb_cmd_valid[i], USR_W)

                    o_icb_cmd_read [i] <<= CatBits(*ary_3)  & io.i_icb_cmd_read
                    o_icb_cmd_addr [i] <<= CatBits(*ary_4)  & io.i_icb_cmd_addr
                    o_icb_cmd_wdata[i] <<= CatBits(*ary_5)  & io.i_icb_cmd_wdata
                    o_icb_cmd_wmask[i] <<= CatBits(*ary_6)  & io.i_icb_cmd_wmask
                    o_icb_cmd_burst[i] <<= CatBits(*ary_7)  & io.i_icb_cmd_burst
                    o_icb_cmd_beat [i] <<= CatBits(*ary_8)  & io.i_icb_cmd_beat
                    o_icb_cmd_lock [i] <<= CatBits(*ary_9)  & io.i_icb_cmd_lock
                    o_icb_cmd_excl [i] <<= CatBits(*ary_10) & io.i_icb_cmd_excl
                    o_icb_cmd_size [i] <<= CatBits(*ary_11) & io.i_icb_cmd_size
                    o_icb_cmd_usr  [i] <<= CatBits(*ary_12) & io.i_icb_cmd_usr

            if SPLT_PTR_1HOT == 1:
                for i in range(0, SPLT_NUM):
                    o_icb_rsp_ready[i] <<= (o_icb_rsp_port_id[i] & i_icb_rsp_ready_pre)

                # 1-hot code, so SPLT_NUM == SPLT_PTR_W
                i_icb_rsp_valid_pre_temp = U.w(1)(0)
                mid_temp = (CatVecH2L(o_icb_rsp_valid) & o_icb_rsp_port_id)
                for tp in range(0, SPLT_PTR_W):
                    i_icb_rsp_valid_pre_temp = i_icb_rsp_valid_pre_temp | mid_temp[tp]
                i_icb_rsp_valid_pre <<= i_icb_rsp_valid_pre_temp

                sel_i_icb_rsp_err = U.w(1)(0)
                sel_i_icb_rsp_excl_ok = U.w(1)(0)

                ary13 = carray(U.w(1)(0), DW)
                sel_i_icb_rsp_rdata = CatBits(*ary13)
                ary14 = carray(U.w(1)(0), USR_W)
                sel_i_icb_rsp_usr = CatBits(*ary14)

                for j in range(SPLT_NUM):

                    ary15 = carray(o_icb_rsp_port_id[j], DW)
                    ary16 = carray(o_icb_rsp_port_id[j], USR_W)

                    sel_i_icb_rsp_err     = sel_i_icb_rsp_err     | (o_icb_rsp_port_id[j] & o_icb_rsp_err[j])
                    sel_i_icb_rsp_excl_ok = sel_i_icb_rsp_excl_ok | (o_icb_rsp_port_id[j] & o_icb_rsp_excl_ok[j])
                    sel_i_icb_rsp_rdata   = sel_i_icb_rsp_rdata   | (CatBits(*ary15) & o_icb_rsp_rdata[j])
                    sel_i_icb_rsp_usr     = sel_i_icb_rsp_usr     | (CatBits(*ary16) & o_icb_rsp_usr[j])

                io.i_icb_rsp_err     <<= sel_i_icb_rsp_err
                io.i_icb_rsp_excl_ok <<= sel_i_icb_rsp_excl_ok
                io.i_icb_rsp_rdata   <<= sel_i_icb_rsp_rdata
                io.i_icb_rsp_usr     <<= sel_i_icb_rsp_usr

            else:
                for j in range(0, 2**SPLT_PTR_W):
                    if o_icb_rsp_port_id == U(j):
                        o_icb_rsp_port_id_num = j

                for i in range(0, SPLT_NUM):
                    o_icb_rsp_ready[i] <<= (o_icb_rsp_port_id_num == i) & (i_icb_rsp_ready_pre == U.w(1)(1))

                i_icb_rsp_valid_pre  <<= o_icb_rsp_valid[o_icb_rsp_port_id_num]

                io.i_icb_rsp_err     <<= o_icb_rsp_err    [o_icb_rsp_port_id_num]
                io.i_icb_rsp_excl_ok <<= o_icb_rsp_excl_ok[o_icb_rsp_port_id_num]
                io.i_icb_rsp_rdata   <<= o_icb_rsp_rdata  [o_icb_rsp_port_id_num]
                io.i_icb_rsp_usr     <<= o_icb_rsp_usr    [o_icb_rsp_port_id_num]

            # ///////////////////////////////////////////////////////////////////////////////////////////////
            # io.output端口 <<= CatVecH2L(Vec signal)
            # cmd output
            io.o_bus_icb_cmd_valid <<= CatVecH2L(o_icb_cmd_valid)
            io.o_bus_icb_cmd_read <<= CatVecH2L(o_icb_cmd_read)
            io.o_bus_icb_cmd_addr <<= CatVecH2L(o_icb_cmd_addr)
            io.o_bus_icb_cmd_wdata <<= CatVecH2L(o_icb_cmd_wdata)
            io.o_bus_icb_cmd_wmask <<= CatVecH2L(o_icb_cmd_wmask)
            io.o_bus_icb_cmd_burst <<= CatVecH2L(o_icb_cmd_burst)
            io.o_bus_icb_cmd_beat <<= CatVecH2L(o_icb_cmd_beat)
            io.o_bus_icb_cmd_lock <<= CatVecH2L(o_icb_cmd_lock)
            io.o_bus_icb_cmd_excl <<= CatVecH2L(o_icb_cmd_excl)
            io.o_bus_icb_cmd_size <<= CatVecH2L(o_icb_cmd_size)
            io.o_bus_icb_cmd_usr <<= CatVecH2L(o_icb_cmd_usr)
            # rsp output
            io.o_bus_icb_rsp_ready <<= CatVecH2L(o_icb_rsp_ready)
            # ///////////////////////////////////////////////////////////////////////////////////////////////

    return SirvGnrlIcbSplt()


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(sirv_gnrl_icb_splt(0, 1, 1, 1, 6, 6, 1, 1, 32, 32, 0)), "sirv_gnrl_icb_splt.fir")
    Emitter.dumpVerilog(f)

