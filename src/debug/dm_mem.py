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
   Date: 2021-05-19
   File Name: dm_mem.py
   Description: Memory module for execution-based debug clients
"""
from pyhcl import *
from src.debug.dm_pkg import *
from src.include.utils import *
from src.include.pkg import *


def dm_mem(NrHarts: int = 1, BusWidth: int = 32, DmBaseAddress: int = 0):
    # local parameters
    SelectableHarts = CatBits(*[U.w(1)(1) * NrHarts])
    DbgAddressBits: int = 12
    HartSelLen: int = 1 if NrHarts == 1 else clog2(NrHarts)
    NrHartsAligned: int = 2 ** HartSelLen
    MaxAar: int = 4 if BusWidth == 64 else 3
    HasSndScratch = (U(DmBaseAddress) != U(0))
    # Depending on whether we are at the zero page or not we either use 'x0' of 'x10/a0'
    LoadBaseAddr = Mux(U(DmBaseAddress == U(0)), U.w(5)(0), U.w(5)(10))

    DataBaseAddr = DataAddr
    DataEndAddr = DataAddr + U(4) * U(DataCount) - U(1)
    ProgBufBaseAddr = DataAddr - U(4) * U(DataCount) - U(1)
    ProgBufEndAddr = DataEndAddr - U(1)
    AbstractCmdBaseAddr = ProgBufBaseAddr - U(40)
    AbstractCmdEndAddr = ProgBufBaseAddr - U(1)

    WhereToAddr = U(0x300)
    FlagsBaseAddr = U(0x400)
    FlagsEndAddr = U(0x7FF)

    HaltedAddr = U(0x100)
    GoingAddr = U(0x104)
    ResumingAddr = U(0x108)
    ExceptionAddr = U(0x10C)

    # FSM
    STATE_E_WIDTH = 2

    Idle = U.w(2)(0)
    Go = U.w(2)(1)
    Resume = U.w(2)(2)
    CmdExcuting = U.w(2)(3)

    class DM_MEM(Module):
        io = IO(
            debug_req_o=Output(U.w(NrHarts)),
            hartsel_i=Input(U.w(20)),
            # from Ctrl and Status register
            haltreq_i=Input(U.w(NrHarts)),
            resumereq_i=Input(U.w(NrHarts)),
            clear_resumeack_i=Input(Bool),

            # state bits
            halted_o=Output(U.w(NrHarts)),          # hart acknowledge halt
            resuming_o=Output(U.w(NrHarts)),        # hart is resuming

            progbuf_i=Input(Vec(ProgBufSize, U.w(32))),     # program buffer to expose

            data_i=Input(Vec(DataCount, U.w(32))),      # data in
            data_o=Output(Vec(DataCount, U.w(32))),     # data out
            data_valid_o=Output(Bool),                  # data out is valid

            # abstract command interfacae
            cmd_valid_i=Input(Bool),
            cmd_i=Input(U.w(32)),       # command_t
            cmderror_valid_o=Output(Bool),
            cmderror_o=Output(U.w(CMDERR_E_WIDTH)),
            cmdbusy_o=Output(Bool),

            # data interface

            # SRAM interface
            req_i=Input(Bool),
            we_i=Input(Bool),
            addr_i=Input(U.w(BusWidth)),
            wdata_i=Input(U.w(BusWidth)),
            be_i=Input(U.w(int(BusWidth/8))),
            rdata_o=Output(U.w(BusWidth))
        )
        cmd_i = command_t(False)
        cmd_i.cmdtype <<= io.cmd_i[31:24]
        cmd_i.control <<= io.cmd_i[23:0]

        progbuf = Wire(Vec(int(ProgBufSize/2), U.w(64)))
        abstract_cmd = Wire(Vec(8, U.w(64)))
        halted = gen_ff(NrHarts, 0)
        resuming = gen_ff(NrHarts, 0)
        resume, go, going = [Wire(Bool) for _ in range(3)]

        exception = Wire(Bool)
        unsupported_command = Wire(Bool)

        rom_rdata = Wire(U.w(64))
        rdata = gen_ff(64, 0)
        word_enable32_q = RegInit(Bool(False))

        # this is needed to avoid lint warnings related to array indexing
        # resize hartsel to valid range
        hartsel, wdata_hartsel = [Wire(U.w(HartSelLen)) for _ in range(2)]

        resumereq_aligned, haltreq_aligned, halted_d_aligned, halted_aligned, \
        resumereq_wdata_aligned, resuming_d_aligned = [vec_init_wire(NrHartsAligned, Bool, Bool(False)) for _ in range(6)]

        halted_q_aligned, resuming_q_aligned = [vec_init(NrHartsAligned, Bool, Bool(False)) for _ in range(2)]

        vec_assign(NrHartsAligned, resumereq_aligned, io.resumereq_i)
        vec_assign(NrHartsAligned, haltreq_aligned, io.haltreq_i)
        vec_assign(NrHartsAligned, resumereq_wdata_aligned, io.resumereq_i)

        vec_assign(NrHartsAligned, halted_q_aligned, halted.q)
        vec_assign(NrHartsAligned, halted.d, halted_d_aligned)
        vec_assign(NrHartsAligned, resuming_q_aligned, resuming.q)
        vec_assign(NrHartsAligned, resuming.d, resuming_d_aligned)

        # distinguish whether we need to forward data from the ROM or the FSM
        # latch the address for this

        fwd_rom = gen_ff(1, 0)
        ac_ar = ac_ar_cmd_t()

        # Abstract Command Access Register
        ac_ar <<= io.cmd_i
        io.debug_req_o <<= io.haltreq_i
        io.halted_o <<= halted.q
        io.resuming_o <<= resuming.q

        # reshapge progbuf
        progbuf <<= io.progbuf_i

        state = gen_ff(STATE_E_WIDTH, 0)

        # hart ctrl queue
        io.cmderror_valid_o <<= Bool(False)
        io.cmderror_o <<= CmdErrNone
        state.n <<= state.q
        go <<= Bool(False)
        resume <<= Bool(False)
        io.cmdbusy_o <<= Bool(True)

        # FSM
        with when(state.q == Idle):
            io.cmdbusy_o <<= Bool(False)
            with when(io.cmd_valid_i & halted_q_aligned[hartsel] & (~unsupported_command)):
                # give the go signal
                state.n <<= Go
            with elsewhen(io.cmd_valid_i):
                # hart must be halted for all requests
                io.cmderror_valid_o <<= Bool(True)
                io.cmderror_o <<= CmdErrorHaltResume
            # CSRs want to resume, the request is ignored when the hart is
            # requested to halt or it didn't clear the resuming_q bit before
            with when(resumereq_aligned[hartsel] & (~resuming_q_aligned[hartsel]) &
                      (~haltreq_aligned[hartsel]) & halted_q_aligned[hartsel]):
                state.n <<= Resume

        with elsewhen(state.q == Go):
            # we are already busy here since we scheduled the execution of a program
            io.cmdbusy_o <<= Bool(True)
            go <<= Bool(True)
            # the thread is now executing the command, track its state
            with when(going):
                state.n <<= CmdExcuting

        with elsewhen(state.q == Resume):
            io.cmdbusy_o <<= Bool(True)
            resume <<= Bool(True)
            with when(resuming_q_aligned[hartsel]):
                state.n <<= Idle

        with elsewhen(state.q == CmdExcuting):
            io.cmdbusy_o <<= Bool(True)
            go <<= Bool(False)
            # wait until the hart has halted again
            with when(halted_aligned[hartsel]):
                state.n <<= Idle

        # only signal once that cmd is unsupported so that we can clear cmderr
        # in subsequent writes to abstractcs
        with when(unsupported_command & io.cmd_valid_i):
            io.cmderror_valid_o <<= Bool(True)
            io.cmderror_o <<= CmdErrNotSupported

        with when(exception):
            io.cmderror_valid_o <<= Bool(True)
            io.cmderror_o <<= CmdErrorException

        # word mus for 32bit and 64bit buses
        word_mux = Wire(U.w(64))
        word_mux <<= Mux(fwd_rom.q, rom_rdata, rdata.q)

        if BusWidth == 64:
            io.rdata_o <<= word_mux
        else:
            io.rdata_o <<= Mux(word_enable32_q, word_mux[63:32], word_mux[31:0])

        # read/write logic
        data_bits = Wire(U.w(64))
        rdata_vec = vec_init_wire(8, U.w(8), U(0))

        vec_assign(NrHartsAligned, halted_d_aligned, halted.q)
        vec_assign(NrHartsAligned, resuming_d_aligned, resuming.q)
        rdata.n <<= rdata.q
        # convert the data in bits representation
        data_bits <<= io.data_i

        # write data in csr register
        io.data_valid_o <<= Bool(False)
        exception <<= Bool(False)
        halted_aligned <<= U(0)
        going <<= Bool(False)

        #  The resume ack signal is lowered when the resume request is deasserted
        with when(io.clear_resumeack_i):
            resuming_d_aligned[hartsel] <<= Bool(False)
        # we've got a new request
        with when(io.req_i):
            # this is a write
            with when(io.we_i):
                with when(io.addr_i[DbgAddressBits-1:0] == HaltedAddr):
                    halted_aligned[wdata_hartsel] <<= Bool(True)
                with elsewhen(io.addr_i[DbgAddressBits-1:0] == GoingAddr):
                    going <<= Bool(True)
                with elsewhen(io.addr_i[DbgAddressBits-1:0] == ResumingAddr):
                    # clear the halted flag as the hart resumed execution
                    halted_d_aligned[wdata_hartsel] <<= Bool(False)
                    #  set the resuming flag which needs to be cleared by the debugger
                    resuming_d_aligned[wdata_hartsel] <<= Bool(True)
                with elsewhen(io.addr_i[DbgAddressBits-1:0] == ExceptionAddr):
                    exception <<= Bool(True)
                with elsewhen((io.addr_i[DbgAddressBits-1:0] >= DataBaseAddr) &
                              (io.addr_i[DbgAddressBits-1:0] <= DataEndAddr)):
                    io.dataa_valid_o <<= Bool(True)
                    data_bits <<= CatBits(*[Mux(io.be_i[i], io.wdata[i*8+7:i*8], U.w(8)(0))
                                            for i in range(int(BusWidth/8)-1, -1, -1)])
            # this is a read
            with otherwise():
                with when(io.addr_i[DbgAddressBits-1:0] == WhereToAddr):
                    # variable ROM content
                    # variable jump to abstract md, program_buffer or resume
                    with when(resumereq_wdata_aligned[wdata_hartsel]):
                        tmp = Wire(U.w(21))
                        tmp <<= ResumeAddress[11:0] - WhereToAddr
                        rdata.n <<= CatBits(U.w(32)(0), U.w(11)(0), tmp)

                    # there is a command active so jump there
                    with when(io.cmdbusy_o):
                        # transfer not set is shortcut to the program buffer if postexec is set
                        # keep this statement narrow to not catch invalid commands
                        with when((cmd_i.cmdtype == AccessRegister) & (~ac_ar.transfer) & ac_ar.postexec):
                            tmp = Wire(U.w(21))
                            tmp <<= ProgBufBaseAddr - WhereToAddr
                            rdata.n <<= CatBits(U.w(32)(0), U.w(11)(0), tmp)
                        with otherwise():
                            # this is a legit abstract cmd -> execute it
                            tmp = Wire(U.w(21))
                            tmp <<= AbstractCmdBaseAddr - WhereToAddr
                            rdata.n <<= CatBits(U.w(32)(0), U.w(11)(0), tmp)
                with elsewhen((io.addr_i[DbgAddressBits-1:0] >= DataBaseAddr) & (io.addr_i[DbgAddressBits-1:0] <= DataEndAddr)):
                    rdata.n <<= CatBits(io.data_i[io.addr_i[DbgAddressBits-1:3] - DataBaseAddr[DbgAddressBits-1:3] + U(1)],
                                        io.data_i[io.addr_i[DbgAddressBits-1:3] - DataBaseAddr[DbgAddressBits-1:3]])
                with elsewhen((io.addr_i[DbgAddressBits-1:0] >= ProgBufBaseAddr) & (io.addr_i[DbgAddressBits-1:0] <= ProgBufEndAddr)):
                    rdata.n <<= progbuf[io.addr_i[DbgAddressBits-1:3] - ProgBufBaseAddr[DbgAddressBits-1:3]]
                # two slots for abstract command
                with elsewhen((io.addr_i[DbgAddressBits-1:0] >= AbstractCmdBaseAddr) & (io.addr_i[DbgAddressBits-1:0] <= AbstractCmdEndAddr)):
                    # return the correct address index
                    rdata.n <<= abstract_cmd[io.addr_i[DbgAddressBits-1:3] - AbstractCmdBaseAddr[DbgAddressBits-1:3]]
                # harts are polling for flags here
                with elsewhen((io.addr_i[DbgAddressBits-1:0] >= FlagsBaseAddr) & (io.addr_i[DbgAddressBits-1:0] <= FlagsEndAddr)):
                    # release the corresponding hart
                    with when(CatBits(io.addr_i[DbgAddressBits-1:3], U.w(3)(0)) - FlagsBaseAddr[DbgAddressBits-1:0] ==
                              (hartsel & CatBits(CatBits(*[U.w(1)(1) * (DbgAddressBits-3)]), U.w(3)(0)))):
                        rdata_vec[hartsel & U.w(3)(0x111)] <<= CatBits(U.w(6)(0), resume, go)
                    rdata.n <<= CatBits(*rdata)
        io.data_o <<= data_bits

        # this abstract command is currently unsupported
        unsupported_command <<= Bool(False)
        # default memory
        # if ac_ar.transfer si not set then we can take a shortcut to the program buffer
        abstract_cmd[0] <<= CatBits(Mux(HasSndScratch, auipc(U.w(5)(0x10), U(0)), nop()), illegal())
        abstract_cmd[1] <<= CatBits(Mux(HasSndScratch, slli(U.w(5)(10), U.w(5)(10), U.w(6)(12)), nop()),
                                    Mux(HasSndScratch, srli(U.w(5)(10), U.w(5)(10), U.w(6)(12)), nop()))
        abstract_cmd[2] <<= CatBits(nop(), nop())
        abstract_cmd[3] <<= CatBits(nop(), nop())
        abstract_cmd[4] <<= CatBits(ebreak(), Mux(HasSndScratch, csrr(CSR_DSCRATCH1, U.w(5)(10)), nop()))
        abstract_cmd[5] <<= U(0)
        abstract_cmd[6] <<= U(0)
        abstract_cmd[7] <<= U(0)

    return DM_MEM()
