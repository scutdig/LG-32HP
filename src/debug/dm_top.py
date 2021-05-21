"""
Copyright Digisim, Computer Architecture team of South China University of Technology,

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
   Author Name: Ruohui Chen
   Date: 2021-05-20
   File Name: dm_top.py
   Description: Top-level of debug module (DM). This is an AXI-Slave.
                DTM protocol is equal to SiFives debug protocol to leverage
                SW infrastructure re-use. As of version 0.13.
"""
from pyhcl import *
from src.debug.dm_pkg import *
from src.debug.dm_csrs import *
from src.debug.dm_sba import *
from src.debug.dm_mem import *


def dm_top(NrHarts: int = 1, BusWidth: int = 32):
    # local parameters
    DmBaseAddress = U(0x1000)   # default to non-zero page
    # Bitmask to select physically available harts for systems
    # that don't use hart numbers in a contiguous fashion.
    SelectableHarts = CatBits(*[U.w(1)(1) for _ in range(NrHarts)])
    ReadByteEnable = 1

    class DM_TOP(Module):
        io = IO(
            testmode_i=Input(Bool),
            ndmreset_o=Output(Bool),            # non-debug module reset
            dmactive_o=Output(Bool),            # debug module is active
            debug_req_o=Output(U.w(NrHarts)),   # async debug request
            unavailable_i=Input(U.w(NrHarts)),  # communicate whether the hart is unavailable (e.g.: power down)
            hartinfo_i=Input(Vec(NrHarts, U.w(32))),

            slave_req_i=Input(Bool),
            slave_we_i=Input(Bool),
            slave_addr_i=Input(U.w(BusWidth)),
            slave_be_i=Input(U.w(int(BusWidth/8))),
            slave_wdata_i=Input(U.w(BusWidth)),
            slave_rdata_o=Output(U.w(BusWidth)),

            master_req_o=Output(Bool),
            master_add_o=Output(U.w(BusWidth)),
            master_we_o=Output(Bool),
            master_wdata_o=Output(U.w(BusWidth)),
            master_be_o=Output(U.w(int(BusWidth/8))),
            master_gnt_i=Input(Bool),
            master_r_valid_i=Input(Bool),
            master_r_rdata_i=Input(U.w(BusWidth)),

            # Connection to DTM - compatible to RocketChip Debug Module
            dmi_rst_ni=Input(Bool),
            dmi_req_valid_i=Input(Bool),
            dmi_req_ready_o=Output(Bool),
            dmi_req_i=Input(U.w(41)),

            dmi_resp_valid_o=Output(Bool),
            dmi_resp_ready_i=Input(Bool),
            dmi_resp_o=Output(U.w(34))
        )
        dm_csrs_i = dm_csrs().io
        dm_sba_i = dm_sba().io
        dm_mem_i = dm_mem().io

        hartinfo_i = hartinfo_t()
        dmi_req_i = dmi_req_t()
        dmi_resp_o = dmi_resp_t()
        hartinfo_i.packed <<= io.hartinfo_i[0]
        dmi_req_i.packed <<= io.dmi_req_i

        halted = Wire(U.w(NrHarts))
        resumeack = Wire(U.w(NrHarts))
        haltreq = Wire(U.w(NrHarts))
        resumereq = Wire(U.w(NrHarts))
        clear_resumeack = Wire(Bool)
        cmd_valid = Wire(Bool)
        cmd = command_t(False)

        cmderror_valid = Wire(Bool)
        cmderror = Wire(U.w(CMDERR_E_WIDTH))
        cmdbusy = Wire(Bool)
        progbuf = Wire(Vec(ProgBufSize, U.w(32)))
        data_csrs_mem = Wire(Vec(DataCount, U.w(32)))
        data_mem_csrs = Wire(Vec(DataCount, U.w(32)))
        data_valid = Wire(Bool)
        hartsel = Wire(U.w(20))

        # System Bus Access Module
        sbaddress_csrs_sba = Wire(U.w(BusWidth))
        sbaddress_sba_csrs = Wire(U.w(BusWidth))
        sbaddress_write_valid = Wire(Bool)
        sbreadonaddr = Wire(Bool)
        sbautoincrement = Wire(Bool)
        # logic [2:0]                       sbaccess;
        sbaccess = Wire(U.w(3))
        sbreadondata = Wire(Bool)
        # logic [BusWidth-1:0]              sbdata_write;
        sbdata_write = Wire(U.w(BusWidth))
        sbdata_read_valid = Wire(Bool)
        sbdata_write_valid = Wire(Bool)
        # logic [BusWidth-1:0]              sbdata_read;
        sbdata_read = Wire(U.w(BusWidth))
        sbdata_valid = Wire(Bool)
        sbbusy = Wire(Bool)
        sberror_valid = Wire(Bool)
        # logic [2:0]                       sberror;
        sberror = Wire(U.w(3))

        # -----------------------
        # dm_csrs
        # -----------------------
        io.dmactive_o <<= dm_csrs_i.dmactive_o
        dm_csrs_i.testmode_i <<= io.testmode_i
        dm_csrs_i.dmi_rst_ni <<= io.dmi_rst_ni
        dm_csrs_i.dmi_req_valid_i <<= io.dmi_req_valid_i
        io.dmi_req_ready_o <<= dm_csrs_i.dmi_req_ready_o
        dm_csrs_i.dmi_req_i_addr <<= dmi_req_i.addr
        dm_csrs_i.dmi_req_i_op <<= dmi_req_i.op
        dm_csrs_i.dmi_req_i_data <<= dmi_req_i.ddata
        io.dmi_resp_valid_o <<= dm_csrs_i.dmi_resp_valid_o
        dm_csrs_i.dmi_resp_ready_i <<= io.dmi_resp_ready_i
        dmi_resp_o.ddata <<= dm_csrs_i.dmi_resp_o_data
        dmi_resp_o.resp <<= dm_csrs_i.dmi_resp_o_resp
        io.ndmreset_o <<= dm_csrs_i.ndmreset_o
        hartsel <<= dm_csrs_i.hartsel_o
        dm_csrs_i.hartinfo_i_zero1[0] <<= hartinfo_i.zero0
        dm_csrs_i.hartinfo_i_nscratch[0] <<= hartinfo_i.nscratch
        dm_csrs_i.hartinfo_i_zero0[0] <<= hartinfo_i.zero0
        dm_csrs_i.hartinfo_i_dataaccess[0] <<= hartinfo_i.dataaccess
        dm_csrs_i.hartinfo_i_datasize[0] <<= hartinfo_i.datasize
        dm_csrs_i.hartinfo_i_dataaddr[0] <<= hartinfo_i.dataaddr
        dm_csrs_i.halted_i <<= halted
        dm_csrs_i.unavailable_i <<= io.unavailable_i
        dm_csrs_i.resumeack_i <<= resumeack
        haltreq               <<= dm_csrs_i.haltreq_o
        resumereq             <<= dm_csrs_i.resumereq_o
        clear_resumeack       <<= dm_csrs_i.clear_resumeack_o
        cmd_valid             <<= dm_csrs_i.cmd_valid_o
        cmd.cmdtype                   <<= dm_csrs_i.cmd_o_cmd_e
        cmd.control                   <<= dm_csrs_i.cmd_o_control
        dm_csrs_i.cmderror_valid_i <<= cmderror_valid        
        dm_csrs_i.cmderror_i <<= cmderror              
        dm_csrs_i.cmdbusy_i <<= cmdbusy               
        progbuf               <<= dm_csrs_i.progbuf_o
        dm_csrs_i.data_i <<= data_mem_csrs         
        dm_csrs_i.data_valid_i <<= data_valid            
        data_csrs_mem         <<= dm_csrs_i.data_o
        sbaddress_csrs_sba    <<= dm_csrs_i.sbaddress_o
        dm_csrs_i.sbaddress_i <<= sbaddress_sba_csrs    
        sbaddress_write_valid <<= dm_csrs_i.sbaddress_write_valid_o
        sbreadonaddr          <<= dm_csrs_i.sbreadonaddr_o
        sbautoincrement       <<= dm_csrs_i.sbautoincrement_o
        sbaccess              <<= dm_csrs_i.sbaccess_o
        sbreadondata          <<= dm_csrs_i.sbreadondata_o
        sbdata_write          <<= dm_csrs_i.sbdata_o
        sbdata_read_valid     <<= dm_csrs_i.sbdata_read_valid_o
        sbdata_write_valid    <<= dm_csrs_i.sbdata_write_valid_o
        dm_csrs_i.sbdata_i <<= sbdata_read           
        dm_csrs_i.sbdata_valid_i <<= sbdata_valid          
        dm_csrs_i.sbbusy_i <<= sbbusy                
        dm_csrs_i.sberror_valid_i <<= sberror_valid         
        dm_csrs_i.sberror_i <<= sberror
        io.dmi_resp_o <<= dmi_resp_o.packed

        # -----------------------
        # dm_sba
        # -----------------------
        dm_sba_i.dmactive_i <<= io.dmactive_o
        
        io.master_req_o <<= dm_sba_i.master_req_o
        io.master_add_o <<= dm_sba_i.master_add_o
        io.master_we_o <<= dm_sba_i.master_we_o
        io.master_wdata_o <<= dm_sba_i.master_wdata_o
        io.master_be_o <<= dm_sba_i.master_be_o
        dm_sba_i.master_gnt_i <<= io.master_gnt_i
        dm_sba_i.master_r_valid_i <<= io.master_r_valid_i
        dm_sba_i.master_r_rdata_i <<= io.master_r_rdata_i

        dm_sba_i.sbaddress_i <<= sbaddress_csrs_sba
        sbaddress_sba_csrs <<= dm_sba_i.sbaddress_o
        dm_sba_i.sbaddress_write_valid_i <<= sbaddress_write_valid
        dm_sba_i.sbreadonaddr_i <<= sbreadonaddr
        dm_sba_i.sbautoincrement_i <<= sbautoincrement
        dm_sba_i.sbaccess_i <<= sbaccess
        dm_sba_i.sbreadondata_i <<= sbreadondata
        dm_sba_i.sbdata_i <<= sbdata_write
        dm_sba_i.sbdata_read_valid_i <<= sbdata_read_valid
        dm_sba_i.sbdata_write_valid_i <<= sbdata_write_valid
        sbdata_read <<= dm_sba_i.sbdata_o
        sbdata_valid <<= dm_sba_i.sbdata_valid_o
        sbbusy <<= dm_sba_i.sbbusy_o
        sberror_valid <<= dm_sba_i.sberror_valid_o
        sberror <<= dm_sba_i.sberror_o

        # -----------------------
        # dm_mem
        # -----------------------
        io.debug_req_o <<= dm_mem_i.debug_req_o
        dm_mem_i.hartsel_i <<= hartsel
        dm_mem_i.haltreq_i <<= haltreq
        dm_mem_i.resumereq_i <<= resumereq
        dm_mem_i.clear_resumeack_i <<= clear_resumeack
        halted <<= dm_mem_i.halted_o
        resumeack <<= dm_mem_i.resuming_o
        dm_mem_i.cmd_valid_i <<= cmd_valid
        dm_mem_i.cmd_i <<= cmd.packed
        cmderror_valid <<= dm_mem_i.cmderror_valid_o
        cmderror <<= dm_mem_i.cmderror_o
        cmdbusy <<= dm_mem_i.cmdbusy_o
        dm_mem_i.progbuf_i <<= progbuf
        dm_mem_i.data_i <<= data_csrs_mem
        data_mem_csrs <<= dm_mem_i.data_o
        data_valid <<= dm_mem_i.data_valid_o
        dm_mem_i.req_i <<= io.slave_req_i
        dm_mem_i.we_i <<= io.slave_we_i
        dm_mem_i.addr_i <<= io.slave_addr_i
        dm_mem_i.wdata_i <<= io.slave_wdata_i
        dm_mem_i.be_i <<= io.slave_be_i
        io.slave_rdata_o <<= dm_mem_i.rdata_o

    return DM_TOP()


if __name__ == '__main__':
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(dm_top()), "dm_top.fir"))
