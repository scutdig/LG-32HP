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
   Date: 2021-05-06
   File Name: cs_registers.py
   Description: Control and Status Registers (CSRs) based on v1.9 spec
"""
from pyhcl import *
from src.include.pkg import *
from src.include.utils import *


def hpm(addr):
    return (addr == CSR_MCYCLE) | \
      (addr == CSR_MINSTRET) | \
      (addr == CSR_MHPMCOUNTER3) | \
      (addr == CSR_MHPMCOUNTER4) | (addr == CSR_MHPMCOUNTER5) | (addr == CSR_MHPMCOUNTER6) | (addr == CSR_MHPMCOUNTER7) | \
      (addr == CSR_MHPMCOUNTER8) | (addr == CSR_MHPMCOUNTER9) | (addr == CSR_MHPMCOUNTER10) | (addr == CSR_MHPMCOUNTER11) | \
      (addr == CSR_MHPMCOUNTER12) | (addr == CSR_MHPMCOUNTER13) | (addr == CSR_MHPMCOUNTER14) | (addr == CSR_MHPMCOUNTER15) | \
      (addr == CSR_MHPMCOUNTER16) | (addr == CSR_MHPMCOUNTER17) | (addr == CSR_MHPMCOUNTER18) | (addr == CSR_MHPMCOUNTER19) | \
      (addr == CSR_MHPMCOUNTER20) | (addr == CSR_MHPMCOUNTER21) | (addr == CSR_MHPMCOUNTER22) | (addr == CSR_MHPMCOUNTER23) | \
      (addr == CSR_MHPMCOUNTER24) | (addr == CSR_MHPMCOUNTER25) | (addr == CSR_MHPMCOUNTER26) | (addr == CSR_MHPMCOUNTER27) | \
      (addr == CSR_MHPMCOUNTER28) | (addr == CSR_MHPMCOUNTER29) | (addr == CSR_MHPMCOUNTER30) | (addr == CSR_MHPMCOUNTER31) | \
      (addr == CSR_CYCLE) | \
      (addr == CSR_INSTRET) | \
      (addr == CSR_HPMCOUNTER3) | \
      (addr == CSR_HPMCOUNTER4) | (addr == CSR_HPMCOUNTER5) | (addr == CSR_HPMCOUNTER6) | (addr == CSR_HPMCOUNTER7) | \
      (addr == CSR_HPMCOUNTER8) | (addr == CSR_HPMCOUNTER9) |  (addr == CSR_HPMCOUNTER10) | (addr == CSR_HPMCOUNTER11) | \
      (addr == CSR_HPMCOUNTER12) | (addr == CSR_HPMCOUNTER13) | (addr == CSR_HPMCOUNTER14) | (addr == CSR_HPMCOUNTER15) | \
      (addr == CSR_HPMCOUNTER16) | (addr == CSR_HPMCOUNTER17) | (addr == CSR_HPMCOUNTER18) | (addr == CSR_HPMCOUNTER19) | \
      (addr == CSR_HPMCOUNTER20) | (addr == CSR_HPMCOUNTER21) | (addr == CSR_HPMCOUNTER22) | (addr == CSR_HPMCOUNTER23) | \
      (addr == CSR_HPMCOUNTER24) | (addr == CSR_HPMCOUNTER25) | (addr == CSR_HPMCOUNTER26) | (addr == CSR_HPMCOUNTER27) | \
      (addr == CSR_HPMCOUNTER28) | (addr == CSR_HPMCOUNTER29) | (addr == CSR_HPMCOUNTER30) | (addr == CSR_HPMCOUNTER31)


def hpmh(addr):
    return (addr == CSR_MCYCLEH) | \
      (addr == CSR_MINSTRETH) | \
      (addr == CSR_MHPMCOUNTER3H) | \
      (addr == CSR_MHPMCOUNTER4H) | (addr == CSR_MHPMCOUNTER5H) | (addr == CSR_MHPMCOUNTER6H) | (addr == CSR_MHPMCOUNTER7H) | \
      (addr == CSR_MHPMCOUNTER8H) | (addr == CSR_MHPMCOUNTER9H) | (addr == CSR_MHPMCOUNTER10H) | (addr == CSR_MHPMCOUNTER11H) | \
      (addr == CSR_MHPMCOUNTER12H) | (addr == CSR_MHPMCOUNTER13H) | (addr == CSR_MHPMCOUNTER14H) | (addr == CSR_MHPMCOUNTER15H) | \
      (addr == CSR_MHPMCOUNTER16H) | (addr == CSR_MHPMCOUNTER17H) | (addr == CSR_MHPMCOUNTER18H) | (addr == CSR_MHPMCOUNTER19H) | \
      (addr == CSR_MHPMCOUNTER20H) | (addr == CSR_MHPMCOUNTER21H) | (addr == CSR_MHPMCOUNTER22H) | (addr == CSR_MHPMCOUNTER23H) | \
      (addr == CSR_MHPMCOUNTER24H) | (addr == CSR_MHPMCOUNTER25H) | (addr == CSR_MHPMCOUNTER26H) | (addr == CSR_MHPMCOUNTER27H) | \
      (addr == CSR_MHPMCOUNTER28H) | (addr == CSR_MHPMCOUNTER29H) | (addr == CSR_MHPMCOUNTER30H) | (addr == CSR_MHPMCOUNTER31H) | \
      (addr == CSR_CYCLEH) | \
      (addr == CSR_INSTRETH) | \
      (addr == CSR_HPMCOUNTER3H) | \
      (addr == CSR_HPMCOUNTER4H) | (addr == CSR_HPMCOUNTER5H) | (addr == CSR_HPMCOUNTER6H) | (addr == CSR_HPMCOUNTER7H) | \
      (addr == CSR_HPMCOUNTER8H) | (addr == CSR_HPMCOUNTER9H) |  (addr == CSR_HPMCOUNTER10H) | (addr == CSR_HPMCOUNTER11H) | \
      (addr == CSR_HPMCOUNTER12H) | (addr == CSR_HPMCOUNTER13H) | (addr == CSR_HPMCOUNTER14H) | (addr == CSR_HPMCOUNTER15H) | \
      (addr == CSR_HPMCOUNTER16H) | (addr == CSR_HPMCOUNTER17H) | (addr == CSR_HPMCOUNTER18H) | (addr == CSR_HPMCOUNTER19H) | \
      (addr == CSR_HPMCOUNTER20H) | (addr == CSR_HPMCOUNTER21H) | (addr == CSR_HPMCOUNTER22H) | (addr == CSR_HPMCOUNTER23H) | \
      (addr == CSR_HPMCOUNTER24H) | (addr == CSR_HPMCOUNTER25H) | (addr == CSR_HPMCOUNTER26H) | (addr == CSR_HPMCOUNTER27H) | \
      (addr == CSR_HPMCOUNTER28H) | (addr == CSR_HPMCOUNTER29H) | (addr == CSR_HPMCOUNTER30H) | (addr == CSR_HPMCOUNTER31H)


def hpmevent(addr):
    return (addr == CSR_MHPMEVENT3) | \
           (addr == CSR_MHPMEVENT4) | (addr == CSR_MHPMEVENT5) | (addr == CSR_MHPMEVENT6) | (addr == CSR_MHPMEVENT7) | \
           (addr == CSR_MHPMEVENT8) | (addr == CSR_MHPMEVENT9) | (addr == CSR_MHPMEVENT10) | (addr == CSR_MHPMEVENT11) | \
           (addr == CSR_MHPMEVENT12) | (addr == CSR_MHPMEVENT13) | (addr == CSR_MHPMEVENT14) | (addr == CSR_MHPMEVENT15) | \
           (addr == CSR_MHPMEVENT16) | (addr == CSR_MHPMEVENT17) | (addr == CSR_MHPMEVENT18) | (addr == CSR_MHPMEVENT19) | \
           (addr == CSR_MHPMEVENT20) | (addr == CSR_MHPMEVENT21) | (addr == CSR_MHPMEVENT22) | (addr == CSR_MHPMEVENT23) | \
           (addr == CSR_MHPMEVENT24) | (addr == CSR_MHPMEVENT25) | (addr == CSR_MHPMEVENT26) | (addr == CSR_MHPMEVENT27) | \
           (addr == CSR_MHPMEVENT28) | (addr == CSR_MHPMEVENT29) | (addr == CSR_MHPMEVENT30) | (addr == CSR_MHPMEVENT31)


def cs_registers():
    # Local parameters
    NUM_HPM_EVENTS = 16

    MTVEC_MODE = U.w(2)(1)

    MAX_N_PMP_ENTRIES = 16
    MAX_N_PMP_CFG = 4
    N_PMP_CFG = int(MAX_N_PMP_ENTRIES / 4 if MAX_N_PMP_ENTRIES % 4 == 0 else MAX_N_PMP_ENTRIES / 4 + 1)

    MSTATUS_UIE_BIT = 0
    MSTATUS_SIE_BIT = 1
    MSTATUS_MIE_BIT = 3
    MSTATUS_UPIE_BIT = 4
    MSTATUS_SPIE_BIT = 5
    MSTATUS_MPIE_BIT = 7
    MSTATUS_SPP_BIT = 8
    MSTATUS_MPP_BIT_HIGH = 12
    MSTATUS_MPP_BIT_LOW = 11
    MSTATUS_MPRV_BIT = 17

    # MISA
    MXL = 1
    """
    MISA definition:
       bit      Character       Description
        0           A           Atomic extension
        2           C           Compressed extension
        3           D           Double-precision floating-point extension
        4           E           RV32E base ISA
        5           F           Single-precision floating-point extension
        8           I           RV32I ISA
        12          M           Integer Multiply/Divide extension
        13          N           User-level interrupts support
        18          S           Supervisor mode implement
        20          U           User mode implement
        23          X           Non-standard extensions present 
    """
    MISA_VALUE = \
        (0 << 0) \
        | (1 << 2) \
        | (0 << 3) \
        | (0 << 4) \
        | (0 << 5) \
        | (1 << 8) \
        | (1 << 12) \
        | (0 << 13) \
        | (0 << 18) \
        | (0 << 20) \
        | (0 << 23) \
        | (MXL << 30)

    MHPMCOUNTER_WIDTH = 64

    # This local parameter when set to 1 makes the Perf Counters not compliant with RISC-V
    # as it does not implement mcycle and minstret
    # but only HPMCOUNTERs (depending on NUM_MHPMCOUNTERS)
    PULP_PERF_COUNTERS = 0

    class Status_t:
        def __init__(self, q):
            """
                args:
                    q: bool, is it state elements.
            """
            if q:
                self.uie = RegInit(Bool(False))
                self.mie = RegInit(Bool(False))
                self.upie = RegInit(Bool(False))
                self.mpie = RegInit(Bool(False))
                self.mpp = RegInit(PRIV_LVL_M)
                self.mprv = RegInit(Bool(False))
            else:
                self.uie = Wire(Bool)
                self.mie = Wire(Bool)
                self.upie = Wire(Bool)
                self.mpie = Wire(Bool)
                self.mpp = Wire(U.w(PRIV_SEL_WIDTH))
                self.mprv = Wire(Bool)

        def __ilshift__(self, other):
            self.uie <<= other.uie
            self.mie <<= other.uie
            self.upie <<= other.upie
            self.mpie <<= other.mpie
            self.mpp <<= other.mpp
            self.mprv <<= other.mprv

        def clear(self):
            self.uie <<= U(0)
            self.mie <<= U(0)
            self.upie <<= U(0)
            self.mpie <<= U(0)
            self.mpp <<= U(0)
            self.mprv <<= U(0)

    class Dcsr_t:
        def __init__(self, q):
            """
                args:
                    q: bool, is it state elements.
            """
            if q:
                self.xdebugver = RegInit(XDEBUGVER_STD)
                self.zero2 = RegInit(U.w(10)(0))
                self.ebreakm = RegInit(Bool(False))
                self.zero1 = RegInit(Bool(False))
                self.ebreaks = RegInit(Bool(False))
                self.ebreaku = RegInit(Bool(False))
                self.stepie = RegInit(Bool(False))
                self.stopcount = RegInit(Bool(False))
                self.stoptime = RegInit(Bool(False))
                self.cause = RegInit(DBG_CAUSE_NONE)
                self.zero0 = RegInit(Bool(False))
                self.mprven = RegInit(Bool(False))
                self.nmip = RegInit(Bool(False))
                self.step = RegInit(Bool(False))
                self.prv = RegInit(PRIV_LVL_M)
            else:
                self.xdebugver = Wire(U.w(4))
                self.zero2 = Wire(U.w(10))
                self.ebreakm = Wire(Bool)
                self.zero1 = Wire(Bool)
                self.ebreaks = Wire(Bool)
                self.ebreaku = Wire(Bool)
                self.stepie = Wire(Bool)
                self.stopcount = Wire(Bool)
                self.stoptime = Wire(Bool)
                self.cause = Wire(U.w(3))
                self.zero0 = Wire(Bool)
                self.mprven = Wire(Bool)
                self.nmip = Wire(Bool)
                self.step = Wire(Bool)
                self.prv = Wire(U.w(PRIV_SEL_WIDTH))

        def __ilshift__(self, other):
            self.xdebugver <<= other.xdebugver
            self.zero2 <<= other.zero2
            self.ebreakm <<= other.ebreakm
            self.zero1 <<= other.zero1
            self.ebreaks <<= other.ebreaks
            self.ebreaku <<= other.ebreau
            self.stepie <<= other.stepie
            self.stopcount <<= other.stopcount
            self.stoptime <<= other.stoptime
            self.cause <<= other.cause
            self.zero0 <<= other.zero0
            self.mprven <<= other.mprven
            self.nmip <<= other.nmip
            self.step <<= other.step
            self.prv <<= other.prv

        def clear(self):
            self.xdebugver <<= U(0)
            self.zero2 <<= U(0)
            self.ebreakm <<= U(0)
            self.zero1 <<= U(0)
            self.ebreaks <<= U(0)
            self.ebreaku <<= U(0)
            self.stepie <<= U(0)
            self.stopcount <<= U(0)
            self.stoptime <<= U(0)
            self.cause <<= U(0)
            self.zero0 <<= U(0)
            self.mprven <<= U(0)
            self.nmip <<= U(0)
            self.step <<= U(0)
            self.prv <<= U(0)

    # In our implementation, we don't support PMP

    class CS_REGISTERS(Module):
        io = IO(
            # Hart ID
            hart_id_i=Input(U.w(32)),
            mtvec_o=Output(U.w(24)),
            utvec_o=Output(U.w(24)),
            mtvec_mode_o=Output(U.w(2)),
            utvec_mode_o=Output(U.w(2)),

            # Used for mtvec address
            mtvec_addr_i=Input(U.w(32)),
            csr_mtvec_init_i=Input(Bool),

            # Interface to registers (SRAM like)
            csr_addr_i=Input(U.w(CSR_NUM_WIDTH)),
            csr_wdata_i=Input(U.w(32)),
            csr_op_i=Input(U.w(CSR_OP_WIDTH)),
            csr_rdata_o=Output(U.w(32)),

            frm_o=Output(U.w(3)),
            fflags_i=Input(U.w(C_FFLAG)),
            fflags_we_i=Input(Bool),

            # Interrupts
            mie_bypass_o=Output(U.w(32)),
            mip_i=Input(U.w(32)),
            m_irq_enable_o=Output(Bool),
            u_irq_enable_o=Output(Bool),

            csr_irq_sec_i=Input(Bool),      # PULP_SECURE = 0 -> always 0
            sec_lvl_o=Output(Bool),
            mepc_o=Output(U.w(32)),
            uepc_o=Output(U.w(32)),
            mcounteren_o=Output(U.w(32)),   # PULP_SECURE = 0 -> always 0

            # Debug
            debug_mode_i=Input(Bool),
            debug_cause_i=Input(U.w(3)),
            debug_csr_save_i=Input(Bool),
            depc_o=Output(U.w(32)),
            debug_single_step_o=Output(Bool),
            debug_ebreakm_o=Output(Bool),
            debug_ebreaku_o=Output(Bool),
            trigger_match_o=Output(Bool),

            # pmp_addr_o and pmp_cfg_o are no used in our implementation
            priv_lvl_o=Output(U.w(PRIV_SEL_WIDTH)),

            pc_if_i=Input(U.w(32)),
            pc_id_i=Input(U.w(32)),
            pc_ex_i=Input(U.w(32)),

            csr_save_if_i=Input(Bool),
            csr_save_id_i=Input(Bool),
            csr_save_ex_i=Input(Bool),

            csr_restore_mret_i=Input(Bool),
            csr_restore_uret_i=Input(Bool),
            csr_restore_dret_i=Input(Bool),

            # Coming from controller
            csr_cause_i=Input(U.w(6)),
            csr_save_cause_i=Input(Bool),

            # Hardware loops are no used in our implementation

            # Performance Counters
            mhpmevent_minstret_i=Input(Bool),
            mhpmevent_load_i=Input(Bool),
            mhpmevent_store_i=Input(Bool),
            mhpmevent_jump_i=Input(Bool),               # Jump instruction retired (j, jr, jal, jalr)
            mhpmevent_branch_i=Input(Bool),             # Branch instruction retired (beq, bne, etc.)
            mhpmevent_branch_taken_i=Input(Bool),       # Branch instruction taken
            mhpmevent_compressed_i=Input(Bool),
            mhpmevent_jr_stall_i=Input(Bool),
            mhpmevent_imiss_i=Input(Bool),
            mhpmevent_ld_stall_i=Input(Bool),
            mhpmevent_pipe_stall_i=Input(Bool)

            # We don't support APU
        )
        # CSR update logic
        csr_wdata_int, csr_rdata_int = [Wire(U.w(32)) for _ in range(2)]
        csr_we_int = Wire(Bool)
        frm = gen_ff(C_RM, 0)
        fflags = gen_ff(C_FFLAG, 0)

        # Interrupt control signals
        mepc = gen_ff(32, 0)
        uepc = gen_ff(32, 0)

        # Trigger
        tmatch_control_rdata = Wire(U.w(32))
        tmatch_value_rdata = Wire(U.w(32))
        tinfo_types = Wire(U.w(16))

        # Debug
        dcsr = gen_packed_ff(Dcsr_t(True), Dcsr_t(False))
        depc = gen_ff(32, 0)
        dscratch0, dscratch1 = [gen_ff(32, 0) for _ in range(2)]
        mscratch = gen_ff(32, 0)

        exception_pc = Wire(U.w(32))
        mstatus = gen_packed_ff(Status_t(True), Status_t(False))
        mcause = gen_ff(6, 0)
        ucause = gen_ff(6, 0)
        mtvec = gen_ff(24, 0)
        utvec = gen_ff(24, 0)
        mtvec_mode = gen_ff(2, 1)       # MTVEC_MODE
        utvec_mode = gen_ff(2, 1)       # MTVEC_MODE

        mip = Wire(U.w(32))
        mie = gen_ff(32, 0)

        csr_mie_wdata = Wire(U.w(32))
        csr_mie_we = Wire(Bool)

        is_irq = Wire(Bool)
        priv_lvl = gen_ff(PRIV_SEL_WIDTH, 3)        # PRIV_LVL_M 0b11

        # No pmp support, ignore pmp_reg_q/n, pmpaddr_we, pmpcfg_we

        # Performance Counter Signals
        mhpmcounter_q = vec_init(32, U.w(MHPMCOUNTER_WIDTH), U(0))
        mhpmevent = gen_packed_ff(vec_init(32, U.w(32), U(0)), Wire(Vec(32, U.w(32))))
        mcounteren = gen_ff(32, 0)
        mcountinhibit = gen_ff(32, 0xFFFF)
        hpm_events = Wire(U.w(NUM_HPM_EVENTS))
        mhpmcounter_increment = Wire(Vec(32, U.w(MHPMCOUNTER_WIDTH)))
        mhpmcounter_write_lower = Wire(U.w(32))
        mhpmcounter_write_upper = Wire(U.w(32))
        mhpmcounter_write_increment = Wire(U.w(32))

        is_irq << io.csr_cause_i[5]

        # mip CSR
        mip <<= io.mip_i

        # mie_n is used instead of mie_q such that a CSR write to the MIE register can
        # affect the instruction immediately following it.

        # MIE CSR operation logic
        csr_mie_wdata <<= io.csr_wdata_i
        csr_mie_we <<= Bool(True)

        csr_mie_wdata <<= LookUpTable(io.csr_op_i, {
            CSR_OP_WRITE: io.csr_wdata_i,
            CSR_OP_SET: io.csr_wdata_i | mie.q,
            CSR_OP_CLEAR: (~io.csr_wdata_i) & mie.q,
            CSR_OP_READ: io.csr_wdata_i,
            ...: io.csr_wdata_i
        })

        csr_mie_we <<= Mux(io.csr_op_i == CSR_OP_READ, Bool(False), Bool(True))

        io.mie_bypass_o <<= Mux((io.csr_addr_i == CSR_MIE) & csr_mie_we, csr_mie_wdata & IRQ_MASK, mie.q)

        ##################################################################################
        # CSR Reg
        ##################################################################################
        # Generate no pulp secure read logic

        # case (csr_addr_i)
        with when((io.csr_addr_i == CSR_FFLAGS) | (io.csr_addr_i == CSR_FRM) | (io.csr_addr_i == CSR_FCSR)):
            csr_rdata_int <<= U(0)
        with elsewhen(io.csr_addr_i == CSR_MSTATUS):
            # mstatus: always M-mode, contains IE bit
            csr_rdata_int <<= CatBits(U.w(14)(0), mstatus.q.mprv, U.w(4)(0), mstatus.q.mpp, U.w(3)(0),
                                      mstatus.q.mpie, U.w(2)(0), mstatus.q.upie, mstatus.q.mie,
                                      U.w(2)(0), mstatus.q.uie)
        with elsewhen(io.csr_addr_i == CSR_MISA):
            # misa: machine isa register
            csr_rdata_int <<= U.w(32)(MISA_VALUE)
        with elsewhen(io.csr_addr_i == CSR_MIE):
            # mie: machine interrupt enable
            csr_rdata_int <<= mie.q

        with elsewhen(io.csr_addr_i == CSR_MTVEC):
            # mtvec: machine trap-handler base address
            csr_rdata_int <<= CatBits(mtvec.q, U.w(6)(0), mtvec_mode.q)
        with elsewhen(io.csr_addr_i == CSR_MSCRATCH):
            # mscratch: machine scratch
            csr_rdata_int <<= mscratch.q
        with elsewhen(io.csr_addr_i == CSR_MEPC):
            # mepc: exception program counter
            csr_rdata_int <<= mepc.q
        with elsewhen(io.csr_addr_i == CSR_MCAUSE):
            # mcause: exception cuase
            csr_rdata_int <<= CatBits(mcause.q[5], U.w(26)(0), mcause.q[4:0])
        with elsewhen(io.csr_addr_i == CSR_MIP):
            # mip: interrupt pending
            csr_rdata_int <<= mip
        with elsewhen(io.csr_addr_i == CSR_MHARTID):
            # mhartid: unique hardware thread id
            csr_rdata_int <<= io.hart_id_i
        with elsewhen(io.csr_addr_i == CSR_MVENDORID):
            # mvendorid: Machine Vendor ID
            csr_rdata_int <<= CatBits(MVENDORID_BANK, MVENDORID_OFFSET)
        with elsewhen(io.csr_addr_i == CSR_MARCHID):
            # marchid: Machine Architecture ID
            csr_rdata_int <<= MARCHID
        with elsewhen((io.csr_addr_i == CSR_MIMPID) | (io.csr_addr_i == CSR_MTVAL)):
            # Unimplemented
            csr_rdata_int <<= U(0)
        with elsewhen(io.csr_addr_i == CSR_MCOUNTEREN):
            # mcounteren: Machine Counter-Enable
            csr_rdata_int <<= mhpmcounter_q
        with elsewhen((io.csr_addr_i == CSR_TSELECT) | (io.csr_addr_i == CSR_TDATA3) |
                      (io.csr_addr_i == CSR_MCONTEXT) | (io.csr_addr_i == CSR_SCONTEXT)):
            csr_rdata_int <<= U(0)      # Always read 0
        with elsewhen(io.csr_addr_i == CSR_TDATA1):
            csr_rdata_int <<= tmatch_control_rdata
        with elsewhen(io.csr_addr_i == CSR_TDATA2):
            csr_rdata_int <<= tmatch_value_rdata
        with elsewhen(io.csr_addr_i == CSR_TINFO):
            csr_rdata_int <<= tinfo_types
        with elsewhen(io.csr_addr_i == CSR_DCSR):
            csr_rdata_int <<= dcsr.q
        with elsewhen(io.csr_addr_i == CSR_DPC):
            csr_rdata_int <<= depc.q
        with elsewhen(io.csr_addr_i == CSR_DSCRATCH0):
            csr_rdata_int <<= dscratch0.q
        with elsewhen(io.csr_addr_i == CSR_DSCRATCH1):
            csr_rdata_int <<= dscratch1.q
        with elsewhen(hpm(io.csr_addr_i)):
            csr_rdata_int <<= mhpmcounter_q[io.csr_addr_i[4:0]][31:0]
        with elsewhen(hpmh(io.csr_addr_i)):
            csr_rdata_int <<= mhpmcounter_q[io.csr_addr_i[4:0]][63:32]
        with elsewhen(io.csr_addr_i == CSR_MCOUNTINHIBIT):
            csr_rdata_int <<= mcountinhibit.q
        with elsewhen(hpmevent(io.csr_addr_i)):
            csr_rdata_int <<= mhpmevent.q[io.csr_addr_i[4:0]]
        # No hardware loops and PMP config support

        # No user CSRs implement (PULP_XPULP | PULP_SECURE == 0)
        with otherwise():
            # Default
            csr_rdata_int <<= U(0)

        # Generate no pulp secure write logic
        fflags.n <<= fflags.q
        frm.n <<= frm.q
        mscratch.n <<= mscratch.q
        mepc.n <<= mepc.q
        uepc.n <<= U(0)
        depc.n <<= depc.q
        dcsr.n <<= dcsr.q
        dscratch0.n <<= dscratch0.q
        dscratch1.n <<= dscratch1.q

        mstatus.n <<= mstatus.q
        mcause.n <<= mcause.q
        ucause.n.clear()
        exception_pc <<= io.pc_id_i
        priv_lvl.n <<= priv_lvl.q
        mtvec.n <<= Mux(io.csr_mtvec_init_i, io.mtvec_addr_i[31:8], mtvec.q)
        utvec.n <<= U(0)

        mie.n <<= mie.q
        mtvec_mode.n <<= mtvec_mode.q
        utvec_mode.n.clear()

        # case (csr_addr_i)

    return CS_REGISTERS()
