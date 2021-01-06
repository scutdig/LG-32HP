from pyhcl import *


def sirv_gnrl_dffl(DW: int = 32):
    print("sirv_gnrl_dffl: DW = ", DW)

    class SirvGnrlDffl(Module):
        # # /////////////////////////////////////////
        # DW   = 32
        # # /////////////////////////////////////////
        io = IO(
            # clk=Input(U.w(1)),

            # how to remove the default input of reset??? or give U.w(1)(0) to reset?
            # rst_n=Input(U.w(1)),
            lden=Input(U.w(1)),
            dnxt=Input(U.w(DW)),
            qout=Output(U.w(DW))
        )

        qout_r = Reg(U.w(DW))
        qout_r <<= Mux(io.lden.to_bool(), io.dnxt, qout_r)
        io.qout <<= qout_r

        # dnxt_vec = Wire(Vec(DW, U.w(1)))
        #
        # io.qout <<= CatVecH2L(dnxt_vec)
        # #if io.lden == U(1):
        # for i in range(0, DW):
        #     dnxt_vec[i] <<= (io.lden == io.dnxt[i])

    return SirvGnrlDffl()


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(sirv_gnrl_dffl(32)), "sirv_gnrl_dffl.fir")
    Emitter.dumpVerilog(f)





