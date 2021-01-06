from pyhcl import *


def sirv_gnrl_dfflr(DW: int = 32):

    class SirvGnrlDfflr(Module):
        # # /////////////////////////////////////////
        # DW   = 32
        # # /////////////////////////////////////////
        io = IO(
            # clk=Input(U.w(1)),
            # rst_n=Input(U.w(1)),
            lden=Input(U.w(1)),
            dnxt=Input(U.w(DW)),
            qout=Output(U.w(DW))
        )

        qout_r = RegInit(U.w(DW)(0))
        qout_r <<= Mux(io.lden.to_bool(), io.dnxt, qout_r)
        io.qout <<= qout_r

    return SirvGnrlDfflr()


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(sirv_gnrl_dfflr(32)), "sirv_gnrl_dfflr.fir")
    Emitter.dumpVerilog(f)


