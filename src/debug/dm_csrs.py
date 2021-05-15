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
from src.rtl.fifo import *


def dm_csrs(NrHarts: int = 1, BusWidth: int = 32):
    # local parameters
    SelectableHarts = CatBits(*[U.w(1)(1) * U(NrHarts)])
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
        fifo_i_io = fifo(FALL_THROUGH=0, DATA_WIDTH=32, DEPTH=2).io

        dtm_op = Wire(U.w(DTM_OP_WIDTH))
        dtm_op <<= io.dmi_req_i_op

        resp_queue_full = Wire(Bool)
        resp_queue_empty = Wire(Bool)
        resp_queue_push = Wire(Bool)
        resp_queue_pop = Wire(Bool)
        resp_queue_data = Wire(U.w(32))

        haltsum0, haltsum1, haltsum2, haltsum3 = [Wire(U.w(32)) for _ in range(4)]
        halted = Wire(U.w(int(((NrHarts-1)/2**5 + 1) * 32)))
        halted_reshaped0 = Wire(Vec(int((NrHarts-1)/2**5 + 1), U.w(32)))
        halted_reshaped1 = Wire(Vec(int((NrHarts-1)/2**10 + 1), U.w(32)))
        halted_reshaped2 = Wire(Vec(int((NrHarts-1)/2**15 + 1), U.w(32)))
        halted_flat1, halted_flat2 = [Wire(U.w(int(((NrHarts-1)/2**10+1)*32))) for _ in range(2)]
        halted_flat3 = Wire(U.w(32))

        halted_flat1_vec, halted_flat2_vec = [Wire(Vec(int(((NrHarts-1)/2**10+1)*32), Bool)) for _ in range(2)]
        halted_flat3_vec = Wire(Vec(32, Bool))

        for i in range(int(((NrHarts-1)/2**10+1)*32)):
            halted_flat1_vec[i] <<= U(0)
            halted_flat2_vec[i] <<= U(0)

        for i in range(32):
            halted_flat3_vec[i] <<= U(0)

        halted_flat1 <<= CatBits(*halted_flat1_vec)
        halted_flat2 <<= CatBits(*halted_flat2_vec)
        halted_flat3 <<= CatBits(*halted_flat3_vec)

        # haltsum0
        hartsel_idx0 = Wire(U.w(15))
        halted <<= U(0)
        haltsum0 <<= U(0)
        hartsel_idx0 <<= io.hartsel_o[19:5]
        halted[NrHarts-1:0] = io.halted_i
        # halted_reshaped0 <<= halted
        for i in range(int((NrHarts-1)/2**5 + 1)):
            halted_reshaped0[i] <<= halted
        with when(hartsel_idx0 < U(int((NrHarts-1)/2**5+1))):
            haltsum0 <<= halted_reshaped0[hartsel_idx0]

        # haltsum1
        hartsel_idx1 = Wire(U.w(10))
        halted_flat1 <<= U(0)
        haltsum1 <<= U(0)
        hartsel_idx1 <<= io.hartsel_o[19:10]

        for k in range(int((NrHarts-1)/2**5+1)):
            halted_flat1_vec[k] <<= reduce_or(halted_reshaped0[k], 32)
        # halted_reshaped1 <<= halted_flat1
        for i in range(int((NrHarts-1)/2**10 + 1)):
            halted_reshaped1[i] <<= halted_flat1

        with when(hartsel_idx1 < U(int((NrHarts-1)/2**10+1))):
            haltsum1 <<= halted_reshaped1[hartsel_idx1]

        # haltsum2
        hartsel_idx2 = Wire(U.w(5))
        halted_flat2 <<= U(0)
        haltsum2 <<= U(0)
        hartsel_idx2 <<= io.hartsel_o[19:15]

        for k in range(int((NrHarts-1)/2**10+1)):
            halted_flat2_vec[k] <<= reduce_or(halted_reshaped1[k], 32)
        # halted_reshaped2 <<= halted_flat2
        for i in range(int((NrHarts-1)/2**15 + 1)):
            halted_reshaped2[i] <<= halted_flat2

        with when(hartsel_idx2 < U(int((NrHarts-1)/2**15+1))):
            haltsum2 <<= halted_reshaped2[hartsel_idx2]

        # haltsum3
        halted_flat3 <<= U(0)
        for k in range(int(NrHarts/2**15+1)):
            halted_flat3_vec[k] <<= reduce_or(halted_reshaped2[k], 32)
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
        progbuf = packed_ff(vec_init(ProgBufSize, U.w(32), U(0)), Wire(Vec(ProgBufSize, U.w(32))))
        data = packed_ff(vec_init(DataCount, U.w(32), U(0)), Wire(Vec(DataCount, U.w(32))))

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

        io.hartsel_o <<= CatBits(dmcontrol.q.hartselhi, dmcontrol.q.hartsello)

        # needed to avoid lint warnings
        havereset_d_aligned, havereset_q_aligned, resumeack_aligned, unavailable_aligned, halted_aligned = \
            [Wire(Vec(NrHartsAligned, Bool)) for _ in range(5)]

        for i in range(NrHartsAligned):
            if i >= NrHarts:
                resumeack_aligned[i] <<= U(0)
                unavailable_aligned[i] <<= U(0)
                halted_aligned[i] <<= U(0)
            else:
                resumeack_aligned[i] <<= io.resumeack_i[i]
                unavailable_aligned[i] <<= io.unavailable_i[i]
                halted_aligned[i] <<= io.halted_i[i]

        havereset.n <<= CatBits(*havereset_d_aligned)
        # havereset_q_aligned <<= havereset.q
        for i in range(NrHartsAligned):
            if i >= NrHarts:
                havereset_q_aligned[i] <<= U(0)
            else:
                havereset_q_aligned[i] <<= havereset.q[i]

        # Original code here, hartinfo_aligned is defined as hartinfo_t (packed)
        # But actually we don't need to split them
        hartinfo_aligned = Wire(U.w(NrHartsAligned))
        hartinfo_aligned_vec = Wire(Vec(NrHartsAligned, Bool))
        for i in range(NrHartsAligned):
            hartinfo_aligned_vec[i] <<= U(0)
        hartinfo_aligned <<= CatBits(*hartinfo_aligned_vec)
        hartinfo_aligned <<= U(0)
        hartinfo_aligned <<= CatBits(U.w(NrHartsAligned-NrHarts)(0), *io.hartinfo_i_zero1, *io.hartinfo_i_nscratch,
                                     *io.hartinfo_i_zero0, *io.hartinfo_i_dataaccess, *io.hartinfo_i_datasize, *io.hartinfo_i_dataaddr)

        # helper variables
        dm_csr_addr = Wire(U.w(DM_CSR_E_WIDTH))
        a_sbcs = sbcs_t(False)
        a_abstractcs = abstractcs_t()
        autoexecdata_idx = Wire(U.w(4))    # 0 == Data0 ... 11 == Data11

        # Get the data index, i.e. 0 for Data0 up to 11 for Data11
        dm_csr_addr <<= CatBits(U.w(1)(0), io.dmi_req_i_addr)
        autoexecdata_idx <<= dm_csr_addr - Data0

        # --------------------
        # Static Values (R/0)
        # --------------------
        # dmstatus
        dmstatus.packed <<= U(0)
        dmstatus.version <<= DbgVersion013
        # no authentication implemented
        dmstatus.authenticated <<= U.w(1)(1)
        # we do not support halt-on-reset sequence
        dmstatus.hasresethaltreq <<= U.w(1)(0)

        dmstatus.allhavereset <<= havereset_q_aligned[selected_hart]
        dmstatus.anyhavereset <<= havereset_q_aligned[selected_hart]

        dmstatus.allresumeack <<= resumeack_aligned[selected_hart]
        dmstatus.anyresumeack <<= resumeack_aligned[selected_hart]

        dmstatus.allunavail <<= unavailable_aligned[selected_hart]
        dmstatus.anyunavail <<= unavailable_aligned[selected_hart]

        # as soon as we are out of the legal Hart region tell the debugger
        # that there are only non-existent harts
        dmstatus.allnonexistent <<= io.hartsel_o > U(NrHarts - 1)
        dmstatus.anynonexistent <<= io.hartsel_o > U(NrHarts - 1)

        # We are not allowed to be in multiple states at once. This is a to
        # make the running/halted and unavailable states exclusive.
        dmstatus.allhalted <<= halted_aligned[selected_hart] & (~unavailable_aligned[selected_hart])
        dmstatus.anyhalted <<= halted_aligned[selected_hart] & (~unavailable_aligned[selected_hart])

        dmstatus.allrunning <<= (~halted_aligned[selected_hart]) & (~unavailable_aligned[selected_hart])
        dmstatus.anyrunning <<= (~halted_aligned[selected_hart]) & (~unavailable_aligned[selected_hart])

        # abstractcs
        abstractcs.packed <<= U(0)
        abstractcs.datacount <<= U(DataCount)
        abstractcs.progbufsize <<= U(ProgBufSize)
        abstractcs.busy <<= io.cmdbusy_i
        abstractcs.cmderr <<= cmderr.q

        # abstractautoexec
        abstractauto.n.packed <<= abstractauto.q.packed
        abstractauto.n.zero0 <<= U(0)

        # default assignements
        # havereset_d_aligned <<= havereset.q
        for i in range(NrHartsAligned):
            if i >= NrHarts:
                havereset_d_aligned[i] <<= U(0)
            else:
                havereset_d_aligned[i] <<= havereset.q[i]
        dmcontrol.n.packed <<= dmcontrol.q.packed
        cmderr.n <<= cmderr.q
        command.n.packed <<= command.q.packed
        progbuf.n <<= progbuf.q
        data.n <<= data.q
        sbcs.n.packed <<= sbcs.q.packed
        sbaddr.n <<= io.sbaddress_i
        sbdata.n <<= sbdata.q

        resp_queue_data <<= U.w(32)(0)
        cmd_valid.n <<= Bool(False)
        io.sbaddress_write_valid_o <<= Bool(False)
        io.sbdata_read_valid_o <<= Bool(False)
        io.sbdata_write_valid_o <<= Bool(False)
        io.clear_resumeack_o <<= Bool(False)

        # helper variables
        a_sbcs.packed <<= U(0)
        a_abstractcs.packed <<= U(0)

        # reads
        with when(io.dmi_req_ready_o & io.dmi_req_valid_i & (dtm_op == DTM_READ)):
            with when((dm_csr_addr >= Data0) & (dm_csr_addr <= U(DataEnd))):
                resp_queue_data <<= data.q[Log2(autoexecdata_idx, 4)]
                with when(~io.cmdbusy_i):
                    # check whether we need to re-execute the command (just give a cmd_valid)
                    cmd_valid.n <<= abstractauto.q.autoexecdata_vec[autoexecdata_idx]
                with elsewhen(cmderr.q == CmdErrNone):
                    # An abstract command was executing while one of the data registers was read
                    cmderr.n <<= CmdErrBusy
            with elsewhen(dm_csr_addr == DMControl):
                resp_queue_data <<= dmcontrol.q.packed
            with elsewhen(dm_csr_addr == DMStatus):
                resp_queue_data <<= dmstatus.packed
            with elsewhen(dm_csr_addr == Hartinfo):
                resp_queue_data <<= hartinfo_aligned_vec[selected_hart]
            with elsewhen(dm_csr_addr == AbstractCS):
                resp_queue_data <<= abstractcs.packed
            with elsewhen(dm_csr_addr == AbstractAuto):
                resp_queue_data <<= abstractauto.q.packed
            with elsewhen(dm_csr_addr == Command):
                # command is read-only
                resp_queue_data <<= U(0)
            with elsewhen((dm_csr_addr >= ProgBuf0) & (dm_csr_addr <= U(ProgBufEnd))):
                resp_queue_data <<= progbuf.q[io.dmi_req_i_addr[clog2(ProgBufSize)-1:0]]
                with when(~io.cmdbusy_i):
                    # check whether we need to re-execute the command (just give a cmd_valid)
                    # range of autoexecprogbuf is 31:16
                    cmd_valid.n <<= abstractauto.q.autoexecprogbuf_vec[CatBits(U.w(1)(1), io.dmi_req_i_addr[3:0])]

                # An abstract command was executing while one of the progbuf registers was read
                with elsewhen(cmderr.q == CmdErrNone):
                    cmderr.n <<= CmdErrBusy
            with elsewhen(dm_csr_addr == HaltSum0):
                resp_queue_data <<= haltsum0
            with elsewhen(dm_csr_addr == HaltSum1):
                resp_queue_data <<= haltsum1
            with elsewhen(dm_csr_addr == HaltSum2):
                resp_queue_data <<= haltsum2
            with elsewhen(dm_csr_addr == HaltSum3):
                resp_queue_data <<= haltsum3
            with elsewhen(dm_csr_addr == SBCS):
                resp_queue_data <<= sbcs.q.packed
            with elsewhen(dm_csr_addr == SBAddress0):
                resp_queue_data <<= sbaddr.q[31:0]
            with elsewhen(dm_csr_addr == SBAddress1):
                resp_queue_data <<= sbaddr.q[63:0]
            with elsewhen(dm_csr_addr == SBData0):
                # access while the SBA was busy
                with when(io.sbbusy_i | sbcs.q.sbbusyerror):
                    sbcs.n.sbbusyerror <<= Bool(True)
                with otherwise():
                    io.sbdata_read_valid_o <<= sbcs.q.sberror == U(0)
                    resp_queue_data <<= sbdata.q[31:0]
            with elsewhen(dm_csr_addr == SBData1):
                # access while the SBA was busy
                with when(io.sbbusy_i | sbcs.q.sbbusyerror):
                    sbcs.n.sbbusyerror <<= Bool(True)
                with otherwise():
                    resp_queue_data <<= sbdata.q[63:32]

        # write
        with when(io.dmi_req_ready_o & io.dmi_req_valid_i & (dtm_op == DTM_WRITE)):
            with when((dm_csr_addr >= Data0) & (dm_csr_addr <= U(DataEnd))):
                if DataCount > 0:
                    # attempts to write them while busy is set does not change their value
                    with when(~io.cmdbusy_i):
                        data.n[io.dmi_req_i_addr[clog2(DataCount)-1:0]] <<= io.dmi_req_i_data
                        # check whether we need to re-execute the command (just give a cmd_valid)
                        cmd_valid.n <<= abstractauto.q.autoexecdata_vec[autoexecdata_idx]
                    # An abstract command was executing while one of the data registers was written
                    with elsewhen(cmderr.q == CmdErrNone):
                        cmderr.n <<= CmdErrBusy
            with elsewhen(dm_csr_addr == DMControl):
                dmcontrol.n.packed <<= io.dmi_req_i_data
                # clear the havreset of the selected hart
                with when(dmcontrol.n.ackhavereset):
                    havereset_d_aligned[selected_hart] <<= Bool(False)
            # DMStatus and Hartinfo are R/O registers
            # Only command error is write-able
            with elsewhen(dm_csr_addr == AbstractCS):   # W1C
                # Gets set if an abstract command fails. The bits in this
                # field remain set until they are cleared by writing 1 to
                # them. No abstract command is started until the value is
                # reset to 0.
                a_abstractcs.packed <<= io.dmi_req_i_data
                # reads during abstract command execution are not allowed
                with when(~io.cmdbusy_i):
                    cmderr.n <<= (~a_abstractcs.cmderr) & cmderr.q
                with elsewhen(cmderr.q == CmdErrNone):
                    cmderr.n <<= CmdErrBusy
            with elsewhen(dm_csr_addr == Command):
                # writes are ignored if a command is already busy
                with when(~io.cmdbusy_i):
                    cmd_valid.n <<= Bool(True)
                    command.n.packed <<= io.dmi_req_i_data
                # if there was an attempted to write during a busy execution
                # and the cmderror field is zero set the busy error
                with elsewhen(cmderr.q == CmdErrNone):
                    cmderr.n <<= CmdErrBusy
            with elsewhen(dm_csr_addr == AbstractAuto):
                # this field can only be written legally when there is no command executing
                with when(~io.cmdbusy_i):
                    abstractauto.n.packed <<= U(0)
                    abstractauto.n.autoexecdata <<= io.dmi_req_i_data[DataCount-1:0]
                    abstractauto.n.autoexecprogbuf <<= io.dmi_req_i_data[ProgBufSize-1+16:16]
                with elsewhen(cmderr.q == CmdErrNone):
                    cmderr.n <<= CmdErrBusy
            with elsewhen((dm_csr_addr >= ProgBuf0) & (dm_csr_addr <= U(ProgBufEnd))):
                # attempts to write them while busy is set does not change their value
                with when(~io.cmdbusy_i):
                    progbuf.n[io.dmi_req_i_addr[clog2(ProgBufSize)-1:0]] <<= io.dmi_req_i_data
                    # check whether we need to re-execute the command (just give a cmd_valid)
                    # this should probably throw an error if executed during another command
                    # was busy
                    # range of autoexecprogbuf is 31:16
                    cmd_valid.n <<= abstractauto.q.autoexecprogbuf_vec[CatBits(U.w(1)(1), io.dmi_req_i_addr[3:0])]
                # An abstract command was executing while one of the progbuf registers was written
                with elsewhen(cmderr.q == CmdErrNone):
                    cmderr.n <<= CmdErrBusy
            with elsewhen(dm_csr_addr == SBCS):
                # access while the SBA was ready
                with when(io.sbbusy_i):
                    sbcs.n.sbbusyerror <<= Bool(True)
                with otherwise():
                    a_sbcs.packed <<= io.dmi_req_i_data
                    sbcs.n.packed <<= a_sbcs.packed
                    # R/W1C
                    sbcs.n.sbbusyerror <<= sbcs.q.sbbusyerror & (~a_sbcs.sbbusyerror)
                    sbcs.n.sberror <<= sbcs.q.sberror & (~a_sbcs.sberror)
            with elsewhen(dm_csr_addr == SBAddress0):
                # access while the SBA was busy
                with when(io.sbbusy_i | sbcs.q.sbbusyerror):
                    sbcs.n.sbbusyerror <<= Bool(True)
                with otherwise():
                    sbaddr.n <<= CatBits(U.w(32)(0), io.dmi_req_i_data)
                    io.sbaddress_write_valid_o <<= (sbcs.q.sberror == U(0))
            with elsewhen(dm_csr_addr == SBAddress1):
                # access while the SBA was busy
                with when(io.sbbusy_i | sbcs.q.sbbusyerror):
                    sbcs.n.sbbusyerror <<= Bool(True)
                with otherwise():
                    sbaddr.n <<= CatBits(io.dmi_req_i_data, U.w(32)(0))
            with elsewhen(dm_csr_addr == SBData0):
                # access while the SBA was busy
                with when(io.sbbusy_i | sbcs.q.sbbusyerror):
                    sbcs.n.sbbusyerror <<= Bool(True)
                with otherwise():
                    sbdata.n <<= CatBits(U.w(32)(0), io.dmi_req_i_data)
                    io.sbaddress_write_valid_o <<= (sbcs.q.sberror == U(0))
            with elsewhen(dm_csr_addr == SBData1):
                # access while the SBA was busy
                with when(io.sbbusy_i | sbcs.q.sbbusyerror):
                    sbcs.n.sbbusyerror <<= Bool(True)
                with otherwise():
                    sbdata.n <<= CatBits(io.dmi_req_i_data, U.w(32)(0))
        # hart threw a command error and has precedence over bus writes
        with when(io.cmderror_valid_i):
            cmderr.n <<= io.cmderror_i

        # update data registers
        with when(io.data_valid_i):
            data.n <<= io.data_i

        # set the havereset flag when we did a ndmreset
        with when(io.ndmreset_o):
            # havereset_d_aligned[NrHarts-1:0] <<= U(1)
            for i in range(NrHarts):
                havereset_d_aligned[i] <<= U(1)

        # --------------------
        # System Bus
        # --------------------
        # set bus error
        with when(io.sberror_valid_i):
            sbcs.n.sberror <<= io.sberror_i
        # update read data
        with when(io.sbdata_valid_i):
            sbdata.n <<= io.sbdata_i

        # dmcontrol
        dmcontrol.n.hasel <<= Bool(False)
        # we do not support resetting an individual hart
        dmcontrol.n.hartreset <<= Bool(False)
        dmcontrol.n.setresethaltreq <<= Bool(False)
        dmcontrol.n.clrresethaltreq <<= Bool(False)
        dmcontrol.n.zero1 <<= Bool(False)
        dmcontrol.n.zero0 <<= Bool(False)
        # Non-writeable, clear only
        dmcontrol.n.ackhavereset <<= Bool(False)
        with when((~dmcontrol.q.resumereq) & dmcontrol.n.resumereq):
            io.clear_resumeack_o <<= Bool(True)
        with when(dmcontrol.q.resumereq & io.resumeack_i):
            dmcontrol.n.resumereq <<= Bool(False)
        # static values for dcsr
        sbcs.n.sbversion <<= U.w(3)(1)
        sbcs.n.sbbusy <<= io.sbbusy_i
        sbcs.n.sbasize <<= U(BusWidth)
        sbcs.n.sbaccess128 <<= Bool(False)
        sbcs.n.sbaccess64 <<= (U.w(32)(BusWidth) == U.w(32)(64))
        sbcs.n.sbaccess32 <<= (U.w(32)(BusWidth) == U.w(32)(32))
        sbcs.n.sbaccess16 <<= Bool(False)
        sbcs.n.sbaccess8 <<= Bool(False)
        sbcs.n.sbaccess <<= Mux(U.w(32)(BusWidth) == U.w(32)(64), U.w(3)(3), U.w(3)(2))

        # output multiplexer
        selected_hart <<= io.hartsel_o[HartSelLen-1:0]
        io.haltreq_o <<= U(0)
        io.resumereq_o <<= U(0)
        haltreq_o_vec = Wire(Vec(NrHarts, Bool))
        resumereq_o_vec = Wire(Vec(NrHarts, Bool))
        for i in range(NrHarts):
            haltreq_o_vec[i] <<= U(0)
            resumereq_o_vec[i] <<= U(0)
        io.haltreq_o <<= CatBits(*haltreq_o_vec)
        io.resumereq_o <<= CatBits(*resumereq_o_vec)
        with when(selected_hart <= U(NrHarts-1)):
            haltreq_o_vec[selected_hart] <<= dmcontrol.q.haltreq
            resumereq_o_vec[selected_hart] <<= dmcontrol.q.resumereq

        io.dmactive_o <<= dmcontrol.q.dmactive
        # io.cmd_o <<= command.q.packed
        io.cmd_o_cmd_e <<= command.q.packed[31:24]
        io.cmd_o_control <<= command.q.packed[23:0]
        io.cmd_valid_o <<= cmd_valid.q
        io.progbuf_o <<= progbuf.q
        # io.data_o <<= data.q
        for i in range(DataCount):
            io.data_o[i] <<= data.q[i]

        resp_queue_pop <<= io.dmi_resp_ready_i & (~resp_queue_empty)

        io.ndmreset_o <<= dmcontrol.q.ndmreset

        # response FIFO
        fifo_i_io.flush_i <<= Bool(False)
        fifo_i_io.testmode_i <<= io.testmode_i
        resp_queue_full <<= fifo_i_io.full_o
        resp_queue_empty <<= fifo_i_io.empty_o
        fifo_i_io.data_i <<= resp_queue_data
        fifo_i_io.push_i <<= resp_queue_push
        io.dmi_resp_o_data <<= fifo_i_io.data_o
        fifo_i_io.pop_i <<= resp_queue_pop
        fifo_i_io.flush_but_first_i <<= Bool(False)

        # ff
        havereset.q <<= SelectableHarts & havereset.n
        # synchronous re-set of debug module, active-low, except for dmactive
        with when(~dmcontrol.q.dmactive):
            dmcontrol.q.haltreq <<= U(0)
            dmcontrol.q.resumereq <<= U(0)
            dmcontrol.q.hartreset <<= U(0)
            dmcontrol.q.ackhavereset <<= U(0)
            dmcontrol.q.zero1 <<= U(0)
            dmcontrol.q.hasel <<= U(0)
            dmcontrol.q.hartsello <<= U(0)
            dmcontrol.q.hartselhi <<= U(0)
            dmcontrol.q.zero0 <<= U(0)
            dmcontrol.q.setresethaltreq <<= U(0)
            dmcontrol.q.clrresethaltreq <<= U(0)
            dmcontrol.q.ndmreset <<= U(0)
            # this is the only write-able bit during reset
            dmcontrol.q.dmactive <<= dmcontrol.n.dmactive
            cmderr.q <<= CmdErrNone
            command.q.packed <<= U(0)
            cmd_valid.q <<= U(0)
            abstractauto.q.packed <<= U(0)
            # progbuf.q <<= U(0)
            # data.q <<= U(0)
            for i in range(ProgBufSize):
                progbuf.q[i] <<= U(0)
            for i in range(DataCount):
                data.q[i] <<= U(0)

            sbcs.q.packed <<= U(0)
            sbaddr.q <<= U(0)
            sbdata.q <<= U(0)
        with otherwise():
            dmcontrol.q.packed <<= dmcontrol.n.packed
            cmderr.q <<= cmderr.n
            command.q.packed <<= command.n.packed
            cmd_valid.q <<= cmd_valid.n
            abstractauto.q.packed <<= abstractauto.n.packed
            progbuf.q <<= progbuf.n
            data.q <<= data.n
            sbcs.q.packed <<= sbcs.n.packed
            sbaddr.q <<= sbaddr.n
            sbdata.q <<= sbdata.n

    return DM_CSRS()


if __name__ == '__main__':
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(dm_csrs()), "dm_csrs.fir"))
