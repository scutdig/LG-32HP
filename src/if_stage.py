from pyhcl import *


def if_stage(PULP_XPULP=0, PULP_OBI=0, PULP_SCORE=0, FPU=0):
    class IF_STAGE(Module):
        pass

    return IF_STAGE()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(if_stage()), "if_stage.fir"))
