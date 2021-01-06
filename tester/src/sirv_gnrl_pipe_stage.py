from pyhcl import *
from .sirv_gnrl_dffl import sirv_gnrl_dffl
from .sirv_gnrl_dfflr import sirv_gnrl_dfflr


def sirv_gnrl_pipe_stage(CUT_READY: int = 0,
                         DP: int = 1,
                         DW: int = 32):

    class SirvGnrlPipeStage(Module):

        # # /////////////////////////////////////////
        # # default parameters
        # CUT_READY = 0
        # DP = 1
        # DW = 32
        # # /////////////////////////////////////////

        io = IO(

            # clk=Input(U.w(1)),
            # rst_n=Input(U.w(1)),
            i_vld=Input(U.w(1)),
            i_rdy=Output(U.w(1)),
            i_dat=Input(U.w(DW)),
            o_vld=Output(U.w(1)),
            o_rdy=Input(U.w(1)),
            o_dat=Output(U.w(DW))
        )

        if DP == 0:
            io.o_vld <<= io.i_vld
            io.i_rdy <<= io.o_rdy
            io.o_dat <<= io.i_dat
        else:
            vld_dfflr = sirv_gnrl_dfflr(1)
            dat_dfflr = sirv_gnrl_dffl(DW)

            vld_set = io.i_vld & io.i_rdy
            vld_clr = io.o_vld & io.o_rdy

            vld_ena = vld_set | vld_clr
            vld_nxt = vld_set | (~vld_clr)

            # vld_dfflr assignment
            vld_dfflr.io.lden <<= vld_ena
            vld_dfflr.io.dnxt <<= vld_nxt
            vld_r = vld_dfflr.io.qout

            io.o_vld <<= vld_r

            # dat_dfflr assignment
            dat_dfflr.io.lden <<= vld_set
            dat_dfflr.io.dnxt <<= io.i_dat
            io.o_dat <<= dat_dfflr.io.qout

            if CUT_READY == 1:
                io.i_rdy <<= (~vld_r)
            else:
                io.i_rdy <<= (~vld_r) | vld_clr

    return SirvGnrlPipeStage()


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(sirv_gnrl_pipe_stage(1, 1, 32)), "sirv_gnrl_pipe_stage.fir")
    Emitter.dumpVerilog(f)

