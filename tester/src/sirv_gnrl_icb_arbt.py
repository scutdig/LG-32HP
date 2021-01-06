from pyhcl import *
from .sirv_gnrl_pipe_stage import sirv_gnrl_pipe_stage
from .sirv_gnrl_fifo import sirv_gnrl_fifo


def carray(el, len):
    ary = []
    for i in range(len):
        ary.append(el)
    return ary


def sirv_gnrl_icb_arbt(ARBT_SCHEME: int = 0,
                       ALLOW_0CYCL_RSP: int = 1,
                       FIFO_OUTS_NUM: int = 1,
                       FIFO_CUT_READY: int = 0,
                       ARBT_NUM: int = 4,
                       ARBT_PTR_W: int = 2,
                       USR_W: int = 1,
                       AW: int = 32,
                       DW: int = 64):
    class SirvGnrlIcbArbt(Module):

        # # /////////////////////////////////////////
        # # default parameters
        # ARBT_SCHEME = 0
        # ALLOW_0CYCL_RSP = 1
        # FIFO_OUTS_NUM = 1
        # FIFO_CUT_READY = 0
        # ARBT_NUM = 4
        # ARBT_PTR_W = 2
        # USR_W = 1
        # AW = 32
        # DW = 64
        # # /////////////////////////////////////////

        io = IO(

            # clk=Input(U.w(1)),
            # rst_n=Input(U.w(1)),
            o_icb_cmd_valid=Output(U.w(1)),
            o_icb_cmd_ready=Input(U.w(1)),
            o_icb_cmd_read=Output(U.w(1)),
            o_icb_cmd_addr=Output(U.w(AW)),
            o_icb_cmd_wdata=Output(U.w(DW)),
            o_icb_cmd_wmask=Output(U.w(int(DW/8))),
            o_icb_cmd_burst=Output(U.w(2)),
            o_icb_cmd_beat=Output(U.w(2)),
            o_icb_cmd_lock=Output(U.w(1)),
            o_icb_cmd_excl=Output(U.w(1)),
            o_icb_cmd_size=Output(U.w(2)),
            o_icb_cmd_usr=Output(U.w(USR_W)),

            o_icb_rsp_valid=Input(U.w(1)),
            o_icb_rsp_ready=Output(U.w(1)),
            o_icb_rsp_err=Input(U.w(1)),
            o_icb_rsp_excl_ok=Input(U.w(1)),
            o_icb_rsp_rdata=Input(U.w(DW)),
            o_icb_rsp_usr=Input(U.w(USR_W)),

            i_bus_icb_cmd_ready=Output(U.w(ARBT_NUM)),
            i_bus_icb_cmd_valid=Input(U.w(ARBT_NUM)),
            i_bus_icb_cmd_read=Input(U.w(ARBT_NUM)),
            i_bus_icb_cmd_addr=Input(U.w(ARBT_NUM*AW)),
            i_bus_icb_cmd_wdata=Input(U.w(ARBT_NUM*DW)),
            i_bus_icb_cmd_wmask=Input(U.w(int(ARBT_NUM*DW/8))),
            i_bus_icb_cmd_burst=Input(U.w(ARBT_NUM*2)),
            i_bus_icb_cmd_beat=Input(U.w(ARBT_NUM*2)),
            i_bus_icb_cmd_lock=Input(U.w(ARBT_NUM)),
            i_bus_icb_cmd_excl=Input(U.w(ARBT_NUM)),
            i_bus_icb_cmd_size=Input(U.w(ARBT_NUM*2)),
            i_bus_icb_cmd_usr=Input(U.w(ARBT_NUM*USR_W)),

            i_bus_icb_rsp_valid=Output(U.w(ARBT_NUM)),
            i_bus_icb_rsp_ready=Input(U.w(ARBT_NUM)),
            i_bus_icb_rsp_err=Output(U.w(ARBT_NUM)),
            i_bus_icb_rsp_excl_ok=Output(U.w(ARBT_NUM)),
            i_bus_icb_rsp_rdata=Output(U.w(ARBT_NUM*DW)),
            i_bus_icb_rsp_usr=Output(U.w(ARBT_NUM*USR_W))

        )

        # ///////////////////////////////////////////////////////////////////////////////////////////////
        # Intermediate variables' definition
        #
        # i_bus_icb_cmd_grt_vec = Wire(U.w(ARBT_NUM))
        # i_bus_icb_cmd_sel = Wire(U.w(ARBT_NUM))
        # replace
        i_bus_icb_cmd_grt_vec = Wire(Vec(ARBT_NUM, U.w(1)))
        i_bus_icb_cmd_sel = Wire(Vec(ARBT_NUM, U.w(1)))

        i_icb_cmd_read  = Wire(Vec(ARBT_NUM, U.w(1)))
        i_icb_cmd_addr  = Wire(Vec(ARBT_NUM, U.w(AW)))
        i_icb_cmd_wdata = Wire(Vec(ARBT_NUM, U.w(DW)))
        i_icb_cmd_wmask = Wire(Vec(ARBT_NUM, U.w(int(DW/8))))
        i_icb_cmd_burst = Wire(Vec(ARBT_NUM, U.w(2)))
        i_icb_cmd_beat  = Wire(Vec(ARBT_NUM, U.w(2)))
        i_icb_cmd_lock  = Wire(Vec(ARBT_NUM, U.w(1)))
        i_icb_cmd_excl  = Wire(Vec(ARBT_NUM, U.w(1)))
        i_icb_cmd_size  = Wire(Vec(ARBT_NUM, U.w(2)))
        i_icb_cmd_usr   = Wire(Vec(ARBT_NUM, U.w(USR_W)))

        i_icb_cmd_ready = Wire(Vec(ARBT_NUM, U.w(1)))
        i_icb_rsp_valid = Wire(Vec(ARBT_NUM, U.w(1)))


        # no use !!!
        # i_icb_rsp_port_id = Wire(U.w(ARBT_PTR_W))

        # rspid_fifo_rdat = Wire(U.w(ARBT_PTR_W))
        # rspid_fifo_wdat = Wire(U.w(ARBT_PTR_W))

        # o_icb_rsp_port_id = Wire(U.w(ARBT_PTR_W))

        # ///////////////////////////////////////////////////////////////////////////////////////////////

        if ARBT_NUM == 1:
            io.i_bus_icb_cmd_ready <<= io.o_icb_cmd_ready
            io.o_icb_cmd_valid     <<= io.i_bus_icb_cmd_valid
            io.o_icb_cmd_read      <<= io.i_bus_icb_cmd_read
            io.o_icb_cmd_addr      <<= io.i_bus_icb_cmd_addr
            io.o_icb_cmd_wdata     <<= io.i_bus_icb_cmd_wdata
            io.o_icb_cmd_wmask     <<= io.i_bus_icb_cmd_wmask
            io.o_icb_cmd_burst     <<= io.i_bus_icb_cmd_burst
            io.o_icb_cmd_beat      <<= io.i_bus_icb_cmd_beat
            io.o_icb_cmd_lock      <<= io.i_bus_icb_cmd_lock
            io.o_icb_cmd_excl      <<= io.i_bus_icb_cmd_excl
            io.o_icb_cmd_size      <<= io.i_bus_icb_cmd_size
            io.o_icb_cmd_usr       <<= io.i_bus_icb_cmd_usr

            io.o_icb_rsp_ready     <<= io.i_bus_icb_rsp_ready
            io.i_bus_icb_rsp_valid <<= io.o_icb_rsp_valid
            io.i_bus_icb_rsp_err   <<= io.o_icb_rsp_err
            io.i_bus_icb_rsp_excl_ok   <<= io.o_icb_rsp_excl_ok
            io.i_bus_icb_rsp_rdata <<= io.o_icb_rsp_rdata
            io.i_bus_icb_rsp_usr   <<= io.o_icb_rsp_usr
        else:
            # Instantiate two submodules and their called parameters
            if FIFO_OUTS_NUM == 1:
                u_sirv_gnrl_rspid_fifo = sirv_gnrl_pipe_stage(FIFO_CUT_READY, 1, ARBT_PTR_W)
            else:
                u_sirv_gnrl_rspid_fifo = sirv_gnrl_fifo(FIFO_CUT_READY, 0, FIFO_OUTS_NUM, ARBT_PTR_W)

            # ///////////////////////////////////////////////////////////////////////////////////////////////
            # assign o_icb_cmd_valid_real = |i_bus_icb_cmd_valid;
            o_icb_cmd_valid_real = U.w(1)(0)
            for tp in range(0, ARBT_NUM):
                o_icb_cmd_valid_real = o_icb_cmd_valid_real | io.i_bus_icb_cmd_valid[tp]
            # ///////////////////////////////////////////////////////////////////////////////////////////////

            # rspid_fifo_i_ready is attached to u_sirv_gnrl_rspid_fifo.io.i_rdy
            rspid_fifo_full    = (~u_sirv_gnrl_rspid_fifo.io.i_rdy)
            io.o_icb_cmd_valid <<= o_icb_cmd_valid_real & (~rspid_fifo_full)
            o_icb_cmd_ready_real = io.o_icb_cmd_ready & (~rspid_fifo_full)

            # if(ARBT_SCHEME == 0) must be true!!!
            for i in range(0, ARBT_NUM):
                if i == 0:
                    i_bus_icb_cmd_grt_vec[i] <<= U.w(1)(1)
                else:
                    # ///////////////////////////////////////////////////////////////////////////////////////////////
                    # assign i_bus_icb_cmd_grt_vec[i] =  ~(|i_bus_icb_cmd_valid[i-1:0]);
                    i_bus_icb_cmd_grt_vec_temp = U.w(1)(0)
                    for tq in range(0, i):
                        i_bus_icb_cmd_grt_vec_temp = i_bus_icb_cmd_grt_vec_temp | io.i_bus_icb_cmd_valid[tq]
                    i_bus_icb_cmd_grt_vec[i] <<= ~i_bus_icb_cmd_grt_vec_temp
                    # ///////////////////////////////////////////////////////////////////////////////////////////////
                i_bus_icb_cmd_sel[i] <<= i_bus_icb_cmd_grt_vec[i] & io.i_bus_icb_cmd_valid[i]

            # always @ (*) begin : i_arbt_indic_id_PROC
            i_arbt_indic_id = U.w(ARBT_PTR_W)(0)
            for j in range(ARBT_NUM):
                ary_0 = carray(i_bus_icb_cmd_sel[j], ARBT_PTR_W)
                i_arbt_indic_id = i_arbt_indic_id | (CatBits(*ary_0) & (U.w(ARBT_PTR_W)(j)))

            # rspid_fifo_o_valid is attached to u_sirv_gnrl_rspid_fifo.io.o_vld
            rspid_fifo_empty   = (~u_sirv_gnrl_rspid_fifo.io.o_vld)

            rspid_fifo_wen = io.o_icb_cmd_valid & io.o_icb_cmd_ready
            rspid_fifo_ren = io.o_icb_rsp_valid & io.o_icb_rsp_ready

            # rspid_fifo_wdat is attached to u_sirv_gnrl_rspid_fifo.io.i_dat!!!
            u_sirv_gnrl_rspid_fifo.io.i_dat <<= i_arbt_indic_id

            # if(ALLOW_0CYCL_RSP == 1) begin: allow_0rsp
            if ALLOW_0CYCL_RSP == 1:
                rspid_fifo_bypass = rspid_fifo_empty & rspid_fifo_wen & rspid_fifo_ren
                # rspid_fifo_rdat is attached to u_sirv_gnrl_rspid_fifo.io.o_dat!!!
                o_icb_rsp_port_id = Mux(rspid_fifo_empty.to_bool(), u_sirv_gnrl_rspid_fifo.io.i_dat, u_sirv_gnrl_rspid_fifo.io.o_dat)
                # ///////////////////////////////////////////////////////////////////////////////
                # deal with the [] problem !!! create a python variable o_icb_rsp_port_id_num
                # ARBT_PTR_NUM = 1, ARBT_NUM = 2
                # if o_icb_rsp_port_id == U(0):
                #     o_icb_rsp_port_id_num = 0
                # if o_icb_rsp_port_id == U(1):
                #     o_icb_rsp_port_id_num = 1

                for i in range(0, 2**ARBT_PTR_W):
                    if o_icb_rsp_port_id == U(i):
                        o_icb_rsp_port_id_num = i
                # ///////////////////////////////////////////////////////////////////////////////

                o_icb_rsp_valid_pre = io.o_icb_rsp_valid

                # o_icb_rsp_ready_pre = io.i_bus_icb_rsp_ready[o_icb_rsp_port_id]
                # io.o_icb_rsp_ready  <<= o_icb_rsp_ready_pre
                # replace
                io.o_icb_rsp_ready <<= io.i_bus_icb_rsp_ready[o_icb_rsp_port_id_num]

            # else begin: no_allow_0rsp
            else:
                rspid_fifo_bypass = U.w(1)(0)
                # rspid_fifo_rdat is attached to u_sirv_gnrl_rspid_fifo.io.o_dat!!!
                o_icb_rsp_port_id = Mux(rspid_fifo_empty.to_bool(), U.w(ARBT_PTR_W)(0), u_sirv_gnrl_rspid_fifo.io.o_dat)
                # ///////////////////////////////////////////////////////////////////////////////
                # deal with the [] problem !!! create a python variable o_icb_rsp_port_id_num
                # ARBT_PTR_NUM = 1, ARBT_NUM = 2
                # if o_icb_rsp_port_id == U(0):
                #     o_icb_rsp_port_id_num = 0
                # if o_icb_rsp_port_id == U(1):
                #     o_icb_rsp_port_id_num = 1

                for i in range(0, 2**ARBT_PTR_W):
                    if o_icb_rsp_port_id == U(i):
                        o_icb_rsp_port_id_num = i
                # ///////////////////////////////////////////////////////////////////////////////
                o_icb_rsp_valid_pre = (~rspid_fifo_empty) & io.o_icb_rsp_valid

                # o_icb_rsp_ready_pre = io.i_bus_icb_rsp_ready[o_icb_rsp_port_id]
                # io.o_icb_rsp_ready <<= (~rspid_fifo_empty) & o_icb_rsp_ready_pre
                # replace
                io.o_icb_rsp_ready <<= (~rspid_fifo_empty) & io.i_bus_icb_rsp_ready[o_icb_rsp_port_id_num]

            for i in range(0, ARBT_NUM):
                i_icb_cmd_read [i] <<= io.i_bus_icb_cmd_read [(i+1)*1     -1 : i*1     ]
                i_icb_cmd_addr [i] <<= io.i_bus_icb_cmd_addr [(i+1)*AW    -1 : i*AW    ]
                i_icb_cmd_wdata[i] <<= io.i_bus_icb_cmd_wdata[(i+1)*DW    -1 : i*DW    ]
                i_icb_cmd_wmask[i] <<= io.i_bus_icb_cmd_wmask[(i+1)*(int(DW/8))-1 : i*(int(DW/8))]
                i_icb_cmd_burst[i] <<= io.i_bus_icb_cmd_burst[(i+1)*2     -1 : i*2     ]
                i_icb_cmd_beat [i] <<= io.i_bus_icb_cmd_beat [(i+1)*2     -1 : i*2     ]
                i_icb_cmd_lock [i] <<= io.i_bus_icb_cmd_lock [(i+1)*1     -1 : i*1     ]
                i_icb_cmd_excl [i] <<= io.i_bus_icb_cmd_excl [(i+1)*1     -1 : i*1     ]
                i_icb_cmd_size [i] <<= io.i_bus_icb_cmd_size [(i+1)*2     -1 : i*2     ]
                i_icb_cmd_usr  [i] <<= io.i_bus_icb_cmd_usr  [(i+1)*USR_W -1 : i*USR_W ]
                #
                i_icb_cmd_ready[i] <<= i_bus_icb_cmd_grt_vec[i] & o_icb_cmd_ready_real
                # o_icb_rsp_port_id == i <==>o_icb_rsp_port_id == U.w(ARBT_PTR_W)(i) ???
                i_icb_rsp_valid[i] <<= o_icb_rsp_valid_pre & (o_icb_rsp_port_id == U.w(ARBT_PTR_W)(i))

            io.i_bus_icb_cmd_ready <<= CatVecH2L(i_icb_cmd_ready)
            io.i_bus_icb_rsp_valid <<= CatVecH2L(i_icb_rsp_valid)

            # print(i_icb_cmd_ready)
            # print(CatVecH2L(i_icb_cmd_ready))
            # print(io.i_bus_icb_cmd_ready)

            for j in range(0, ARBT_NUM):

                ary_1 = carray(i_bus_icb_cmd_sel[j], 1)
                ary_2 = carray(i_bus_icb_cmd_sel[j], AW)
                ary_3 = carray(i_bus_icb_cmd_sel[j], DW)
                ary_4 = carray(i_bus_icb_cmd_sel[j], int(DW/8))
                ary_5 = carray(i_bus_icb_cmd_sel[j], 2)
                ary_6 = carray(i_bus_icb_cmd_sel[j], 2)
                ary_7 = carray(i_bus_icb_cmd_sel[j], 1)
                ary_8 = carray(i_bus_icb_cmd_sel[j], 1)
                ary_9 = carray(i_bus_icb_cmd_sel[j], 2)
                ary_10 = carray(i_bus_icb_cmd_sel[j], USR_W)

                io.o_icb_cmd_read  <<= U.w(1)(0)         | (CatBits(*ary_1) & i_icb_cmd_read[j])
                io.o_icb_cmd_addr  <<= U.w(AW)(0)        | (CatBits(*ary_2) & i_icb_cmd_addr[j])
                io.o_icb_cmd_wdata <<= U.w(DW)(0)        | (CatBits(*ary_3) & i_icb_cmd_wdata[j])
                io.o_icb_cmd_wmask <<= U.w(int(DW/8))(0) | (CatBits(*ary_4) & i_icb_cmd_wmask[j])
                io.o_icb_cmd_burst <<= U.w(2)(0)         | (CatBits(*ary_5) & i_icb_cmd_burst[j])
                io.o_icb_cmd_beat  <<= U.w(2)(0)         | (CatBits(*ary_6) & i_icb_cmd_beat[j])
                io.o_icb_cmd_lock  <<= U.w(1)(0)         | (CatBits(*ary_7) & i_icb_cmd_lock[j])
                io.o_icb_cmd_excl  <<= U.w(1)(0)         | (CatBits(*ary_8) & i_icb_cmd_excl[j])
                io.o_icb_cmd_size  <<= U.w(2)(0)         | (CatBits(*ary_9) & i_icb_cmd_size[j])
                io.o_icb_cmd_usr   <<= U.w(USR_W)(0)     | (CatBits(*ary_10) & i_icb_cmd_usr[j])

            u_sirv_gnrl_rspid_fifo.io.i_vld <<= rspid_fifo_wen & (~rspid_fifo_bypass)
            u_sirv_gnrl_rspid_fifo.io.o_rdy <<= rspid_fifo_ren & (~rspid_fifo_bypass)

            ary_11 = carray(io.o_icb_rsp_err, ARBT_NUM)
            ary_12 = carray(io.o_icb_rsp_excl_ok, ARBT_NUM)
            ary_13 = carray(io.o_icb_rsp_rdata, ARBT_NUM)
            ary_14 = carray(io.o_icb_rsp_usr, ARBT_NUM)

            io.i_bus_icb_rsp_err     <<= CatBits(*ary_11)
            io.i_bus_icb_rsp_excl_ok <<= CatBits(*ary_12)
            io.i_bus_icb_rsp_rdata   <<= CatBits(*ary_13)
            io.i_bus_icb_rsp_usr     <<= CatBits(*ary_14)

    return SirvGnrlIcbArbt()


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(sirv_gnrl_icb_arbt(0, 0, 1, 1, 2, 1, 1, 32, 32)), "sirv_gnrl_icb_arbt.fir")
    Emitter.dumpVerilog(f)











