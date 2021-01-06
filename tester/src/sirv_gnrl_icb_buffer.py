from pyhcl import *
from .sirv_gnrl_fifo import sirv_gnrl_fifo
from .sirv_gnrl_dfflr import sirv_gnrl_dfflr


def carray(el, len):
    ary = []
    for i in range(len):
        ary.append(el)
    return ary

def sirv_gnrl_icb_buffer(OUTS_CNT_W: int = 1,
                         AW: int = 32,
                         DW: int = 32,
                         CMD_DP: int = 0,
                         RSP_DP: int = 0,
                         CMD_CUT_READY: int = 0,
                         RSP_CUT_READY: int = 0,
                         USR_W: int = 1):
    class SirvGnrlIcbBuffer(Module):

        # # /////////////////////////////////////////
        # # default parameters
        # OUTS_CNT_W = 1
        # AW = 32
        # DW = 32
        # CMD_DP = 0
        # RSP_DP = 0
        # CMD_CUT_READY = 0
        # RSP_CUT_READY = 0
        # USR_W = 1
        # # /////////////////////////////////////////

        io = IO(

            # clk=Input(U.w(1)),
            # rst_n=Input(U.w(1)),
            icb_buffer_active=Output(U.w(1)),

            i_icb_cmd_valid=Input(U.w(1)),
            i_icb_cmd_ready=Output(U.w(1)),
            i_icb_cmd_read=Input(U.w(1)),
            i_icb_cmd_addr=Input(U.w(AW)),
            i_icb_cmd_wdata=Input(U.w(DW)),
            i_icb_cmd_wmask=Input(U.w(int(DW/8))),
            i_icb_cmd_lock=Input(U.w(1)),
            i_icb_cmd_excl=Input(U.w(1)),
            i_icb_cmd_size=Input(U.w(2)),
            i_icb_cmd_burst=Input(U.w(2)),
            i_icb_cmd_beat=Input(U.w(2)),
            i_icb_cmd_usr=Input(U.w(USR_W)),

            i_icb_rsp_valid=Output(U.w(1)),
            i_icb_rsp_ready=Input(U.w(1)),
            i_icb_rsp_err=Output(U.w(1)),
            i_icb_rsp_excl_ok=Output(U.w(1)),
            i_icb_rsp_rdata=Output(U.w(DW)),
            i_icb_rsp_usr=Output(U.w(USR_W)),

            o_icb_cmd_valid=Output(U.w(1)),
            o_icb_cmd_ready=Input(U.w(1)),
            o_icb_cmd_read=Output(U.w(1)),
            o_icb_cmd_addr=Output(U.w(AW)),
            o_icb_cmd_wdata=Output(U.w(DW)),
            o_icb_cmd_wmask=Output(U.w(int(DW/8))),
            o_icb_cmd_lock=Output(U.w(1)),
            o_icb_cmd_excl=Output(U.w(1)),
            o_icb_cmd_size=Output(U.w(2)),
            o_icb_cmd_burst=Output(U.w(2)),
            o_icb_cmd_beat=Output(U.w(2)),
            o_icb_cmd_usr=Output(U.w(USR_W)),

            o_icb_rsp_valid=Input(U.w(1)),
            o_icb_rsp_ready=Output(U.w(1)),
            o_icb_rsp_err=Input(U.w(1)),
            o_icb_rsp_excl_ok=Input(U.w(1)),
            o_icb_rsp_rdata=Input(U.w(DW)),
            o_icb_rsp_usr=Input(U.w(USR_W))

        )

        # ///////////////////////////////////////////////////////////////////////////////////////////////
        # Intermediate variables' definition

        # ///////////////////////////////////////////////////////////////////////////////////////////////

        CMD_PACK_W = (1 + AW + DW + int(DW/8) + 1 + 1 + 2 + 2 + 2 + USR_W)
        RSP_PACK_W = (2 + DW + USR_W)

        # ///////////////////////////////////////////////////////////////////////////////////////////////
        # Instantiate 3 submodules and their called parameters

        u_sirv_gnrl_cmd_fifo = sirv_gnrl_fifo(CMD_CUT_READY, 0, CMD_DP, CMD_PACK_W)
        u_sirv_gnrl_rsp_fifo = sirv_gnrl_fifo(RSP_CUT_READY, 0, RSP_DP, RSP_PACK_W)

        outs_cnt_dfflr = sirv_gnrl_dfflr(OUTS_CNT_W)

        # ///////////////////////////////////////////////////////////////////////////////////////////////

        # ///////////////////////////////////////////////////////////////////////////////////////////////
        # u_sirv_gnrl_cmd_fifo connect
        u_sirv_gnrl_cmd_fifo.io.i_vld <<= io.i_icb_cmd_valid
        io.i_icb_cmd_ready <<= u_sirv_gnrl_cmd_fifo.io.i_rdy
        u_sirv_gnrl_cmd_fifo.io.i_dat <<= CatBits(io.i_icb_cmd_read,
                                                  io.i_icb_cmd_addr,
                                                  io.i_icb_cmd_wdata,
                                                  io.i_icb_cmd_wmask,
                                                  io.i_icb_cmd_lock,
                                                  io.i_icb_cmd_excl,
                                                  io.i_icb_cmd_size,
                                                  io.i_icb_cmd_burst,
                                                  io.i_icb_cmd_beat,
                                                  io.i_icb_cmd_usr)
        io.o_icb_cmd_valid <<= u_sirv_gnrl_cmd_fifo.io.o_vld
        u_sirv_gnrl_cmd_fifo.io.o_rdy <<= io.o_icb_cmd_ready
        io.o_icb_cmd_read <<= u_sirv_gnrl_cmd_fifo.io.o_dat[CMD_PACK_W-1]
        io.o_icb_cmd_addr <<= u_sirv_gnrl_cmd_fifo.io.o_dat[CMD_PACK_W-2:CMD_PACK_W-1-AW]
        io.o_icb_cmd_wdata <<= u_sirv_gnrl_cmd_fifo.io.o_dat[CMD_PACK_W-2-AW:CMD_PACK_W-1-AW-DW]
        io.o_icb_cmd_wmask <<= u_sirv_gnrl_cmd_fifo.io.o_dat[CMD_PACK_W-2-AW-DW:CMD_PACK_W-1-AW-DW-int(DW/8)]
        io.o_icb_cmd_lock <<= u_sirv_gnrl_cmd_fifo.io.o_dat[CMD_PACK_W-2-AW-DW-int(DW/8):CMD_PACK_W-1-AW-DW-int(DW/8)-1]
        io.o_icb_cmd_excl <<= u_sirv_gnrl_cmd_fifo.io.o_dat[CMD_PACK_W-2-AW-DW-int(DW/8)-1:CMD_PACK_W-1-AW-DW-int(DW/8)-1-1]
        io.o_icb_cmd_size <<= u_sirv_gnrl_cmd_fifo.io.o_dat[CMD_PACK_W-2-AW-DW-int(DW/8)-1-1:CMD_PACK_W-1-AW-DW-int(DW/8)-1-1-2]
        io.o_icb_cmd_burst <<= u_sirv_gnrl_cmd_fifo.io.o_dat[CMD_PACK_W-2-AW-DW-int(DW/8)-1-1-2:CMD_PACK_W-1-AW-DW-int(DW/8)-1-1-2-2]
        io.o_icb_cmd_beat <<= u_sirv_gnrl_cmd_fifo.io.o_dat[CMD_PACK_W-2-AW-DW-int(DW/8)-1-1-2-2:CMD_PACK_W-1-AW-DW-int(DW/8)-1-1-2-2-2]
        io.o_icb_cmd_usr <<= u_sirv_gnrl_cmd_fifo.io.o_dat[CMD_PACK_W-2-AW-DW-int(DW/8)-1-1-2-2-2:CMD_PACK_W-1-AW-DW-int(DW/8)-1-1-2-2-2-USR_W]

        # ///////////////////////////////////////////////////////////////////////////////////////////////

        # ///////////////////////////////////////////////////////////////////////////////////////////////
        # u_sirv_gnrl_rsp_fifo connect
        u_sirv_gnrl_rsp_fifo.io.i_vld <<= io.o_icb_rsp_valid
        io.o_icb_rsp_ready <<= u_sirv_gnrl_rsp_fifo.io.i_rdy
        u_sirv_gnrl_rsp_fifo.io.i_dat <<= CatBits(io.o_icb_rsp_err,
                                                  io.o_icb_rsp_excl_ok,
                                                  io.o_icb_rsp_rdata,
                                                  io.o_icb_rsp_usr)
        io.i_icb_rsp_valid <<= u_sirv_gnrl_rsp_fifo.io.o_vld
        u_sirv_gnrl_rsp_fifo.io.o_rdy <<= io.i_icb_rsp_ready
        io.i_icb_rsp_err <<= u_sirv_gnrl_rsp_fifo.io.o_dat[RSP_PACK_W-1]
        io.i_icb_rsp_excl_ok <<= u_sirv_gnrl_rsp_fifo.io.o_dat[RSP_PACK_W-2]
        io.i_icb_rsp_rdata <<= u_sirv_gnrl_rsp_fifo.io.o_dat[RSP_PACK_W-3:RSP_PACK_W-2-DW]
        io.i_icb_rsp_usr <<= u_sirv_gnrl_rsp_fifo.io.o_dat[RSP_PACK_W-3-DW:RSP_PACK_W-2-DW-USR_W]
        # ///////////////////////////////////////////////////////////////////////////////////////////////

        outs_cnt_inc = io.i_icb_cmd_valid & io.i_icb_cmd_ready
        outs_cnt_dec = io.i_icb_rsp_valid & io.i_icb_rsp_ready

        outs_cnt_ena = outs_cnt_inc ^ outs_cnt_dec

        outs_cnt_r = outs_cnt_dfflr.io.qout
        outs_cnt_nxt = Mux(outs_cnt_inc == U.w(1)(1), (outs_cnt_r + U.w(1)(1)), (outs_cnt_r - U.w(1)(1)))
        # ///////////////////////////////////////////////////////////////////////////////////////////////
        # outs_cnt_dfflr connect
        outs_cnt_dfflr.io.lden <<= outs_cnt_ena
        outs_cnt_dfflr.io.dnxt <<= outs_cnt_nxt
        # ///////////////////////////////////////////////////////////////////////////////////////////////

        ary = carray(U.w(1)(0), OUTS_CNT_W)
        io.icb_buffer_active <<= io.i_icb_cmd_valid | (~(outs_cnt_r == CatBits(*ary)))

    return SirvGnrlIcbBuffer()


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(sirv_gnrl_icb_buffer(1, 32, 32, 1, 1, 1, 1, 1)), "sirv_gnrl_icb_buffer.fir")
    Emitter.dumpVerilog(f)

