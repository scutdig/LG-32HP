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
   Date: 2021-05-11
   File Name: dm_csrs.py
   Description: Debug CSRs. Communication over Debug Transport Module (DTM)
"""
from pyhcl import *
from src.debug.dm_pkg import *
from math import *
from src.include.utils import *


def dm_csrs(NrHarts: int = 1, BusWidth: int = 32):
    # local parameters
    SelectableHarts = CatBits(*[U.w(1)(1) * NrHarts])
    HartSelLen = 1 if NrHarts == 1 else clog2(NrHarts)
    NrHartsAligned = 2 ** HartSelLen
    # localparam dm::dm_csr_e DataEnd = dm::dm_csr_e'(dm::Data0 + {4'h0, dm::DataCount} - 8'h1);
    DataEnd = 4 + DataCount - 1
    # localparam dm::dm_csr_e ProgBufEnd = dm::dm_csr_e'(dm::ProgBuf0 + {4'h0, dm::ProgBufSize} - 8'h1);
    ProgBufEnd = 0x20 + ProgBufSize - 1

    class DM_CSRS(Module):
        """
        Expanded IO ports
            - dmi_req_i
            - dmi_resp_o
            - hartinfo_i
            - cmd_o
        """
        io = IO(
            testmode_i=Input(Bool),
            dmi_rst_ni=Input(Bool),         # Debug Module Intf reset active-low
            dmi_req_valid_i=Input(Bool),
            dmi_req_ready_o=Output(Bool),

            # typedef struct packed {
            #     logic [6:0]  addr;
            #     dtm_op_e     op;
            #     logic [31:0] data;
            # } dmi_req_t;
            # dmi_req_i, expend
            dmi_req_i_addr=Input(U.w(7)),
            dmi_req_i_op=Input(U.w(DTM_OP_WIDTH)),
            dmi_req_i_data=Input(U.w(32)),

            # Every request needs a response one cycle later
            dmi_resp_valid_o=Output(Bool),
            dmi_resp_ready_i=Input(Bool),

            # typedef struct packed  {
            #     logic [31:0] data;
            #     logic [1:0]  resp;
            # } dmi_resp_t;
            # dmi_resp_o extend
            dmi_resp_o_data=Output(U.w(32)),
            dmi_resp_o_resp=Output(U.w(2)),

            # global ctrl
            ndmreset_o=Output(Bool),        # non-debug module reset active-high
            dmactive_o=Output(Bool),        # 1-> debug_module is active,
                                            # 0 -> synchronous re-set
            # typedef struct packed {
            #     logic [31:24] zero1;
            #     logic [23:20] nscratch;
            #     logic [19:17] zero0;
            #     logic         dataaccess;
            #     logic [15:12] datasize;
            #     logic [11:0]  dataaddr;
            # } hartinfo_t;
            # hart status
            # hartinfo_i expend, static hartinfo
            hartinfo_i_zero1=Input(Vec(NrHarts, U.w(8))),
            hartinfo_i_nscratch=Input(Vec(NrHarts, U.w(4))),
            hartinfo_i_zero0=Input(Vec(NrHarts, U.w(3))),
            hartinfo_i_dataaccess=Input(Vec(NrHarts, Bool)),
            hartinfo_i_datasize=Input(Vec(NrHarts, U.w(4))),
            hartinfo_i_dataaddr=Input(Vec(NrHarts, U.w(12))),
            halted_i=Input(U.w(NrHarts)),                   # hart is halted
            unavailable_i=Input(U.w(NrHarts)),              # e.g.: powered down
            resumeack_i=Input(U.w(NrHarts)),                # hart acknowledged resume request

            # hart control
            hartsel_o=Output(U.w(20)),                      # hartselect to ctrl module
            haltreq_o=Output(U.w(NrHarts)),                 # request to halt a hart
            resumereq_o=Output(U.w(NrHarts)),               # request hart to resume
            clear_resumeack_o=Output(Bool),

            cmd_valid_o=Output(Bool),                       # debugger writing to cmd field
            # typedef struct packed {
            #     cmd_e        cmdtype;
            #     logic [23:0] control;
            # } command_t;
            # cmd_o expand, abstract command
            cmd_o_cmd_e=Output(U.w(CMD_E_WIDTH)),
            cmd_o_control=Output(U.w(24)),
            cmderror_valid_i=Input(Bool),                   # an error occurred
            cmderror_i=Input(U.w(CMDERR_E_WIDTH)),          # this error occurred
            cmdbusy_i=Input(Bool),                          # cmd is curently busy executing

            progbuf_o=Output(Vec(ProgBufSize, U.w(32))),    # to system bus
            data_o=Output(Vec(DataCount, U.w(32))),
            data_i=Input(Vec(DataCount, U.w(32))),
            data_valid_i=Input(Bool),

            # system bus access module (SBA)
            sbaddress_o=Output(U.w(BusWidth)),
            sbaddress_i=Input(U.w(BusWidth)),
            sbaddress_write_valid_o=Output(Bool),
            # control signals in
            sbreadonaddr_o=Output(Bool),
            sbautoincrement_o=Output(Bool),
            sbaccess_o=Output(U.w(3)),
            # data out
            sbreadondata_o=Output(Bool),
            sbdata_o=Output(U.w(BusWidth)),
            sbdata_read_valid_o=Output(Bool),
            sbdata_write_valid_o=Output(Bool),
            # read data in
            sbdata_i=Input(U.w(BusWidth)),
            sbdata_valid_i=Input(Bool),
            # control signals
            sbbusy_i=Input(Bool),
            sberror_valid_i=Input(Bool),                    # bus error occurred
            sberror_i=Input(U.w(3)),                        # bus error occurred
        )

        dtm_op = Wire(U.w(DTM_OP_WIDTH))
        dtm_op <<= io.dmi_req_i_op

        resp_queue_full = Wire(Bool)
        resp_queue_empty = Wire(Bool)
        resp_queue_push = Wire(Bool)
        resp_queue_pop = Wire(Bool)
        resp_queue_data = Wire(U.w(32))

        haltsum0, haltsum1, haltsum2, haltsum3 = [Wire(U.w(32)) for _ in range(4)]
        halted = Wire(U.w(((NrHarts-1)/2**5 + 1) * 32))
        halted_reshaped0 = Wire(Vec((NrHarts-1)/2**5 + 1, U.w(32)))
        halted_reshaped1 = Wire(Vec((NrHarts-1)/2**10 + 1, U.w(32)))
        halted_reshaped2 = Wire(Vec((NrHarts-1)/2**15 + 1, U.w(32)))
        halted_flat1, halted_flat2 = [Wire(U.w(((NrHarts-1)/2**10+1)*32-1)) for _ in range(2)]
        halted_flat3 = Wire(U.w(32))

        # haltsum0
        hartsel_idx0 = Wire(U.w(15))
        halted <<= U(0)
        haltsum0 <<= U(0)
        hartsel_idx0 <<= io.hartsel_o[19:5]
        halted[NrHarts-1:0] = io.halted_i
        halted_reshaped0 <<= halted
        with when(hartsel_idx0 < U((NrHarts-1)/2**5+1)):
            haltsum0 <<= halted_reshaped0[hartsel_idx0]

        # haltsum1
        hartsel_idx1 = Wire(U.w(10))
        halted_flat1 <<= U(0)
        haltsum1 <<= U(0)
        hartsel_idx1 <<= io.hartsel_o[19:10]

        for k in range((NrHarts-1)/2**5+1):
            halted_flat1[k] <<= reduce_or(halted_reshaped0[k], 32)
        halted_reshaped1 <<= halted_flat1

        with when(hartsel_idx1 < U((NrHarts-1)/2**10+1)):
            haltsum1 <<= halted_reshaped1[hartsel_idx1]

        # haltsum2
        hartsel_idx2 = Wire(U.w(5))
        halted_flat2 <<= U(0)
        haltsum2 <<= U(0)
        hartsel_idx2 <<= io.hartsel_o[19:15]

        for k in range((NrHarts-1)/2**10+1):
            halted_flat2[k] <<= reduce_or(halted_reshaped1[k], 32)
        halted_reshaped2 <<= halted_flat2

        with when(hartsel_idx2 < U((NrHarts-1)/2**15+1)):
            haltsum2 <<= halted_reshaped2[hartsel_idx2]

        # haltsum3
        halted_flat3 <<= U(0)
        for k in range(NrHarts/2**15+1):
            halted_flat3[k] <<= reduce_or(halted_reshaped2[k], 32)
        haltsum3 <<= halted_flat3

        dmstatus = dmstatus_t()
        dmcontrol = packed_ff(dmcontrol_t(True), dmcontrol_t(False))
        abstractcs = abstractcs_t()
        cmderr = gen_ff(CMDERR_E_WIDTH, 0)
        command = packed_ff(command_t(True), command_t(False))
        cmd_valid = gen_ff(1, 0)
        abstractauto = packed_ff(abstractauto_t(True), abstractauto_t(False))
        sbcs = packed_ff(sbcs_t(True), sbcs_t(False))
        sbaddr = gen_ff(64, 0)
        sbdata = gen_ff(64, 0)

        havereset = gen_ff(NrHarts, 2**NrHarts-1)

        # program buffer
        progbuf = vec_init(ProgBufSize, U.w(32), 0)
        data = vec_init(DataCount, U.w(32), 0)

        selected_hart = Wire(U.w(HartSelLen))

        # a successful response returns zero
        io.dmi_resp_o_resp <<= DTM_SUCCESS
        io.dmi_resp_valid_o <<= ~resp_queue_empty
        io.dmi_req_ready_o <<= ~resp_queue_full
        resp_queue_push <<= io.dmi_req_valid_i & io.dmi_req_ready_o
        # SBA
        io.sbautoincrement_o <<= sbcs.q.sbautoincrement
        io.sbreadonaddr_o <<= sbcs.q.sbreadonaddr
        io.sbreadondata_o <<= sbcs.q.sbreadondata
        io.sbaccess_o <<= sbcs.q.sbaccess
        io.sbdata_o <<= sbdata.q[BusWidth-1:0]
        io.sbaddress_o <<= sbaddr.q[BusWidth-1:0]

        io.hartsel_o <<= CatBits(dmcontrol.q.haartselhi, dmcontrol.q.hartsello)

        # needed to avoid lint warnings
        havereset_d_aligned, havereset_q_aligned, resumeack_aligned, unavailable_aligned, halted_aligned = [Wire(U.w(NrHartsAligned)) for _ in range(5)]
        resumeack_aligned <<= io.resumeack_i
        unavailable_aligned <<= io.unavailable_i
        halted_aligned <<= io.halted_i

        havereset.n <<= havereset_d_aligned
        havereset_q_aligned <<= havereset.q

        # Original code here, hartinfo_aligned is defined as hartinfo_t (packed)
        # But actually we don't need to split them
        hartinfo_aligned = Wire(U.w(NrHartsAligned))
        hartinfo_aligned <<= U(0)
        hartinfo_aligned <<= CatBits(U.w(NrHartsAligned-NrHarts)(0), io.hartinfo_i_zero1, io.hartinfo_i_nscratch,
                                     io.hartinfo_i_zero0, io.hartinfo_i_dataaccess, io.hartinfo_i_datasize, io.hartinfo_i_dataaddr)

        # helper variables
        dm_csr_addr = Wire(U.w(DM_CSR_E_WIDTH))
        sbcs = sbcs_t(False)
        a_abstractcs = abstractcs_t()
        autoexecdata_idx = Wire(U.w(4))    # 0 == Data0 ... 11 == Data11

        # Get the data index, i.e. 0 for Data0 up to 11 for Data11
        dm_csr_addr <<= CatBits(U.w(1)(0), io.dmi_req_i_addr)
        autoexecdata_idx <<= dm_csr_addr - Data0

    return DM_CSRS()
