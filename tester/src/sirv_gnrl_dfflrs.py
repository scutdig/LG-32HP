from pyhcl import *


def sirv_gnrl_dfflrs(DW: int = 32):

    class SirvGnrlDfflrs(Module):
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

        qout_r = RegInit(U.w(DW)(2**DW-1))
        qout_r <<= Mux(io.lden.to_bool(), io.dnxt, qout_r)
        io.qout <<= qout_r

    return SirvGnrlDfflrs()


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(sirv_gnrl_dfflrs(32)), "sirv_gnrl_dfflrs.fir")
    Emitter.dumpVerilog(f)


