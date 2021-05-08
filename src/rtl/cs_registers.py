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


def cs_registers(NUM_MHPMCOUNTERS=1):
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

        with when(io.csr_addr_i == CSR_FFLAGS):
            with when(csr_we_int):
                fflags.n <<= U(0)
        with elsewhen(io.csr_addr_i == CSR_FRM):
            with when(csr_we_int):
                frm.n <<= U(0)
        with elsewhen(io.csr_addr_i == CSR_FCSR):
            fflags.n <<= U(0)
            frm.n <<= U(0)

        # mstatus: IE bit
        with elsewhen(io.csr_addr_i == CSR_MSTATUS):
            with when(csr_we_int):
                mstatus.n.uie <<= csr_wdata_int[MSTATUS_UIE_BIT]
                mstatus.n.mie <<= csr_wdata_int[MSTATUS_MIE_BIT]
                mstatus.n.upie <<= csr_wdata_int[MSTATUS_UPIE_BIT]
                mstatus.n.mpie <<= csr_wdata_int[MSTATUS_MPIE_BIT]
                mstatus.n.mpp <<= csr_wdata_int[MSTATUS_MPP_BIT_HIGH:MSTATUS_MPP_BIT_LOW]
                mstatus.n.mprv <<= csr_wdata_int[MSTATUS_MPRV_BIT]

        # mie: machine interrupt enable
        with elsewhen(io.csr_addr_i == CSR_MIE):
            with when(csr_we_int):
                mie.n <<= csr_wdata_int & IRQ_MASK
        # mtvec: machine trap-handler base address
        with elsewhen(io.csr_addr_i == CSR_MTVEC):
            with when(csr_we_int):
                mtvec.n <<= csr_wdata_int[31:8]
                mtvec_mode.n <<= CatBits(U.w(1)(0), csr_wdata_int[0])
        # mscratch: machine scratch
        with elsewhen(io.csr_addr_i == CSR_MSCRATCH):
            with when(csr_we_int):
                mscratch.n <<= csr_wdata_int
        # mepc: exception program counter
        with elsewhen(io.csr_addr_i == CSR_MEPC):
            with when(csr_we_int):
                mepc.n <<= csr_wdata_int & (~U.w(32)(1))
        # mcause
        with elsewhen(io.csr_addr_i == CSR_MCAUSE):
            with when(csr_we_int):
                mcause.n <<= CatBits(csr_wdata_int[31], csr_wdata_int[4:0])

        with elsewhen(io.csr_addr_i == CSR_DCSR):
            with when(csr_we_int):
                # Following are read-only and never assigned here (dcsr_q value is used)
                #
                # - xdebugver
                # - cause
                # - nmip
                dcsr.n.ebreakm   <<= csr_wdata_int[15]
                dcsr.n.ebreaks   <<= U(0)                   # ebreaks (implemented as WARL)
                dcsr.n.ebreaku   <<= U(0)                   # ebreaku (implemented as WARL)
                dcsr.n.stepie    <<= csr_wdata_int[11]      # stepie
                dcsr.n.stopcount <<= U(0)                   # stopcount
                dcsr.n.stoptime  <<= U(0)                   # stoptime
                dcsr.n.mprven    <<= U(0)                   # mprven
                dcsr.n.step      <<= csr_wdata_int[2]
                dcsr.n.prv       <<= PRIV_LVL_M             # prv (implemented as WARL)

        with elsewhen(io.csr_addr_i == CSR_DPC):
            with when(csr_we_int):
                depc.n <<= csr_wdata_int & (~U.w(32)(1))

        with elsewhen(io.csr_addr_i == CSR_DSCRATCH0):
            with when(csr_we_int):
                dscratch0.n <<= csr_wdata_int

        with elsewhen(io.csr_addr_i == CSR_DSCRATCH1):
            with when(csr_we_int):
                dscratch1.n <<= csr_wdata_int

        # No hardware loops support
        with otherwise():
            pass

        # Exception controller gets priority over other writes
        with when(io.csr_save_cause_i):
            with when(io.csr_save_if_i):
                exception_pc <<= io.pc_if_i
            with elsewhen(io.csr_save_id_i):
                exception_pc <<= io.pc_id_i
            with elsewhen(io.csr_save_ex_i):
                exception_pc <<= io.pc_ex_i

            with when(io.debug_csr_save_i):
                # All interrupts are masked, don't update cause, epc, tval dpc and mpstatus
                dcsr.n.prv <<= PRIV_LVL_M
                dcsr.n.cause <<= io.debug_cause_i
                depc.n <<= exception_pc
            with otherwise():
                priv_lvl.n <<= PRIV_LVL_M
                mstatus.n.mpie <<= mstatus.q.mie
                mstatus.n.mie <<= U(0)
                mstatus.n.mpp <<= PRIV_LVL_M
                mepc.n <<= exception_pc
                mcause.n <<= io.csr_cause_i

        with elsewhen(io.csr_restore_mret_i):
            mstatus.n.mie <<= mstatus.q.mpie
            priv_lvl.n <<= PRIV_LVL_M
            mstatus.n.mpie <<= U(1)
            mstatus.n.mpp <<= PRIV_LVL_M

        with elsewhen(io.csr_restore_dret_i):
            priv_lvl.n <<= dcsr.q.prv

        # CSR operation logic
        csr_wdata_int <<= io.csr_wdata_i
        csr_we_int <<= U.w(1)(1)

        csr_wdata_int <<= LookUpTable(io.csr_op_i, {
            CSR_OP_WRITE: io.csr_wdata_i,
            CSR_OP_SET: io.csr_wdata_i | io.csr_rdata_o,
            CSR_OP_CLEAR: (~io.csr_wdata_i) & io.csr_rdata_o,
            CSR_OP_READ: io.csr_wdata_i
        })

        with when(io.csr_op_i == CSR_OP_READ):
            csr_we_int <<= U.w(1)(0)

        io.csr_rdata_o <<= csr_rdata_int

        # Directly output some registers
        io.m_irq_enable_o <<= mstatus.q.mie & (~(dcsr.q.step & (~dcsr.q.stepie)))
        io.u_irq_enable_o <<= mstatus.q.uie & (~(dcsr.q.step & (~dcsr.q.stepie)))
        io.priv_lvl_o <<= priv_lvl.q
        io.sec_lvl_o <<= priv_lvl.q[0]
        io.frm_o <<= U(0)

        io.mtvec_o <<= mtvec.q
        io.utvec_o <<= utvec.q
        io.mtvec_mode_o <<= mtvec_mode.q
        io.utvec_mode_o <<= utvec_mode.q

        io.mepc_o <<= mepc.q
        io.uepc_o <<= uepc.q

        io.mcounteren_o <<= U(0)

        io.depc_o <<= depc.q

        io.debug_single_step_o <<= dcsr.q.step
        io.debug_ebreakm_o <<= dcsr.q.ebreakm
        io.debug_ebreaku_o <<= dcsr.q.ebreaku

        uepc.q <<= U(0)
        ucause.q <<= U(0)
        utvec.q <<= U(0)
        utvec_mode.q <<= U(0)
        priv_lvl.q <<= PRIV_LVL_M

        # Update CSRs
        frm.q <<= U(0)
        fflags.q <<= U(0)

        mstatus.q.uie <<= U(0)
        mstatus.q.mie <<= mstatus.n.mie
        mstatus.q.upie <<= U(0)
        mstatus.q.mpie <<= mstatus.n.mpie
        mstatus.q.mpp <<= PRIV_LVL_M
        mstatus.q.mprv <<= U(0)

        mepc.q <<= mepc.n
        mcause.q <<= mcause.n
        depc.q <<= depc.n
        dcsr.q <<= dcsr.n
        dscratch0.q <<= dscratch0.n
        dscratch1.q <<= dscratch1.n
        mscratch.q <<= mscratch.n
        mie.q <<= mie.n
        mtvec.q <<= mtvec.n
        mtvec_mode.q <<= mtvec_mode.n

        ##################################################################################
        # Debug Trigger
        ##################################################################################
        # Register values
        tmatch_control_exec_q = RegInit(Bool(False))
        tmatch_value_q = RegInit(U.w(32)(0))
        # Write enables
        tmatch_control_we = Wire(Bool)
        tmatch_value_we = Wire(Bool)

        # Write select
        tmatch_control_we <<= csr_we_int & io.debug_mode_i & (io.csr_addr_i == CSR_TDATA1)
        tmatch_value_we <<= csr_we_int & io.debug_mode_i & (io.csr_addr_i == CSR_TDATA2)

        # Registers
        with when(tmatch_control_we):
            tmatch_control_exec_q <<= csr_wdata_int[2]
        with when(tmatch_value_we):
            tmatch_value_q <<= csr_wdata_int[31:0]

        # All supported trigger types
        tinfo_types <<= 1 << TTYPE_MCONTROL

        # Assign read data
        # TDATA0 - only support simple address matching
        tmatch_control_rdata <<= CatBits(
            TTYPE_MCONTROL,                 # type      : address/data match
            U.w(1)(1),                      # dmode     : access from D mode only
            U.w(6)(0x00),                   # maskmax   : exact match only
            U.w(1)(0),                      # hit       : not supported
            U.w(1)(0),                      # select    : address match only
            U.w(1)(0),                      # timing    : match before execution
            U.w(2)(0),                      # sizelo    : match any access
            U.w(4)(0x1),                    # action    : enter debug mode
            U.w(1)(0),                      # chain     : not supported
            U.w(4)(0x0),                    # match     : simple match
            U.w(1)(1),                      # m         : match in m-mode
            U.w(1)(0),                      # 0         : zero
            U.w(1)(0),                      # s         : not supported
            U.w(1)(0),                      # u         : match in u-mode
            tmatch_control_exec_q,          # execute   : match in instruction address
            U.w(1)(0),                      # store     : not supported
            U.w(1)(0)                       # load      : not supported
        )

        # TDATA1 - address match value only
        tmatch_value_rdata <<= tmatch_value_q

        # Breakpoint matching
        # We match against the next address, as the breakpoint must be taken before execution
        io.trigger_match_o <<= tmatch_control_exec_q & (io.pc_id_i[31:0] == tmatch_value_q[31:0])

        ##################################################################################
        # Perf. Counter
        ##################################################################################

        # -----------------------------
        # Events to count
        hpm_events <<= CatBits(
            U.w(1)(1),                                  # cycle counter
            io.mhpmevent_minstret_i,                    # instruction counter
            io.mhpmevent_ld_stall_i,                    # nr of load use hazards
            io.mhpmevent_jr_stall_i,                    # nr of jump register hazards
            io.mhpmevent_imiss_i,                       # cycles waiting for instruction fetches, excluding jumps and branches
            io.mhpmevent_load_i,                        # nr of loads
            io.mhpmevent_store_i,                       # nr of stores
            io.mhpmevent_jump_i,                        # nr of jumps (unconditional)
            io.mhpmevent_branch_i,                      # nr of branches (conditional)
            io.mhpmevent_branch_taken_i,                # nr of taken branches (conditional)
            io.mhpmevent_compressed_i,                  # compressed instruction counter
            U.w(5)(0)
        )

        # -----------------------------
        # address decoder for performance counter registers
        mcounteren_we, mcountinhibit_we, mhpmevent_we = [Wire(Bool) for _ in range(3)]
        mcounteren_we       <<= csr_we_int & (  io.csr_addr_i == CSR_MCOUNTEREN)
        mcountinhibit_we    <<= csr_we_int & (  io.csr_addr_i == CSR_MCOUNTINHIBIT)
        mhpmevent_we        <<= csr_we_int & ( (io.csr_addr_i == CSR_MHPMEVENT3  ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT4  ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT5  ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT6  ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT7  ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT8  ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT9  ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT10 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT11 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT12 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT13 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT14 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT15 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT16 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT17 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT18 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT19 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT20 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT21 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT22 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT23 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT24 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT25 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT26 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT27 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT28 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT29 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT30 ) |
                                               (io.csr_addr_i == CSR_MHPMEVENT31 ))
        # -----------------------------
        # Increment value for performance counters
        for incr_gidx in range(32):
            mhpmcounter_increment[incr_gidx] <<= mhpmcounter_q[incr_gidx] + U(1)

        # -----------------------------
        # next value for performance counters and control regsiters
        mcounteren.n <<= mcounteren.q
        mcountinhibit.n <<= mcountinhibit.q
        mhpmevent.n <<= mhpmevent.q

        # No user mode enable

        # Inhibit Control
        with when(mcountinhibit_we):
            mcountinhibit.n <<= csr_wdata_int

        # Event Control
        with when(mhpmevent_we):
            mhpmevent.n[io.csr_addr_i[4:0]] <<= csr_wdata_int

        mhpmcounter_write_lower_arr = [Wire(Bool) for _ in range(32)]
        mhpmcounter_write_upper_arr = [Wire(Bool) for _ in range(32)]
        mhpmcounter_write_increment_arr = [Wire(Bool) for _ in range(32)]

        for wcnt_gidx in range(32):
            # Write lower counter bits
            mhpmcounter_write_lower_arr[wcnt_gidx] <<= csr_we_int & (io.csr_addr_i == (CSR_MCYCLE + U(wcnt_gidx)))
            mhpmcounter_write_lower <<= CatBits(*mhpmcounter_write_lower_arr)

            # Write upper counter bits
            mhpmcounter_write_upper_arr[wcnt_gidx] <<= (~mhpmcounter_write_lower[wcnt_gidx]) & csr_we_int & (io.csr_addr_i == (CSR_MCYCLEH + wcnt_gidx))
            mhpmcounter_write_upper <<= CatBits(*mhpmcounter_write_upper_arr)

            if wcnt_gidx == 0:
                # mcycle = mhpmcounter[0] : count every cycle (if not inhibited)
                mhpmcounter_write_increment_arr[wcnt_gidx] <<= (~mhpmcounter_write_lower[wcnt_gidx]) & \
                                                               (~mhpmcounter_write_upper[wcnt_gidx]) & \
                                                               (~mcountinhibit.q[wcnt_gidx])
            elif wcnt_gidx == 2:
                # minstret = mhpmcounter[2] : count every retired instruction (if not inhibited)
                mhpmcounter_write_increment_arr[wcnt_gidx] <<= (~mhpmcounter_write_lower[wcnt_gidx]) & \
                                                               (~mhpmcounter_write_upper[wcnt_gidx]) & \
                                                               (~mcountinhibit.q[wcnt_gidx]) & \
                                                               hpm_events[1]
            elif 2 < wcnt_gidx < (NUM_MHPMCOUNTERS + 3):
                reduce_tmp = hpm_events & mhpmevent.q[wcnt_gidx][NUM_HPM_EVENTS-1:0]
                reduce_res = Wire(Bool)
                reduce_res <<= reduce_tmp[NUM_HPM_EVENTS-1]
                for i in range(NUM_HPM_EVENTS-2, -1, -1):
                    reduce_res <<= reduce_res | reduce_tmp[i]
                mhpmcounter_write_increment_arr[wcnt_gidx] <<= (~mhpmcounter_write_lower[wcnt_gidx]) & \
                                                               (~mhpmcounter_write_upper[wcnt_gidx]) & \
                                                               (~mcountinhibit.q[wcnt_gidx]) & reduce_res
            else:
                mhpmcounter_write_increment_arr[wcnt_gidx] <<= Bool(False)

            mhpmcounter_write_increment <<= CatBits(*mhpmcounter_write_increment_arr)

        # -----------------------------
        # HPM Registers
        #   Counter Registers: mhpcounter_q[]
        for cnt_gidx in range(32):
            # mcyclce  is located at index 0
            # there is no counter at index 1
            # minstret is located at index 2
            # Programable HPM counters start at index 3
            if cnt_gidx == 1 or cnt_gidx >= (NUM_MHPMCOUNTERS + 3):
                mhpmcounter_q[cnt_gidx] <<= U(0)
            else:
                with when(mhpmcounter_write_lower[cnt_gidx]):
                    mhpmcounter_q[cnt_gidx][31:0] <<= csr_wdata_int
                with elsewhen(mhpmcounter_write_upper[cnt_gidx]):
                    mhpmcounter_q[cnt_gidx][63:32] <<= csr_wdata_int
                with elsewhen(mhpmcounter_write_increment[cnt_gidx]):
                    mhpmcounter_q[cnt_gidx] <<= mhpmcounter_increment[cnt_gidx]

        #   Event Register: mhpevent_q[]
        for evt_gidx in range(32):
            # programable HPM events start at index3
            if evt_gidx < 3 or evt_gidx >= (NUM_MHPMCOUNTERS + 3):
                mhpmevent.q[evt_gidx] <<= U(0)
            else:
                if NUM_HPM_EVENTS < 32:
                    mhpmevent.q[evt_gidx][31:NUM_HPM_EVENTS] <<= U(0)
                mhpmevent.q[evt_gidx][NUM_HPM_EVENTS-1:0] <<= mhpmevent.n[evt_gidx][NUM_HPM_EVENTS-1:0]

        #   Enable Register: mcounteren_q
        #   Not implement
        for en_gidx in range(32):
            mcounteren.q[en_gidx] <<= U(0)

        #   Inhibit Register: mcountinhibit_q
        #   Note: implemented ocunters are disabled out of reset to save power
        for inh_gidx in range(32):
            if inh_gidx == 1 or inh_gidx >= (NUM_MHPMCOUNTERS + 3):
                mcountinhibit.q[inh_gidx] <<= U(0)
            else:
                mcountinhibit.q[inh_gidx] <<= mcountinhibit.n[inh_gidx]

    return CS_REGISTERS()
