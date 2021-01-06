from .config import *


class DataCache(Module):
    io = IO(
        addr=Input(U.w(WLEN)),
        write_data=Input(U.w(WLEN)),
        Mem_Read=Input(U.w(MEM_READ_SIG_LEN)),
        Mem_Write=Input(U.w(MEM_WRITE_SIG_LEN)),
        Data_Size=Input(U.w(DATA_SIZE_SIG_LEN)),
        Load_Type=Input(U.w(LOAD_TYPE_SIG_LEN)),
        data_out=Output(U.w(WLEN))
    )

    cache = Mem(DATA_CACHE_LEN, U.w(WLEN))
    fix_addr = io.addr / U(4)

    write_data = LookUpTable(io.Data_Size, {
        Data_Size_W: io.write_data,
        Data_Size_H: CatBits(U.w(16)(0), io.write_data[15:0]),
        Data_Size_B: CatBits(U.w(24)(0), io.write_data[7:0]),
        ...: io.write_data
    })

    read_data = LookUpTable(CatBits(io.Data_Size, io.Load_Type), {
        Word_Unsigned: cache[fix_addr],
        HWord_Unsigned: cache[fix_addr][15:0],
        HWord_Signed: ((cache[fix_addr][15:0].to_sint() << U(16)) >> U(16)).to_uint(),
        Byte_Unsigned: cache[fix_addr][7:0],
        Byte_Signed: ((cache[fix_addr][7:0].to_sint() << U(24)) >> U(24)).to_uint(),
        ...: cache[fix_addr]
    })

    cache[fix_addr] <<= Mux(io.Mem_Write.to_bool(), write_data, cache[fix_addr])
    io.data_out <<= Mux(io.Mem_Read.to_bool(), read_data, U(0))


if __name__ == '__main__':
    f = Emitter.dump(Emitter.emit(DataCache()), "DataCache.fir")
    Emitter.dumpVerilog(f)