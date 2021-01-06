from .config import *


class AddrBuffer(Module):
    io = IO(
        addr_input=Input(U.w(WLEN)),
        flush=Input(U.w(1)),
        record=Input(U.w(1)), 
        front=Output(U.w(WLEN))
    )

    buffer = Mem(3, U.w(WLEN))
    counter = Mem(3, U.w(2))
    is_used = Mem(3, Bool)

    io.front <<= Mux(counter[U(0)] > counter[U(1)],
                     Mux(counter[U(0)] > counter[U(2)], buffer[U(0)], buffer[U(2)]),
                     Mux(counter[U(1)] > counter[U(2)], buffer[U(1)], buffer[U(2)]))

    write_index = Mux(is_used[U(0)] == U(0), Write_0, Mux(is_used[U(1)] == U(0), Write_1, Write_2))

    temp_used_list = []

    for i in range(0, 3):
        temp_used_list.append(Mux(io.record.to_bool(), Mux(write_index == U(i), U.w(1)(1), is_used[U(i)]),
                                  is_used[U(i)]))

    for i in range(0, 3):
        is_used[U(i)] <<= Mux(io.flush.to_bool(), U.w(1)(0), Mux(counter[U(i)] == U(2), U.w(1)(0), temp_used_list[i]))

    for i in range(0, 3):
        counter[U(i)] <<= Mux(io.flush.to_bool(), U(0), 
                              Mux(counter[U(i)] == U(2), U(0), 
                                  Mux(is_used[U(i)], counter[U(i)] + U(1), counter[U(i)])))

    for i in range(0, 3):
        buffer[U(i)] <<= Mux(io.flush.to_bool(), U(0),
                             Mux(counter[U(i)] == U(2), U(0),
                                 Mux(io.record.to_bool(),
                                     Mux(write_index == U(i), io.addr_input, buffer[U(i)]),
                                     buffer[U(i)])))


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(AddrBuffer()), "AddrBuffer.fir")
    Emitter.dumpVerilog(f)
