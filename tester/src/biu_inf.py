from .config import *
from .e203_defines import *


def biu_inf():
    write_biu_addr = 0x101
    read_biu_addr = 0x100

    class BIUInterface(Module):
        io = IO(
            Mem_Write=Input(U.w(MEM_WRITE_SIG_LEN)),
            addr=Input(U.w(WLEN)),
            write_data=Input(U.w(WLEN)),

            # To Data cache
            DC_Mem_Write=Output(U.w(MEM_WRITE_SIG_LEN)),
            DC_addr=Output(U.w(WLEN)),
            DC_write_data=Output(U.w(WLEN)),

            # To BIU
            biu_addr=Output(U.w(WLEN)),
            biu_write_data=Output(U.w(WLEN)),
            biu_cmd_valid=Output(U.w(1)),
            biu_cmd_read=Output(U.w(1)),
            biu_cmd_wmask=Output(U.w(WMASK_SIZE)),
            biu_cmd_burst=Output(U.w(2)),
            biu_cmd_beat=Output(U.w(2)),
            biu_cmd_lock=Output(U.w(2)),
            biu_cmd_excl=Output(U.w(1)),
            biu_cmd_size=Output(U.w(2)),
            biu_rsp_ready=Output(U.w(1)),

            ppi_cmd_ready=Output(U.w(1)),
            ppi_rsp_valid=Output(U.w(1)),
            ppi_rsp_err=Output(U.w(1)),
            ppi_rsp_excl_ok=Output(U.w(1)),
            ppi_rsp_rdata=Output(U.w(E203_XLEN))
        )

        biu_data = RegInit(U.w(WLEN)(0))
        biu_addr = RegInit(U.w(WLEN)(0))
        write_counter = RegInit(U.w(1)(0))

        biu_interact = ((io.addr == U(write_biu_addr)) | (io.addr == U(read_biu_addr))) & io.Mem_Write

        io.DC_Mem_Write <<= Mux(biu_interact, U(0), io.Mem_Write)
        io.DC_addr <<= Mux(biu_interact, U(0), io.addr)
        io.DC_write_data <<= Mux(biu_interact, U(0), io.write_data)

        biu_data <<= Mux(biu_interact, io.write_data, biu_data)

        # To BIU
        io.biu_cmd_wmask <<= U(0)
        io.biu_cmd_burst <<= U(0)
        io.biu_cmd_beat <<= U(0)
        io.biu_cmd_lock <<= U(0)
        io.biu_cmd_excl <<= U(0)
        io.biu_cmd_size <<= U(0)

        with when((io.addr == U(read_biu_addr)) & biu_interact):
            # Read BIU
            io.biu_addr <<= io.write_data
            io.biu_write_data <<= U(0)
            io.biu_cmd_valid <<= U(1)
            io.biu_cmd_read <<= U(1)
            io.biu_rsp_ready <<= U(1)

            io.ppi_cmd_ready <<= U(1)
            io.ppi_rsp_valid <<= U(1)
            io.ppi_rsp_err <<= U(0)
            io.ppi_rsp_excl_ok <<= U(1)
            io.ppi_rsp_rdata <<= U(40)
        with elsewhen((io.addr == U(write_biu_addr)) & biu_interact):
            # Write BIU
            io.biu_cmd_read <<= U(0)

            io.ppi_cmd_ready <<= U(0)
            io.ppi_rsp_valid <<= U(0)
            io.ppi_rsp_err <<= U(0)
            io.ppi_rsp_excl_ok <<= U(0)
            io.ppi_rsp_rdata <<= U(0)
            with when(write_counter == U(0)):
                write_counter <<= write_counter + U(1)
                io.biu_addr <<= U(0)
                io.biu_write_data <<= U(0)
                io.biu_cmd_valid <<= U(0)
                io.biu_rsp_ready <<= U(0)
            with otherwise():
                write_counter <<= U(0)
                io.biu_addr <<= biu_data
                io.biu_write_data <<= io.write_data
                io.biu_cmd_valid <<= U(1)
                io.biu_rsp_ready <<= U(1)
        with otherwise():
            io.biu_addr <<= U(0)
            io.biu_write_data <<= U(0)
            io.biu_cmd_valid <<= U(0)
            io.biu_cmd_read <<= U(0)
            io.biu_rsp_ready <<= U(0)

            io.ppi_cmd_ready <<= U(0)
            io.ppi_rsp_valid <<= U(0)
            io.ppi_rsp_err <<= U(0)
            io.ppi_rsp_excl_ok <<= U(0)
            io.ppi_rsp_rdata <<= U(0)

    return BIUInterface()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(biu_inf()), "BIUInterface.fir"))
