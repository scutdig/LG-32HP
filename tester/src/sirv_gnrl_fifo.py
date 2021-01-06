from pyhcl import *
from .sirv_gnrl_dffl import sirv_gnrl_dffl
from .sirv_gnrl_dfflr import sirv_gnrl_dfflr
from .sirv_gnrl_dfflrs import sirv_gnrl_dfflrs


def carray(el, len):
    ary = []
    for i in range(len):
        ary.append(el)
    return ary


def sirv_gnrl_fifo(CUT_READY: int = 0,
                   MSKO: int = 0,
                   DP: int = 8,
                   DW: int = 32):
    print("sirv_gnrl_fifo: DP = ", DP)
    class SirvGnrlFifo(Module):

        # # /////////////////////////////////////////
        # # default parameters
        # CUT_READY = 0
        # MSKO = 0
        # DP   = 8
        # DW   = 32
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

        # //////////////////////////////////////////////////////////////////
        # # Intermediate variables' definition
        #
        rptr_vec_nxt   = Wire(U.w(DP))
        rptr_vec_r     = Wire(U.w(DP))
        rptr_vec_r_vec = Wire(Vec(DP, U.w(1)))
        wptr_vec_nxt   = Wire(U.w(DP))
        wptr_vec_r     = Wire(U.w(DP))
        wptr_vec_r_vec = Wire(Vec(DP, U.w(1)))

        i_vec = Wire(U.w(DP+1))
        o_vec = Wire(U.w(DP+1))
        vec_nxt = Wire(U.w(DP+1))
        vec_r = Wire(U.w(DP+1))
        vec_r_vec = Wire(Vec(DP+1, U.w(1)))

        fifo_rf_r = Wire(Vec(DP, U.w(DW)))
        fifo_rf_en = Wire(Vec(DP, U.w(1)))

        # //////////////////////////////////////////////////////////////////

        if DP == 0:
            io.o_vld <<= io.i_vld
            io.i_rdy <<= io.o_rdy
            io.o_dat <<= io.i_dat
        else:
            # //////////////////////////////////////////////////////////////////
            # Instantiate two submodules and their called parameters
            #
            rptr_vec_0_dfflrs = sirv_gnrl_dfflrs(1)
            wptr_vec_0_dfflrs = sirv_gnrl_dfflrs(1)

            if DP > 1:
                rptr_vec_31_dfflr = sirv_gnrl_dfflr(DP-1)
                wptr_vec_31_dfflr = sirv_gnrl_dfflr(DP-1)

            vec_0_dfflrs = sirv_gnrl_dfflrs(1)
            vec_31_dfflr = sirv_gnrl_dfflr(DP)

            fifo_rf_dffl = [sirv_gnrl_dffl(DW).io for _ in range(0, DP)]

            # //////////////////////////////////////////////////////////////////

            # //////////////////////////////////////////////////////////////////
            # change VEC to Wire
            # (1) rptr_vec_r
            rptr_vec_r_vec[0] <<= rptr_vec_0_dfflrs.io.qout
            if DP > 1:
                for i in range(1, DP):
                    rptr_vec_r_vec[i] <<= rptr_vec_31_dfflr.io.qout[i-1]
            rptr_vec_r <<= CatVecH2L(rptr_vec_r_vec)

            # (2) wptr_vec_r
            wptr_vec_r_vec[0] <<= wptr_vec_0_dfflrs.io.qout
            if DP > 1:
                for i in range(1, DP):
                    wptr_vec_r_vec[i] <<= wptr_vec_31_dfflr.io.qout[i-1]
            wptr_vec_r <<= CatVecH2L(wptr_vec_r_vec)

            # (3) vec_r
            vec_r_vec[0] <<= vec_0_dfflrs.io.qout
            for i in range(1, DP+1):
                vec_r_vec[i] <<= vec_31_dfflr.io.qout[i-1]
            vec_r <<= CatVecH2L(vec_r_vec)
            # //////////////////////////////////////////////////////////////////

            wen = io.i_vld & io.i_rdy
            ren = io.o_vld & io.o_rdy

            if DP == 1:
                rptr_vec_nxt <<= U.w(DP)(1)
            else:
                ary0 = carray(U.w(1)(0), DP-1)
                rptr_vec_nxt <<= Mux(rptr_vec_r[DP-1] == U.w(1)(1), CatBits(*ary0, U.w(1)(1)), (rptr_vec_r << U(1)))
            if DP == 1:
                wptr_vec_nxt <<= U.w(DP)(1)
            else:
                ary1 = carray(U.w(1)(0), DP-1)
                wptr_vec_nxt <<= Mux(wptr_vec_r[DP-1] == U.w(1)(1), CatBits(*ary1, U.w(1)(1)), (wptr_vec_r << U(1)))

            # rptr_vec_0_dfflrs connect
            rptr_vec_0_dfflrs.io.lden <<= ren
            rptr_vec_0_dfflrs.io.dnxt <<= rptr_vec_nxt[0]
            # rptr_vec_r_vec[0] <<= rptr_vec_0_dfflrs.io.qout

            # wptr_vec_0_dfflrs connect
            wptr_vec_0_dfflrs.io.lden <<= wen
            wptr_vec_0_dfflrs.io.dnxt <<= wptr_vec_nxt[0]
            # wptr_vec_r_vec[0] <<= wptr_vec_0_dfflrs.io.qout

            if DP > 1:
                # rptr_vec_31_dfflr connect
                rptr_vec_31_dfflr.io.lden <<= ren
                rptr_vec_31_dfflr.io.dnxt <<= rptr_vec_nxt[DP-1:1]
                # for i in range(1, DP):
                #     rptr_vec_r_vec[i] <<= rptr_vec_31_dfflr.io.qout[i-1]

                # wptr_vec_31_dfflr connect
                wptr_vec_31_dfflr.io.lden <<= wen
                wptr_vec_31_dfflr.io.dnxt <<= wptr_vec_nxt[DP-1:1]
                # for i in range(1, DP):
                #     wptr_vec_r_vec[i] <<= wptr_vec_31_dfflr.io.qout[i-1]


            # next part
            vec_en = ren ^ wen
            vec_nxt <<= Mux(wen == U.w(1)(1), CatBits(vec_r[DP-1:0], U.w(1)(1)), (vec_r >> U(1)))

            # vec_0_dfflrs connect
            vec_0_dfflrs.io.lden <<= vec_en
            vec_0_dfflrs.io.dnxt <<= vec_nxt[0]

            # vec_31_dfflr connect
            vec_31_dfflr.io.lden <<= vec_en
            vec_31_dfflr.io.dnxt <<= vec_nxt[DP:1]

            i_vec <<= CatBits(U.w(1)(0), vec_r[DP:1])
            o_vec <<= CatBits(U.w(1)(0), vec_r[DP:1])

            if DP == 1:
                if CUT_READY == 1:
                    io.i_rdy <<= (~i_vec[DP-1])
                else:
                    io.i_rdy <<= (~i_vec[DP-1]) | ren
            else:
                io.i_rdy <<= (~i_vec[DP-1])

            for i in range(0, DP):
                fifo_rf_en[i] <<= wen & wptr_vec_r[i]

                fifo_rf_dffl[i].lden <<= fifo_rf_en[i]
                fifo_rf_dffl[i].dnxt <<= io.i_dat
                fifo_rf_r[i] <<= fifo_rf_dffl[i].qout

            ary2 = carray(U.w(1)(0), DW)
            for j in range(0, DP):
                ary3 = carray(rptr_vec_r[j], DW)
                mux_rdat = CatBits(*ary2) | (CatBits(*ary3) & fifo_rf_r[j])

            if MSKO == 1:
                ary4 = carray(io.o_vld, DW)
                io.o_dat <<= CatBits(*ary4) & mux_rdat
            else:
                io.o_dat <<= mux_rdat

            io.o_vld <<= (o_vec[0])

    return SirvGnrlFifo()

# DW = (1+AW+DW+(DW/8)+1+1+2+2+2+USR_W) = 1+32+32+4+1+1+2+2+2+1=78


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(sirv_gnrl_fifo(1, 0, 1, 78)), "sirv_gnrl_fifo.fir")
    Emitter.dumpVerilog(f)


