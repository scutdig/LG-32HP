from .config import *


class InstCache(Module):
    io = IO(
        addr=Input(U.w(WLEN)),
        inst=Output(U.w(WLEN))
    )

    cache = Mem(INSTCACHE_SIZE, U.w(BLEN))
    io.inst <<= CatBits(cache[io.addr], cache[io.addr + U(1)],
                        cache[io.addr + U(2)], cache[io.addr + U(3)])


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(InstCache()), "InstCache.fir")
    Emitter.dumpVerilog(f)
