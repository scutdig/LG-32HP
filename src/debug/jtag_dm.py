"""
Filename:       jtag_dm.py
Author:         Ruohui Chen
Description:    Debug Module for RISC-V core, base on Debug Spec v1.0
"""

from pyhcl import *


# Parameters definition
DM_RESP_VALID       = U.w(1)(1)
DM_RESP_INVALID     = U.w(1)(0)
DTM_REQ_VALID       = U.w(1)(1)
DTM_REQ_INVALID     = U.w(1)(0)

DTM_OP_NOP          = U.w(2)(0)
DTM_OP_READ         = U.w(2)(1)
DTM_OP_WRITE        = U.w(2)(2)


def jtag_dm(DMI_ADDR_BITS=6, DMI_DATA_BITS=32, DMI_OP_BITS=2):
    DM_RESP_BITS = DMI_ADDR_BITS + DMI_DATA_BITS + DMI_OP_BITS
    DTM_REQ_BITS = DMI_ADDR_BITS + DMI_DATA_BITS + DMI_OP_BITS
    SHIFT_REG_BITS = DTM_REQ_BITS

    dmr_addr = {
        'DCSR':         U.w(16)(0x7b0),
        'DMSTATUS':     U.w(6)(0x11),
        'DMCONTROL':    U.w(6)(0x10),
        'HARTINFO':     U.w(6)(0x12),
        'ABSTRACTCS':   U.w(6)(0x16),
        'DATA0':        U.w(6)(0x04),
        'SBCS':         U.w(6)(0x38),
        'SBADDRESS0':   U.w(6)(0x39),
        'SBDATA0':      U.w(6)(0x3C),
        'COMMAND':      U.w(6)(0x17),
        'DPC':          U.w(16)(0x7b1),
    }

    OP_SUCC = U.w(2)(0)

    class JTAG_DM(Module):
        io = IO(
            dm_ack_o=Output(Bool),
            dtm_req_valid_i=Input(Bool),
            dtm_req_data_i=Input(U.w(DTM_REQ_BITS)),
            dtm_ack_i=Input(Bool),
            dm_resp_data_o=Output(U.w(DM_RESP_BITS)),
            dm_resp_valid_o=Output(Bool),
            dm_reg_we_o=Output(Bool),
            dm_reg_addr_o=Output(U.w(5)),
            dm_reg_wdata_o=Output(U.w(32)),
            dm_reg_rdata_i=Input(U.w(32)),
            dm_mem_we_o=Output(Bool),
            dm_mem_addr_o=Output(U.w(32)),
            dm_mem_wdata_o=Output(U.w(32)),
            dm_mem_rdata_i=Input(U.w(32)),
            dm_op_req_o=Output(Bool),
            dm_halt_req_o=Output(Bool),
            dm_reset_req_o=Output(Bool)
        )

        # Registers for DM
        sbaddress0 = RegInit(U.w(32)(0))
        dcsr       = RegInit(U.w(32)(0))
        hartinfo   = RegInit(U.w(32)(0))
        sbcs       = RegInit(U.w(32)(0x20040404))
        dmcontrol  = RegInit(U.w(32)(0))
        abstractcs = RegInit(U.w(32)(0x1000003))
        data0      = RegInit(U.w(32)(0))
        sbdata0    = RegInit(U.w(32)(0))
        command    = RegInit(U.w(32)(0))
        dmstatus   = RegInit(U.w(32)(0x430c82))

        read_data       = RegInit(U.w(32)(0))
        dm_reg_we       = RegInit(Bool(False))
        dm_reg_addr     = RegInit(U.w(5)(0))
        dm_reg_wdata    = RegInit(U.w(32)(0))
        dm_mem_we       = RegInit(Bool(False))
        dm_mem_addr     = RegInit(U.w(32)(0))
        dm_mem_wdata    = RegInit(U.w(32)(0))
        dm_halt_req     = RegInit(Bool(False))
        dm_reset_req    = RegInit(Bool(False))
        need_resp       = RegInit(Bool(False))
        is_read_reg     = RegInit(Bool(False))
        rx_valid        = Wire(Bool)
        rx_data         = Wire(U.w(DTM_REQ_BITS))

        sbaddress0_next = Wire(U.w(32))
        dm_resp_data    = Wire(U.w(DM_RESP_BITS))
        sbaddress0_next <<= sbaddress0 + U(4)

        op              = Wire(U.w(DMI_OP_BITS))
        data            = Wire(U.w(DMI_DATA_BITS))
        address         = Wire(U.w(DMI_ADDR_BITS))
        op <<= rx_data[DMI_OP_BITS-1:0]
        data <<= rx_data[DMI_DATA_BITS+DMI_OP_BITS-1:DMI_OP_BITS]
        address <<= rx_data[DTM_REQ_BITS-1:DMI_DATA_BITS+DMI_OP_BITS]

        read_dmstatus   = Wire(Bool)
        read_dmstatus <<= (op == DTM_OP_READ) & (address == dmr_addr['DMSTATUS'])

        with when(rx_valid):
            need_resp <<= Bool(True)
            with when(op == DTM_OP_READ):
                with when(address == dmr_addr['DMSTATUS']):
                    read_data <<= dmstatus
                with elsewhen(address == dmr_addr['DMCONTROL']):
                    read_data <<= dmcontrol
                with elsewhen(address == dmr_addr['HARTINFO']):
                    read_data <<= hartinfo
                with elsewhen(address == dmr_addr['SBCS']):
                    read_data <<= sbcs
                with elsewhen(address == dmr_addr['ABSTRACTCS']):
                    read_data <<= abstractcs
                with elsewhen(address == dmr_addr['DATA0']):
                    with when(is_read_reg):
                        read_data <<= io.dm_reg_rdata_i
                    with otherwise():
                        read_data <<= data0
                    is_read_reg <<= Bool(False)
                with elsewhen(address == dmr_addr['SBDATA0']):
                    read_data <<= io.dm_mem_rdata_i
                    with when(sbcs[16] == U.w(1)(1)):
                        sbaddress0 <<= sbaddress0_next
                    with when(sbcs[15] == U.w(1)(1)):
                        dm_mem_addr <<= sbaddress0_next
                with otherwise():
                    read_data <<= U.w(DMI_DATA_BITS)(0)
            with elsewhen(op == DTM_OP_WRITE):
                pass

    return JTAG_DM()
