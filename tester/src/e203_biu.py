from .e203_defines import *
from .sirv_gnrl_icb_arbt import *
from .sirv_gnrl_icb_buffer import sirv_gnrl_icb_buffer
from .sirv_gnrl_icb_splt import sirv_gnrl_icb_splt
from pyhcl import *


class E203Biu(Module):
    io = IO(
        # clk=Input(U.w(1)),
        # rst_n=Input(U.w(1)),
        biu_active=Output(U.w(1)),
        
        # //////////////////////////////////////////////
        # The ICB Interface from LSU
        ## cmd
        lsu2biu_icb_cmd_valid=Input(U.w(1)),
        lsu2biu_icb_cmd_ready=Output(U.w(1)),
        lsu2biu_icb_cmd_addr=Input(U.w(E203_ADDR_SIZE)),
        lsu2biu_icb_cmd_read=Input(U.w(1)),
        lsu2biu_icb_cmd_wdata=Input(U.w(E203_XLEN)),
        lsu2biu_icb_cmd_wmask=Input(U.w(WMASK_SIZE)),
        lsu2biu_icb_cmd_burst=Input(U.w(2)),
        lsu2biu_icb_cmd_beat=Input(U.w(2)),
        lsu2biu_icb_cmd_lock=Input(U.w(1)),
        lsu2biu_icb_cmd_excl=Input(U.w(1)),
        lsu2biu_icb_cmd_size=Input(U.w(2)),
        ## rsp
        lsu2biu_icb_rsp_valid=Output(U.w(1)),
        lsu2biu_icb_rsp_ready=Input(U.w(1)),
        lsu2biu_icb_rsp_err=Output(U.w(1)),
        lsu2biu_icb_rsp_excl_ok=Output(U.w(1)),
        lsu2biu_icb_rsp_rdata=Output(U.w(E203_XLEN)),
        # //////////////////////////////////////////////

        # //////////////////////////////////////////////
        # the icb interface from ifetch
        ## bus cmd channel
        ifu2biu_icb_cmd_valid=Input(U.w(1)),
        ifu2biu_icb_cmd_ready=Output(U.w(1)),
        ifu2biu_icb_cmd_addr=Input(U.w(E203_ADDR_SIZE)),
        ifu2biu_icb_cmd_read=Input(U.w(1)),
        ifu2biu_icb_cmd_wdata=Input(U.w(E203_XLEN)),
        ifu2biu_icb_cmd_wmask=Input(U.w(WMASK_SIZE)),
        ifu2biu_icb_cmd_burst=Input(U.w(2)),
        ifu2biu_icb_cmd_beat=Input(U.w(2)),
        ifu2biu_icb_cmd_lock=Input(U.w(1)),
        ifu2biu_icb_cmd_excl=Input(U.w(1)),
        ifu2biu_icb_cmd_size=Input(U.w(2)),
        ## bus rsp channel
        ifu2biu_icb_rsp_valid=Output(U.w(1)),
        ifu2biu_icb_rsp_ready=Input(U.w(1)),
        ifu2biu_icb_rsp_err=Output(U.w(1)),
        ifu2biu_icb_rsp_excl_ok=Output(U.w(1)),
        ifu2biu_icb_rsp_rdata=Output(U.w(E203_XLEN)),
        # //////////////////////////////////////////////

        # //////////////////////////////////////////////
        # The ICB Interface to Private Peripheral Interface(PPI)
        ppi_region_indic=Input(U.w(E203_ADDR_SIZE)),
        ppi_icb_enable=Input(U.w(1)),
        ## Bus cmd channel
        ppi_icb_cmd_valid=Output(U.w(1)),
        ppi_icb_cmd_ready=Input(U.w(1)),
        ppi_icb_cmd_addr=Output(U.w(E203_ADDR_SIZE)), 
        ppi_icb_cmd_read=Output(U.w(1)), 
        ppi_icb_cmd_wdata=Output(U.w(E203_XLEN)),
        ppi_icb_cmd_wmask=Output(U.w(WMASK_SIZE)),
        ppi_icb_cmd_burst=Output(U.w(2)),
        ppi_icb_cmd_beat=Output(U.w(2)),
        ppi_icb_cmd_lock=Output(U.w(1)),
        ppi_icb_cmd_excl=Output(U.w(1)),
        ppi_icb_cmd_size=Output(U.w(2)),
        ## Bus RSP channel
        ppi_icb_rsp_valid=Input(U.w(1)),
        ppi_icb_rsp_ready=Output(U.w(1)),
        ppi_icb_rsp_err=Input(U.w(1)),
        ppi_icb_rsp_excl_ok=Input(U.w(1)),
        ppi_icb_rsp_rdata=Input(U.w(E203_XLEN)),
        # //////////////////////////////////////////////

        # //////////////////////////////////////////////
        # The ICB Interface to CLINT
        clint_region_indic=Input(U.w(E203_ADDR_SIZE)),
        clint_icb_enable=Input(U.w(1)),
        ## Bus cmd channel
        clint_icb_cmd_valid=Output(U.w(1)),
        clint_icb_cmd_ready=Input(U.w(1)),
        clint_icb_cmd_addr=Output(U.w(E203_ADDR_SIZE)),
        clint_icb_cmd_read=Output(U.w(1)),
        clint_icb_cmd_wdata=Output(U.w(E203_XLEN)),
        clint_icb_cmd_wmask=Output(U.w(WMASK_SIZE)),
        clint_icb_cmd_burst=Output(U.w(2)),
        clint_icb_cmd_beat=Output(U.w(2)),
        clint_icb_cmd_lock=Output(U.w(1)),
        clint_icb_cmd_excl=Output(U.w(1)),
        clint_icb_cmd_size=Output(U.w(2)),
        ## Bus RSP channel
        clint_icb_rsp_valid=Input(U.w(1)),
        clint_icb_rsp_ready=Output(U.w(1)),
        clint_icb_rsp_err=Input(U.w(1)),
        clint_icb_rsp_excl_ok=Input(U.w(1)),
        clint_icb_rsp_rdata=Input(U.w(E203_XLEN)),
        # //////////////////////////////////////////////

        # //////////////////////////////////////////////
        # The ICB Interface to PLIC
        plic_region_indic=Input(U.w(E203_ADDR_SIZE)),
        plic_icb_enable=Input(U.w(1)),
        ## Bus cmd channel
        plic_icb_cmd_valid=Output(U.w(1)),
        plic_icb_cmd_ready=Input(U.w(1)),
        plic_icb_cmd_addr=Output(U.w(E203_ADDR_SIZE)),
        plic_icb_cmd_read=Output(U.w(1)),
        plic_icb_cmd_wdata=Output(U.w(E203_XLEN)),
        plic_icb_cmd_wmask=Output(U.w(WMASK_SIZE)),
        plic_icb_cmd_burst=Output(U.w(2)),
        plic_icb_cmd_beat=Output(U.w(2)),
        plic_icb_cmd_lock=Output(U.w(1)),
        plic_icb_cmd_excl=Output(U.w(1)),
        plic_icb_cmd_size=Output(U.w(2)),
        ## Bus RSP channel
        plic_icb_rsp_valid=Input(U.w(1)),
        plic_icb_rsp_ready=Output(U.w(1)),
        plic_icb_rsp_err=Input(U.w(1)),
        plic_icb_rsp_excl_ok=Input(U.w(1)),
        plic_icb_rsp_rdata=Input(U.w(E203_XLEN)),
        # //////////////////////////////////////////////

        # //////////////////////////////////////////////
        # The ICB Interface to Fast I/O
        fio_region_indic=Input(U.w(E203_ADDR_SIZE)),
        fio_icb_enable=Input(U.w(1)),
        ## Bus cmd channel
        fio_icb_cmd_valid=Output(U.w(1)),
        fio_icb_cmd_ready=Input(U.w(1)),
        fio_icb_cmd_addr=Output(U.w(E203_ADDR_SIZE)),
        fio_icb_cmd_read=Output(U.w(1)),
        fio_icb_cmd_wdata=Output(U.w(E203_XLEN)),
        fio_icb_cmd_wmask=Output(U.w(WMASK_SIZE)),
        fio_icb_cmd_burst=Output(U.w(2)),
        fio_icb_cmd_beat=Output(U.w(2)),
        fio_icb_cmd_lock=Output(U.w(1)),
        fio_icb_cmd_excl=Output(U.w(1)),
        fio_icb_cmd_size=Output(U.w(2)),
        ## Bus RSP channel
        fio_icb_rsp_valid=Input(U.w(1)),
        fio_icb_rsp_ready=Output(U.w(1)),
        fio_icb_rsp_err=Input(U.w(1)),
        fio_icb_rsp_excl_ok=Input(U.w(1)),
        fio_icb_rsp_rdata=Input(U.w(E203_XLEN)),
        # //////////////////////////////////////////////

        # //////////////////////////////////////////////
        # The ICB Interface from Ifetch(mem)
        mem_icb_enable=Input(U.w(1)),
        ## Bus cmd channel
        mem_icb_cmd_valid=Output(U.w(1)),
        mem_icb_cmd_ready=Input(U.w(1)),
        mem_icb_cmd_addr=Output(U.w(E203_ADDR_SIZE)),
        mem_icb_cmd_read=Output(U.w(1)),
        mem_icb_cmd_wdata=Output(U.w(E203_XLEN)),
        mem_icb_cmd_wmask=Output(U.w(WMASK_SIZE)),
        mem_icb_cmd_burst=Output(U.w(2)),
        mem_icb_cmd_beat=Output(U.w(2)),
        mem_icb_cmd_lock=Output(U.w(1)),
        mem_icb_cmd_excl=Output(U.w(1)),
        mem_icb_cmd_size=Output(U.w(2)),
        ## Bus RSP channel
        mem_icb_rsp_valid=Input(U.w(1)),
        mem_icb_rsp_ready=Output(U.w(1)),
        mem_icb_rsp_err=Input(U.w(1)),
        mem_icb_rsp_excl_ok=Input(U.w(1)),
        mem_icb_rsp_rdata=Input(U.w(E203_XLEN))
        # //////////////////////////////////////////////


    )

    # Instantiate three submodules and their called parameters
    u_biu_icb_arbt = sirv_gnrl_icb_arbt(0, 0, 1, 1, 2, 1, 1, 32, 32)
    u_sirv_gnrl_icb_buffer = sirv_gnrl_icb_buffer(1, 32, 32, 1, 1, 1, 1, 1)
    u_biu_icb_splt = sirv_gnrl_icb_splt(0, 1, 1, 1, 6, 6, 1, 1, 32, 32, 0)

    #################################################################################
    # three submodules wire connect
    #################################################################################
    # (1)combine ifu and lsu to sirv_gnrl_icb_arbt
    # cmd channel
    # originally <<=, replaced by =
    u_biu_icb_arbt.io.i_bus_icb_cmd_valid <<= CatBits(io.ifu2biu_icb_cmd_valid, io.lsu2biu_icb_cmd_valid)
    u_biu_icb_arbt.io.i_bus_icb_cmd_addr  <<= CatBits(io.ifu2biu_icb_cmd_addr, io.lsu2biu_icb_cmd_addr)
    u_biu_icb_arbt.io.i_bus_icb_cmd_read  <<= CatBits(io.ifu2biu_icb_cmd_read, io.lsu2biu_icb_cmd_read)
    u_biu_icb_arbt.io.i_bus_icb_cmd_wdata <<= CatBits(io.ifu2biu_icb_cmd_wdata, io.lsu2biu_icb_cmd_wdata)
    u_biu_icb_arbt.io.i_bus_icb_cmd_wmask <<= CatBits(io.ifu2biu_icb_cmd_wmask, io.lsu2biu_icb_cmd_wmask)
    u_biu_icb_arbt.io.i_bus_icb_cmd_burst <<= CatBits(io.ifu2biu_icb_cmd_burst, io.lsu2biu_icb_cmd_burst)
    u_biu_icb_arbt.io.i_bus_icb_cmd_beat  <<= CatBits(io.ifu2biu_icb_cmd_beat, io.lsu2biu_icb_cmd_beat)
    u_biu_icb_arbt.io.i_bus_icb_cmd_lock  <<= CatBits(io.ifu2biu_icb_cmd_lock, io.lsu2biu_icb_cmd_lock)
    u_biu_icb_arbt.io.i_bus_icb_cmd_excl  <<= CatBits(io.ifu2biu_icb_cmd_excl, io.lsu2biu_icb_cmd_excl)
    u_biu_icb_arbt.io.i_bus_icb_cmd_size  <<= CatBits(io.ifu2biu_icb_cmd_size, io.lsu2biu_icb_cmd_size)

    ifu2biu_icb_cmd_ifu = U.w(1)(1)
    lsu2biu_icb_cmd_ifu = U.w(1)(0)
    # originally <<=, replaced by =
    u_biu_icb_arbt.io.i_bus_icb_cmd_usr <<= CatBits(ifu2biu_icb_cmd_ifu, lsu2biu_icb_cmd_ifu)
    # originally <<=, replaced by =
    io.ifu2biu_icb_cmd_ready <<= u_biu_icb_arbt.io.i_bus_icb_cmd_ready[1]
    io.lsu2biu_icb_cmd_ready <<= u_biu_icb_arbt.io.i_bus_icb_cmd_ready[0]

    # rsp channel
    # originally <<=, replaced by =
    io.ifu2biu_icb_rsp_valid   <<= u_biu_icb_arbt.io.i_bus_icb_rsp_valid[1]
    io.lsu2biu_icb_rsp_valid   <<= u_biu_icb_arbt.io.i_bus_icb_rsp_valid[0]
    io.ifu2biu_icb_rsp_err     <<= u_biu_icb_arbt.io.i_bus_icb_rsp_err[1]
    io.lsu2biu_icb_rsp_err     <<= u_biu_icb_arbt.io.i_bus_icb_rsp_err[0]
    io.ifu2biu_icb_rsp_excl_ok <<= u_biu_icb_arbt.io.i_bus_icb_rsp_excl_ok[1]
    io.lsu2biu_icb_rsp_excl_ok <<= u_biu_icb_arbt.io.i_bus_icb_rsp_excl_ok[0]
    io.ifu2biu_icb_rsp_rdata   <<= u_biu_icb_arbt.io.i_bus_icb_rsp_rdata[63:32]
    io.lsu2biu_icb_rsp_rdata   <<= u_biu_icb_arbt.io.i_bus_icb_rsp_rdata[31:0]
    # originally <<=, replaced by =
    u_biu_icb_arbt.io.i_bus_icb_rsp_ready  <<= CatBits(io.ifu2biu_icb_rsp_ready, io.lsu2biu_icb_rsp_ready)
    # u_biu_icb_arbt.io.i_bus_icb_rsp_usr is useless here!

    # (2) sirv_gnrl_icb_arbt <<==>> sirv_gnrl_icb_buffer
    # o <--> i cmd
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_valid <<= u_biu_icb_arbt.io.o_icb_cmd_valid
    u_biu_icb_arbt.io.o_icb_cmd_ready <<= u_sirv_gnrl_icb_buffer.io.i_icb_cmd_ready
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_read <<= u_biu_icb_arbt.io.o_icb_cmd_read
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_addr <<= u_biu_icb_arbt.io.o_icb_cmd_addr
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_wdata <<= u_biu_icb_arbt.io.o_icb_cmd_wdata
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_wmask <<= u_biu_icb_arbt.io.o_icb_cmd_wmask
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_burst <<= u_biu_icb_arbt.io.o_icb_cmd_burst
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_beat <<= u_biu_icb_arbt.io.o_icb_cmd_beat
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_excl <<= u_biu_icb_arbt.io.o_icb_cmd_excl
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_lock <<= u_biu_icb_arbt.io.o_icb_cmd_lock
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_size <<= u_biu_icb_arbt.io.o_icb_cmd_size
    u_sirv_gnrl_icb_buffer.io.i_icb_cmd_usr <<= u_biu_icb_arbt.io.o_icb_cmd_usr

    # o <--> i rsp
    u_biu_icb_arbt.io.o_icb_rsp_valid <<= u_sirv_gnrl_icb_buffer.io.i_icb_rsp_valid
    u_sirv_gnrl_icb_buffer.io.i_icb_rsp_ready <<= u_biu_icb_arbt.io.o_icb_rsp_ready
    u_biu_icb_arbt.io.o_icb_rsp_err <<= u_sirv_gnrl_icb_buffer.io.i_icb_rsp_err
    u_biu_icb_arbt.io.o_icb_rsp_excl_ok <<= u_sirv_gnrl_icb_buffer.io.i_icb_rsp_excl_ok
    u_biu_icb_arbt.io.o_icb_rsp_rdata <<= u_sirv_gnrl_icb_buffer.io.i_icb_rsp_rdata
    u_biu_icb_arbt.io.o_icb_rsp_usr <<= U.w(1)(0)

    # (3) sirv_gnrl_icb_buffer <<==>> sirv_gnrl_icb_splt
    buf_icb_cmd_ifu = u_sirv_gnrl_icb_buffer.io.o_icb_cmd_usr
    ### u_sirv_gnrl_icb_buffer.io.icb_buffer_active will be used in e203_biu.io.biu_active
    # o <--> i cmd
    u_biu_icb_splt.io.i_icb_cmd_valid <<= u_sirv_gnrl_icb_buffer.io.o_icb_cmd_valid
    u_sirv_gnrl_icb_buffer.io.o_icb_cmd_ready <<= u_biu_icb_splt.io.i_icb_cmd_ready
    u_biu_icb_splt.io.i_icb_cmd_read <<= u_sirv_gnrl_icb_buffer.io.o_icb_cmd_read
    u_biu_icb_splt.io.i_icb_cmd_addr <<= u_sirv_gnrl_icb_buffer.io.o_icb_cmd_addr
    u_biu_icb_splt.io.i_icb_cmd_wdata <<= u_sirv_gnrl_icb_buffer.io.o_icb_cmd_wdata
    u_biu_icb_splt.io.i_icb_cmd_wmask <<= u_sirv_gnrl_icb_buffer.io.o_icb_cmd_wmask
    u_biu_icb_splt.io.i_icb_cmd_lock <<= u_sirv_gnrl_icb_buffer.io.o_icb_cmd_lock
    u_biu_icb_splt.io.i_icb_cmd_excl <<= u_sirv_gnrl_icb_buffer.io.o_icb_cmd_excl
    u_biu_icb_splt.io.i_icb_cmd_size <<= u_sirv_gnrl_icb_buffer.io.o_icb_cmd_size
    u_biu_icb_splt.io.i_icb_cmd_burst <<= u_sirv_gnrl_icb_buffer.io.o_icb_cmd_burst
    u_biu_icb_splt.io.i_icb_cmd_beat <<= u_sirv_gnrl_icb_buffer.io.o_icb_cmd_beat
    u_biu_icb_splt.io.i_icb_cmd_usr <<= U.w(1)(0)
    ### u_sirv_gnrl_icb_buffer.io.o_icb_cmd_usr will be used in buf_icb_cmd_ifu = buf_icb_cmd_usr

    # o <--> i rsp
    u_sirv_gnrl_icb_buffer.io.o_icb_rsp_valid <<= u_biu_icb_splt.io.i_icb_rsp_valid
    u_biu_icb_splt.io.i_icb_rsp_ready <<= u_sirv_gnrl_icb_buffer.io.o_icb_rsp_ready
    u_sirv_gnrl_icb_buffer.io.o_icb_rsp_err <<= u_biu_icb_splt.io.i_icb_rsp_err
    u_sirv_gnrl_icb_buffer.io.o_icb_rsp_excl_ok <<= u_biu_icb_splt.io.i_icb_rsp_excl_ok
    u_sirv_gnrl_icb_buffer.io.o_icb_rsp_rdata <<= u_biu_icb_splt.io.i_icb_rsp_rdata
    u_sirv_gnrl_icb_buffer.io.o_icb_rsp_usr <<= U.w(1)(0)

    # (4) split sirv_gnrl_icb_splt into ppi, clint, plic, fio, mem
    # cmd channel
    # ifuerr_icb_cmd_valid is use for 0 Cycle response
    ifuerr_icb_cmd_valid = u_biu_icb_splt.io.o_bus_icb_cmd_valid[5]
    io.ppi_icb_cmd_valid <<= u_biu_icb_splt.io.o_bus_icb_cmd_valid[4]
    io.clint_icb_cmd_valid <<= u_biu_icb_splt.io.o_bus_icb_cmd_valid[3]
    io.plic_icb_cmd_valid <<= u_biu_icb_splt.io.o_bus_icb_cmd_valid[2]
    io.fio_icb_cmd_valid <<= u_biu_icb_splt.io.o_bus_icb_cmd_valid[1]
    io.mem_icb_cmd_valid <<= u_biu_icb_splt.io.o_bus_icb_cmd_valid[0]

    # ifuerr_icb_cmd_addr is useless???
    ifuerr_icb_cmd_addr = u_biu_icb_splt.io.o_bus_icb_cmd_addr[191:160]
    io.ppi_icb_cmd_addr <<= u_biu_icb_splt.io.o_bus_icb_cmd_addr[159:128]
    io.clint_icb_cmd_addr <<= u_biu_icb_splt.io.o_bus_icb_cmd_addr[127:96]
    io.plic_icb_cmd_addr <<= u_biu_icb_splt.io.o_bus_icb_cmd_addr[95:64]
    io.fio_icb_cmd_addr <<= u_biu_icb_splt.io.o_bus_icb_cmd_addr[63:32]
    io.mem_icb_cmd_addr <<= u_biu_icb_splt.io.o_bus_icb_cmd_addr[31:0]

    # ifuerr_icb_cmd_read is useless???
    ifuerr_icb_cmd_read = u_biu_icb_splt.io.o_bus_icb_cmd_read[5]
    io.ppi_icb_cmd_read <<= u_biu_icb_splt.io.o_bus_icb_cmd_read[4]
    io.clint_icb_cmd_read <<= u_biu_icb_splt.io.o_bus_icb_cmd_read[3]
    io.plic_icb_cmd_read <<= u_biu_icb_splt.io.o_bus_icb_cmd_read[2]
    io.fio_icb_cmd_read <<= u_biu_icb_splt.io.o_bus_icb_cmd_read[1]
    io.mem_icb_cmd_read <<= u_biu_icb_splt.io.o_bus_icb_cmd_read[0]

    # ifuerr_icb_cmd_wdata is useless???
    ifuerr_icb_cmd_wdata = u_biu_icb_splt.io.o_bus_icb_cmd_wdata[191:160]
    io.ppi_icb_cmd_wdata <<= u_biu_icb_splt.io.o_bus_icb_cmd_wdata[159:128]
    io.clint_icb_cmd_wdata <<= u_biu_icb_splt.io.o_bus_icb_cmd_wdata[127:96]
    io.plic_icb_cmd_wdata <<= u_biu_icb_splt.io.o_bus_icb_cmd_wdata[95:64]
    io.fio_icb_cmd_wdata <<= u_biu_icb_splt.io.o_bus_icb_cmd_wdata[63:32]
    io.mem_icb_cmd_wdata <<= u_biu_icb_splt.io.o_bus_icb_cmd_wdata[31:0]

    # ifuerr_icb_cmd_wmask is useless???
    ifuerr_icb_cmd_wmask = u_biu_icb_splt.io.o_bus_icb_cmd_wmask[23:20]
    io.ppi_icb_cmd_wmask <<= u_biu_icb_splt.io.o_bus_icb_cmd_wmask[19:16]
    io.clint_icb_cmd_wmask <<= u_biu_icb_splt.io.o_bus_icb_cmd_wmask[15:12]
    io.plic_icb_cmd_wmask <<= u_biu_icb_splt.io.o_bus_icb_cmd_wmask[11:8]
    io.fio_icb_cmd_wmask <<= u_biu_icb_splt.io.o_bus_icb_cmd_wmask[7:4]
    io.mem_icb_cmd_wmask <<= u_biu_icb_splt.io.o_bus_icb_cmd_wmask[3:0]

    # ifuerr_icb_cmd_burst is useless???
    ifuerr_icb_cmd_burst = u_biu_icb_splt.io.o_bus_icb_cmd_burst[11:10]
    io.ppi_icb_cmd_burst <<= u_biu_icb_splt.io.o_bus_icb_cmd_burst[9:8]
    io.clint_icb_cmd_burst <<= u_biu_icb_splt.io.o_bus_icb_cmd_burst[7:6]
    io.plic_icb_cmd_burst <<= u_biu_icb_splt.io.o_bus_icb_cmd_burst[5:4]
    io.fio_icb_cmd_burst <<= u_biu_icb_splt.io.o_bus_icb_cmd_burst[3:2]
    io.mem_icb_cmd_burst <<= u_biu_icb_splt.io.o_bus_icb_cmd_burst[1:0]

    # ifuerr_icb_cmd_beat is useless???
    ifuerr_icb_cmd_beat = u_biu_icb_splt.io.o_bus_icb_cmd_beat[11:10]
    io.ppi_icb_cmd_beat <<= u_biu_icb_splt.io.o_bus_icb_cmd_beat[9:8]
    io.clint_icb_cmd_beat <<= u_biu_icb_splt.io.o_bus_icb_cmd_beat[7:6]
    io.plic_icb_cmd_beat <<= u_biu_icb_splt.io.o_bus_icb_cmd_beat[5:4]
    io.fio_icb_cmd_beat <<= u_biu_icb_splt.io.o_bus_icb_cmd_beat[3:2]
    io.mem_icb_cmd_beat <<= u_biu_icb_splt.io.o_bus_icb_cmd_beat[1:0]

    # ifuerr_icb_cmd_lock is useless???
    ifuerr_icb_cmd_lock = u_biu_icb_splt.io.o_bus_icb_cmd_lock[5]
    io.ppi_icb_cmd_lock <<= u_biu_icb_splt.io.o_bus_icb_cmd_lock[4]
    io.clint_icb_cmd_lock <<= u_biu_icb_splt.io.o_bus_icb_cmd_lock[3]
    io.plic_icb_cmd_lock <<= u_biu_icb_splt.io.o_bus_icb_cmd_lock[2]
    io.fio_icb_cmd_lock <<= u_biu_icb_splt.io.o_bus_icb_cmd_lock[1]
    io.mem_icb_cmd_lock <<= u_biu_icb_splt.io.o_bus_icb_cmd_lock[0]

    # ifuerr_icb_cmd_excl is useless???
    ifuerr_icb_cmd_excl = u_biu_icb_splt.io.o_bus_icb_cmd_excl[5]
    io.ppi_icb_cmd_excl <<= u_biu_icb_splt.io.o_bus_icb_cmd_excl[4]
    io.clint_icb_cmd_excl <<= u_biu_icb_splt.io.o_bus_icb_cmd_excl[3]
    io.plic_icb_cmd_excl <<= u_biu_icb_splt.io.o_bus_icb_cmd_excl[2]
    io.fio_icb_cmd_excl <<= u_biu_icb_splt.io.o_bus_icb_cmd_excl[1]
    io.mem_icb_cmd_excl <<= u_biu_icb_splt.io.o_bus_icb_cmd_excl[0]

    # ifuerr_icb_cmd_size is useless???
    ifuerr_icb_cmd_size = u_biu_icb_splt.io.o_bus_icb_cmd_size[11:10]
    io.ppi_icb_cmd_size <<= u_biu_icb_splt.io.o_bus_icb_cmd_size[9:8]
    io.clint_icb_cmd_size <<= u_biu_icb_splt.io.o_bus_icb_cmd_size[7:6]
    io.plic_icb_cmd_size <<= u_biu_icb_splt.io.o_bus_icb_cmd_size[5:4]
    io.fio_icb_cmd_size <<= u_biu_icb_splt.io.o_bus_icb_cmd_size[3:2]
    io.mem_icb_cmd_size <<= u_biu_icb_splt.io.o_bus_icb_cmd_size[1:0]
    # u_biu_icb_splt.io.o_bus_icb_cmd_ready will be connected after rsp channel,
    # because it will use the signal ifuerr_icb_rsp_ready
    # (ifuerr_icb_cmd_ready = ifuerr_icb_rsp_ready;)

    # rsp channel
    # // 0 Cycle response
    ifuerr_icb_rsp_valid = ifuerr_icb_cmd_valid
    ifuerr_icb_rsp_err = U.w(1)(1)
    ifuerr_icb_rsp_excl_ok = U.w(1)(0)
    ifuerr_icb_rsp_rdata = U.w(32)(0)

    u_biu_icb_splt.io.o_bus_icb_rsp_valid <<= CatBits(ifuerr_icb_rsp_valid,
                                                      io.ppi_icb_rsp_valid,
                                                      io.clint_icb_rsp_valid,
                                                      io.plic_icb_rsp_valid,
                                                      io.fio_icb_rsp_valid,
                                                      io.mem_icb_rsp_valid)

    u_biu_icb_splt.io.o_bus_icb_rsp_err <<= CatBits(ifuerr_icb_rsp_err,
                                                    io.ppi_icb_rsp_err,
                                                    io.clint_icb_rsp_err,
                                                    io.plic_icb_rsp_err,
                                                    io.fio_icb_rsp_err,
                                                    io.mem_icb_rsp_err)

    u_biu_icb_splt.io.o_bus_icb_rsp_excl_ok <<= CatBits(ifuerr_icb_rsp_excl_ok,
                                                        io.ppi_icb_rsp_excl_ok,
                                                        io.clint_icb_rsp_excl_ok,
                                                        io.plic_icb_rsp_excl_ok,
                                                        io.fio_icb_rsp_excl_ok,
                                                        io.mem_icb_rsp_excl_ok)

    u_biu_icb_splt.io.o_bus_icb_rsp_rdata <<= CatBits(ifuerr_icb_rsp_rdata,
                                                      io.ppi_icb_rsp_rdata,
                                                      io.clint_icb_rsp_rdata,
                                                      io.plic_icb_rsp_rdata,
                                                      io.fio_icb_rsp_rdata,
                                                      io.mem_icb_rsp_rdata)

    u_biu_icb_splt.io.o_bus_icb_rsp_usr <<= U.w(6)(0)

    ifuerr_icb_rsp_ready = u_biu_icb_splt.io.o_bus_icb_rsp_ready[5]
    io.ppi_icb_rsp_ready <<= u_biu_icb_splt.io.o_bus_icb_rsp_ready[4]
    io.clint_icb_rsp_ready <<= u_biu_icb_splt.io.o_bus_icb_rsp_ready[3]
    io.plic_icb_rsp_ready <<= u_biu_icb_splt.io.o_bus_icb_rsp_ready[2]
    io.fio_icb_rsp_ready <<= u_biu_icb_splt.io.o_bus_icb_rsp_ready[1]
    io.mem_icb_rsp_ready <<= u_biu_icb_splt.io.o_bus_icb_rsp_ready[0]

    # u_biu_icb_splt.io.o_bus_icb_cmd_ready connect(It was originally a cmd channel)
    ifuerr_icb_cmd_ready = ifuerr_icb_rsp_ready
    u_biu_icb_splt.io.o_bus_icb_cmd_ready <<= CatBits(ifuerr_icb_cmd_ready,
                                                      io.ppi_icb_cmd_ready,
                                                      io.clint_icb_cmd_ready,
                                                      io.plic_icb_cmd_ready,
                                                      io.fio_icb_cmd_ready,
                                                      io.mem_icb_cmd_ready)

    # create io.biu_active and u_biu_icb_splt.io.buf_icb_splt_indic signals
    buf_icb_cmd_ppi = io.ppi_icb_enable & (u_sirv_gnrl_icb_buffer.io.o_icb_cmd_addr[31:28] == io.ppi_region_indic[31:28])
    buf_icb_sel_ppi = buf_icb_cmd_ppi & (~buf_icb_cmd_ifu)

    buf_icb_cmd_clint = io.clint_icb_enable & (u_sirv_gnrl_icb_buffer.io.o_icb_cmd_addr[31:16] == io.clint_region_indic[31:16])
    buf_icb_sel_clint = buf_icb_cmd_clint & (~buf_icb_cmd_ifu)

    buf_icb_cmd_plic = io.plic_icb_enable & (u_sirv_gnrl_icb_buffer.io.o_icb_cmd_addr[31:14] == io.plic_region_indic[31:14])
    buf_icb_sel_plic = buf_icb_cmd_plic & (~buf_icb_cmd_ifu)

    buf_icb_cmd_fio = io.fio_icb_enable & (u_sirv_gnrl_icb_buffer.io.o_icb_cmd_addr[31:28] == io.fio_region_indic[31:28])
    buf_icb_sel_fio = buf_icb_cmd_fio & (~buf_icb_cmd_ifu)

    buf_icb_sel_ifuerr = (buf_icb_cmd_ppi | buf_icb_cmd_clint | buf_icb_cmd_plic | buf_icb_cmd_fio) & buf_icb_cmd_ifu

    buf_icb_sel_mem = io.mem_icb_enable & (~buf_icb_sel_ifuerr) & (~buf_icb_sel_ppi) & (~buf_icb_sel_clint) & (~buf_icb_sel_plic) & (~buf_icb_sel_fio)

    u_biu_icb_splt.io.i_icb_splt_indic <<= CatBits(buf_icb_sel_ifuerr,
                                                   buf_icb_sel_ppi,
                                                   buf_icb_sel_clint,
                                                   buf_icb_sel_plic,
                                                   buf_icb_sel_fio,
                                                   buf_icb_sel_mem)

    io.biu_active <<= io.ifu2biu_icb_cmd_valid | io.lsu2biu_icb_cmd_valid | u_sirv_gnrl_icb_buffer.io.icb_buffer_active


if __name__ == '__main__':
    e203 = E203Biu()
    top = Emitter.emit(e203)
    f = Emitter.dump(top, "E203Biu.fir")
    Emitter.dumpVerilog(f)


