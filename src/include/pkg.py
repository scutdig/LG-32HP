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
   Date: 2021-03-01
   File Name: pkg.py
   Description: Constants used by the processor core.
"""
from pyhcl import *
from enum import Enum

##################################################################################
# Prefetch controller state (for FSM)
##################################################################################
PState_IDLE = U.w(1)(0)
PState_BRANCH_WAIT = U.w(1)(1)


##################################################################################
# OpCodes
##################################################################################
OPCODE_SYSTEM    = U.w(7)(0x73)
OPCODE_FENCE     = U.w(7)(0x0f)
OPCODE_OP        = U.w(7)(0x33)
OPCODE_OPIMM     = U.w(7)(0x13)
OPCODE_STORE     = U.w(7)(0x23)
OPCODE_LOAD      = U.w(7)(0x03)
OPCODE_BRANCH    = U.w(7)(0x63)
OPCODE_JALR      = U.w(7)(0x67)
OPCODE_JAL       = U.w(7)(0x6f)
OPCODE_AUIPC     = U.w(7)(0x17)
OPCODE_LUI       = U.w(7)(0x37)
OPCODE_OP_FP     = U.w(7)(0x53)
OPCODE_OP_FMADD  = U.w(7)(0x43)
OPCODE_OP_FNMADD = U.w(7)(0x4f)
OPCODE_OP_FMSUB  = U.w(7)(0x47)
OPCODE_OP_FNMSUB = U.w(7)(0x4b)
OPCODE_STORE_FP  = U.w(7)(0x27)
OPCODE_LOAD_FP   = U.w(7)(0x07)
OPCODE_AMO       = U.w(7)(0x2f)
OPCODE_PULP_OP   = U.w(7)(0x5b)
OPCODE_VECOP     = U.w(7)(0x57)
OPCODE_HWLOOP    = U.w(7)(0x7b)

##################################################################################
# ALU Operations
##################################################################################
ALU_OP_WIDTH = 7

# Enum logic
ALU_ADD   = U.w(7)(0b0011000)
ALU_SUB   = U.w(7)(0b0011001)
ALU_ADDU  = U.w(7)(0b0011010)
ALU_SUBU  = U.w(7)(0b0011011)
ALU_ADDR  = U.w(7)(0b0011100)
ALU_SUBR  = U.w(7)(0b0011101)
ALU_ADDUR = U.w(7)(0b0011110)
ALU_SUBUR = U.w(7)(0b0011111)

ALU_XOR   = U.w(7)(0b0101111)
ALU_OR    = U.w(7)(0b0101110)
ALU_AND   = U.w(7)(0b0010101)

#  Shifts
ALU_SRA   = U.w(7)(0b0100100)
ALU_SRL   = U.w(7)(0b0100101)
ALU_ROR   = U.w(7)(0b0100110)
ALU_SLL   = U.w(7)(0b0100111)

#  bit manipulation
ALU_BEXT  = U.w(7)(0b0101000)
ALU_BEXTU = U.w(7)(0b0101001)
ALU_BINS  = U.w(7)(0b0101010)
ALU_BCLR  = U.w(7)(0b0101011)
ALU_BSET  = U.w(7)(0b0101100)
ALU_BREV  = U.w(7)(0b1001001)

#  Bit counting
ALU_FF1   = U.w(7)(0b0110110)
ALU_FL1   = U.w(7)(0b0110111)
ALU_CNT   = U.w(7)(0b0110100)
ALU_CLB   = U.w(7)(0b0110101)

#  Sign-/zero-extensions
ALU_EXTS  = U.w(7)(0b0111110)
ALU_EXT   = U.w(7)(0b0111111)

#  Comparisons
ALU_LTS   = U.w(7)(0b0000000)
ALU_LTU   = U.w(7)(0b0000001)
ALU_LES   = U.w(7)(0b0000100)
ALU_LEU   = U.w(7)(0b0000101)
ALU_GTS   = U.w(7)(0b0001000)
ALU_GTU   = U.w(7)(0b0001001)
ALU_GES   = U.w(7)(0b0001010)
ALU_GEU   = U.w(7)(0b0001011)
ALU_EQ    = U.w(7)(0b0001100)
ALU_NE    = U.w(7)(0b0001101)

#  Set Lower Than operations
ALU_SLTS  = U.w(7)(0b0000010)
ALU_SLTU  = U.w(7)(0b0000011)
ALU_SLETS = U.w(7)(0b0000110)
ALU_SLETU = U.w(7)(0b0000111)

#  Absolute value
ALU_ABS   = U.w(7)(0b0010100)
ALU_CLIP  = U.w(7)(0b0010110)
ALU_CLIPU = U.w(7)(0b0010111)

#  Insert/extract
ALU_INS   = U.w(7)(0b0101101)

#  min/max
ALU_MIN   = U.w(7)(0b0010000)
ALU_MINU  = U.w(7)(0b0010001)
ALU_MAX   = U.w(7)(0b0010010)
ALU_MAXU  = U.w(7)(0b0010011)

#  div/rem
ALU_DIVU  = U.w(7)(0b0110000)  # bit 0 is used for signed mode, bit 1 is used for remdiv
ALU_DIV   = U.w(7)(0b0110001)  # bit 0 is used for signed mode, bit 1 is used for remdiv
ALU_REMU  = U.w(7)(0b0110010)  # bit 0 is used for signed mode, bit 1 is used for remdiv
ALU_REM   = U.w(7)(0b0110011)  # bit 0 is used for signed mode, bit 1 is used for remdiv

ALU_SHUF  = U.w(7)(0b0111010)
ALU_SHUF2 = U.w(7)(0b0111011)
ALU_PCKLO = U.w(7)(0b0111000)
ALU_PCKHI = U.w(7)(0b0111001)

MUL_OP_WIDTH = 3

# mul_opcode_e
MUL_MAC32 = U.w(3)(0b000)
MUL_MSU32 = U.w(3)(0b001)
MUL_I     = U.w(3)(0b010)
MUL_IR    = U.w(3)(0b011)
MUL_DOT8  = U.w(3)(0b100)
MUL_DOT16 = U.w(3)(0b101)
MUL_H     = U.w(3)(0b110)

##################################################################################
# CSR operations
##################################################################################
CSR_OP_WIDTH = 2

# csr_opcode_e
CSR_OP_READ  = U.w(2)(0b00)
CSR_OP_WRITE = U.w(2)(0b01)
CSR_OP_SET   = U.w(2)(0b10)
CSR_OP_CLEAR = U.w(2)(0b11)

##################################################################################
# Privileged mode
##################################################################################
PRIV_SEL_WIDTH = 2

# PrivLvl_t
PRIV_LVL_M = U.w(2)(0b11)
PRIV_LVL_H = U.w(2)(0b10)
PRIV_LVL_S = U.w(2)(0b01)
PRIV_LVL_U = U.w(2)(0b00)

##################################################################################
# ID Stage
##################################################################################
# forwarding operand mux
SEL_REGFILE      = U.w(2)(0b00)
SEL_FW_EX        = U.w(2)(0b01)
SEL_FW_WB        = U.w(2)(0b10)

# operand a selection
OP_A_REGA_OR_FWD = U.w(3)(0b000)
OP_A_CURRPC      = U.w(3)(0b001)
OP_A_IMM         = U.w(3)(0b010)
OP_A_REGB_OR_FWD = U.w(3)(0b011)
OP_A_REGC_OR_FWD = U.w(3)(0b100)

# immediate a selection
IMMA_Z      = U.w(1)(0b0)
IMMA_ZERO   = U.w(1)(0b1)

# operand b selection
OP_B_REGB_OR_FWD = U.w(3)(0b000)
OP_B_REGC_OR_FWD = U.w(3)(0b001)
OP_B_IMM         = U.w(3)(0b010)
OP_B_REGA_OR_FWD = U.w(3)(0b011)
OP_B_BMASK       = U.w(3)(0b100)

# immediate b selection
IMMB_I      = U.w(4)(0b0000)
IMMB_S      = U.w(4)(0b0001)
IMMB_U      = U.w(4)(0b0010)
IMMB_PCINCR = U.w(4)(0b0011)
IMMB_S2     = U.w(4)(0b0100)
IMMB_S3     = U.w(4)(0b0101)
IMMB_VS     = U.w(4)(0b0110)
IMMB_VU     = U.w(4)(0b0111)
IMMB_SHUF   = U.w(4)(0b1000)
IMMB_CLIP   = U.w(4)(0b1001)
IMMB_BI     = U.w(4)(0b1011)

# multiplication immediates
MIMM_ZERO    = U.w(1)(0b0)
MIMM_S3      = U.w(1)(0b1)

# operand c selection
OP_C_REGC_OR_FWD = U.w(2)(0b00)
OP_C_REGB_OR_FWD = U.w(2)(0b01)
OP_C_JT          = U.w(2)(0b10)

# branch types
BRANCH_NONE = U.w(2)(0b00)
BRANCH_JAL  = U.w(2)(0b01)
BRANCH_JALR = U.w(2)(0b10)
BRANCH_COND = U.w(2)(0b11)  # conditional branches

# jump target mux
JT_JAL  = U.w(2)(0b01)
JT_JALR = U.w(2)(0b10)
JT_COND = U.w(2)(0b11)

# RegC Mux Selection
REGC_S1 = U.w(2)(0b10)
REGC_S4 = U.w(2)(0b00)
REGC_RD = U.w(2)(0b01)
REGC_ZERO = U.w(2)(0b11)

##################################################################################
# CSRs
##################################################################################
# User CSRs


# User trap setup
CSR_USTATUS        = U.w(12)(0x000)         # Not included (PULP_SECURE = 0)

# Floating Point
CSR_FFLAGS         = U.w(12)(0x001)         # Included if FPU = 1
CSR_FRM            = U.w(12)(0x002)         # Included if FPU = 1
CSR_FCSR           = U.w(12)(0x003)         # Included if FPU = 1

# User trap setup
CSR_UTVEC          = U.w(12)(0x005)         # Not included (PULP_SECURE = 0)

# User trap handling
CSR_UEPC           = U.w(12)(0x041)         # Not included (PULP_SECURE = 0)
CSR_UCAUSE         = U.w(12)(0x042)         # Not included (PULP_SECURE = 0)


# User Custom CSRs


# Hardware Loop
CSR_LPSTART0       = U.w(12)(0x800)         # Custom CSR. Included if PULP_HWLP = 1
CSR_LPEND0         = U.w(12)(0x801)         # Custom CSR. Included if PULP_HWLP = 1
CSR_LPCOUNT0       = U.w(12)(0x802)         # Custom CSR. Included if PULP_HWLP = 1
CSR_LPSTART1       = U.w(12)(0x804)         # Custom CSR. Included if PULP_HWLP = 1
CSR_LPEND1         = U.w(12)(0x805)         # Custom CSR. Included if PULP_HWLP = 1
CSR_LPCOUNT1       = U.w(12)(0x806)         # Custom CSR. Included if PULP_HWLP = 1

# User Hart ID
CSR_UHARTID        = U.w(12)(0xCC0)         # Custom CSR. User Hart ID

# Privilege
CSR_PRIVLV         = U.w(12)(0xCC1)         # Custom CSR. Privilege Level


# Machine CSRs


# Machine trap setup
CSR_MSTATUS        = U.w(12)(0x300)
CSR_MISA           = U.w(12)(0x301)
CSR_MIE            = U.w(12)(0x304)
CSR_MTVEC          = U.w(12)(0x305)

# Performance counters
CSR_MCOUNTEREN     = U.w(12)(0x306)
CSR_MCOUNTINHIBIT  = U.w(12)(0x320)
CSR_MHPMEVENT3     = U.w(12)(0x323)
CSR_MHPMEVENT4     = U.w(12)(0x324)
CSR_MHPMEVENT5     = U.w(12)(0x325)
CSR_MHPMEVENT6     = U.w(12)(0x326)
CSR_MHPMEVENT7     = U.w(12)(0x327)
CSR_MHPMEVENT8     = U.w(12)(0x328)
CSR_MHPMEVENT9     = U.w(12)(0x329)
CSR_MHPMEVENT10    = U.w(12)(0x32A)
CSR_MHPMEVENT11    = U.w(12)(0x32B)
CSR_MHPMEVENT12    = U.w(12)(0x32C)
CSR_MHPMEVENT13    = U.w(12)(0x32D)
CSR_MHPMEVENT14    = U.w(12)(0x32E)
CSR_MHPMEVENT15    = U.w(12)(0x32F)
CSR_MHPMEVENT16    = U.w(12)(0x330)
CSR_MHPMEVENT17    = U.w(12)(0x331)
CSR_MHPMEVENT18    = U.w(12)(0x332)
CSR_MHPMEVENT19    = U.w(12)(0x333)
CSR_MHPMEVENT20    = U.w(12)(0x334)
CSR_MHPMEVENT21    = U.w(12)(0x335)
CSR_MHPMEVENT22    = U.w(12)(0x336)
CSR_MHPMEVENT23    = U.w(12)(0x337)
CSR_MHPMEVENT24    = U.w(12)(0x338)
CSR_MHPMEVENT25    = U.w(12)(0x339)
CSR_MHPMEVENT26    = U.w(12)(0x33A)
CSR_MHPMEVENT27    = U.w(12)(0x33B)
CSR_MHPMEVENT28    = U.w(12)(0x33C)
CSR_MHPMEVENT29    = U.w(12)(0x33D)
CSR_MHPMEVENT30    = U.w(12)(0x33E)
CSR_MHPMEVENT31    = U.w(12)(0x33F)

# Machine trap handling
CSR_MSCRATCH       = U.w(12)(0x340)
CSR_MEPC           = U.w(12)(0x341)
CSR_MCAUSE         = U.w(12)(0x342)
CSR_MTVAL          = U.w(12)(0x343)
CSR_MIP            = U.w(12)(0x344)

# Physical memory protection (PMP)
CSR_PMPCFG0        = U.w(12)(0x3A0)         # Not included (USE_PMP = 0)
CSR_PMPCFG1        = U.w(12)(0x3A1)         # Not included (USE_PMP = 0)
CSR_PMPCFG2        = U.w(12)(0x3A2)         # Not included (USE_PMP = 0)
CSR_PMPCFG3        = U.w(12)(0x3A3)         # Not included (USE_PMP = 0)
CSR_PMPADDR0       = U.w(12)(0x3B0)         # Not included (USE_PMP = 0)
CSR_PMPADDR1       = U.w(12)(0x3B1)         # Not included (USE_PMP = 0)
CSR_PMPADDR2       = U.w(12)(0x3B2)         # Not included (USE_PMP = 0)
CSR_PMPADDR3       = U.w(12)(0x3B3)         # Not included (USE_PMP = 0)
CSR_PMPADDR4       = U.w(12)(0x3B4)         # Not included (USE_PMP = 0)
CSR_PMPADDR5       = U.w(12)(0x3B5)         # Not included (USE_PMP = 0)
CSR_PMPADDR6       = U.w(12)(0x3B6)         # Not included (USE_PMP = 0)
CSR_PMPADDR7       = U.w(12)(0x3B7)         # Not included (USE_PMP = 0)
CSR_PMPADDR8       = U.w(12)(0x3B8)         # Not included (USE_PMP = 0)
CSR_PMPADDR9       = U.w(12)(0x3B9)         # Not included (USE_PMP = 0)
CSR_PMPADDR10      = U.w(12)(0x3BA)         # Not included (USE_PMP = 0)
CSR_PMPADDR11      = U.w(12)(0x3BB)         # Not included (USE_PMP = 0)
CSR_PMPADDR12      = U.w(12)(0x3BC)         # Not included (USE_PMP = 0)
CSR_PMPADDR13      = U.w(12)(0x3BD)         # Not included (USE_PMP = 0)
CSR_PMPADDR14      = U.w(12)(0x3BE)         # Not included (USE_PMP = 0)
CSR_PMPADDR15      = U.w(12)(0x3BF)         # Not included (USE_PMP = 0)

# Trigger
CSR_TSELECT        = U.w(12)(0x7A0)
CSR_TDATA1         = U.w(12)(0x7A1)
CSR_TDATA2         = U.w(12)(0x7A2)
CSR_TDATA3         = U.w(12)(0x7A3)
CSR_TINFO          = U.w(12)(0x7A4)
CSR_MCONTEXT       = U.w(12)(0x7A8)
CSR_SCONTEXT       = U.w(12)(0x7AA)

# Debug/trace
CSR_DCSR           = U.w(12)(0x7B0)
CSR_DPC            = U.w(12)(0x7B1)

# Debug
CSR_DSCRATCH0      = U.w(12)(0x7B2)
CSR_DSCRATCH1      = U.w(12)(0x7B3)

# Hardware Performance Monitor
CSR_MCYCLE         = U.w(12)(0xB00)
CSR_MINSTRET       = U.w(12)(0xB02)
CSR_MHPMCOUNTER3   = U.w(12)(0xB03)
CSR_MHPMCOUNTER4   = U.w(12)(0xB04)
CSR_MHPMCOUNTER5   = U.w(12)(0xB05)
CSR_MHPMCOUNTER6   = U.w(12)(0xB06)
CSR_MHPMCOUNTER7   = U.w(12)(0xB07)
CSR_MHPMCOUNTER8   = U.w(12)(0xB08)
CSR_MHPMCOUNTER9   = U.w(12)(0xB09)
CSR_MHPMCOUNTER10  = U.w(12)(0xB0A)
CSR_MHPMCOUNTER11  = U.w(12)(0xB0B)
CSR_MHPMCOUNTER12  = U.w(12)(0xB0C)
CSR_MHPMCOUNTER13  = U.w(12)(0xB0D)
CSR_MHPMCOUNTER14  = U.w(12)(0xB0E)
CSR_MHPMCOUNTER15  = U.w(12)(0xB0F)
CSR_MHPMCOUNTER16  = U.w(12)(0xB10)
CSR_MHPMCOUNTER17  = U.w(12)(0xB11)
CSR_MHPMCOUNTER18  = U.w(12)(0xB12)
CSR_MHPMCOUNTER19  = U.w(12)(0xB13)
CSR_MHPMCOUNTER20  = U.w(12)(0xB14)
CSR_MHPMCOUNTER21  = U.w(12)(0xB15)
CSR_MHPMCOUNTER22  = U.w(12)(0xB16)
CSR_MHPMCOUNTER23  = U.w(12)(0xB17)
CSR_MHPMCOUNTER24  = U.w(12)(0xB18)
CSR_MHPMCOUNTER25  = U.w(12)(0xB19)
CSR_MHPMCOUNTER26  = U.w(12)(0xB1A)
CSR_MHPMCOUNTER27  = U.w(12)(0xB1B)
CSR_MHPMCOUNTER28  = U.w(12)(0xB1C)
CSR_MHPMCOUNTER29  = U.w(12)(0xB1D)
CSR_MHPMCOUNTER30  = U.w(12)(0xB1E)
CSR_MHPMCOUNTER31  = U.w(12)(0xB1F)

CSR_MCYCLEH        = U.w(12)(0xB80)
CSR_MINSTRETH      = U.w(12)(0xB82)
CSR_MHPMCOUNTER3H  = U.w(12)(0xB83)
CSR_MHPMCOUNTER4H  = U.w(12)(0xB84)
CSR_MHPMCOUNTER5H  = U.w(12)(0xB85)
CSR_MHPMCOUNTER6H  = U.w(12)(0xB86)
CSR_MHPMCOUNTER7H  = U.w(12)(0xB87)
CSR_MHPMCOUNTER8H  = U.w(12)(0xB88)
CSR_MHPMCOUNTER9H  = U.w(12)(0xB89)
CSR_MHPMCOUNTER10H = U.w(12)(0xB8A)
CSR_MHPMCOUNTER11H = U.w(12)(0xB8B)
CSR_MHPMCOUNTER12H = U.w(12)(0xB8C)
CSR_MHPMCOUNTER13H = U.w(12)(0xB8D)
CSR_MHPMCOUNTER14H = U.w(12)(0xB8E)
CSR_MHPMCOUNTER15H = U.w(12)(0xB8F)
CSR_MHPMCOUNTER16H = U.w(12)(0xB90)
CSR_MHPMCOUNTER17H = U.w(12)(0xB91)
CSR_MHPMCOUNTER18H = U.w(12)(0xB92)
CSR_MHPMCOUNTER19H = U.w(12)(0xB93)
CSR_MHPMCOUNTER20H = U.w(12)(0xB94)
CSR_MHPMCOUNTER21H = U.w(12)(0xB95)
CSR_MHPMCOUNTER22H = U.w(12)(0xB96)
CSR_MHPMCOUNTER23H = U.w(12)(0xB97)
CSR_MHPMCOUNTER24H = U.w(12)(0xB98)
CSR_MHPMCOUNTER25H = U.w(12)(0xB99)
CSR_MHPMCOUNTER26H = U.w(12)(0xB9A)
CSR_MHPMCOUNTER27H = U.w(12)(0xB9B)
CSR_MHPMCOUNTER28H = U.w(12)(0xB9C)
CSR_MHPMCOUNTER29H = U.w(12)(0xB9D)
CSR_MHPMCOUNTER30H = U.w(12)(0xB9E)
CSR_MHPMCOUNTER31H = U.w(12)(0xB9F)

CSR_CYCLE          = U.w(12)(0xC00)
CSR_INSTRET        = U.w(12)(0xC02)
CSR_HPMCOUNTER3    = U.w(12)(0xC03)
CSR_HPMCOUNTER4    = U.w(12)(0xC04)
CSR_HPMCOUNTER5    = U.w(12)(0xC05)
CSR_HPMCOUNTER6    = U.w(12)(0xC06)
CSR_HPMCOUNTER7    = U.w(12)(0xC07)
CSR_HPMCOUNTER8    = U.w(12)(0xC08)
CSR_HPMCOUNTER9    = U.w(12)(0xC09)
CSR_HPMCOUNTER10   = U.w(12)(0xC0A)
CSR_HPMCOUNTER11   = U.w(12)(0xC0B)
CSR_HPMCOUNTER12   = U.w(12)(0xC0C)
CSR_HPMCOUNTER13   = U.w(12)(0xC0D)
CSR_HPMCOUNTER14   = U.w(12)(0xC0E)
CSR_HPMCOUNTER15   = U.w(12)(0xC0F)
CSR_HPMCOUNTER16   = U.w(12)(0xC10)
CSR_HPMCOUNTER17   = U.w(12)(0xC11)
CSR_HPMCOUNTER18   = U.w(12)(0xC12)
CSR_HPMCOUNTER19   = U.w(12)(0xC13)
CSR_HPMCOUNTER20   = U.w(12)(0xC14)
CSR_HPMCOUNTER21   = U.w(12)(0xC15)
CSR_HPMCOUNTER22   = U.w(12)(0xC16)
CSR_HPMCOUNTER23   = U.w(12)(0xC17)
CSR_HPMCOUNTER24   = U.w(12)(0xC18)
CSR_HPMCOUNTER25   = U.w(12)(0xC19)
CSR_HPMCOUNTER26   = U.w(12)(0xC1A)
CSR_HPMCOUNTER27   = U.w(12)(0xC1B)
CSR_HPMCOUNTER28   = U.w(12)(0xC1C)
CSR_HPMCOUNTER29   = U.w(12)(0xC1D)
CSR_HPMCOUNTER30   = U.w(12)(0xC1E)
CSR_HPMCOUNTER31   = U.w(12)(0xC1F)

CSR_CYCLEH         = U.w(12)(0xC80)
CSR_INSTRETH       = U.w(12)(0xC82)
CSR_HPMCOUNTER3H   = U.w(12)(0xC83)
CSR_HPMCOUNTER4H   = U.w(12)(0xC84)
CSR_HPMCOUNTER5H   = U.w(12)(0xC85)
CSR_HPMCOUNTER6H   = U.w(12)(0xC86)
CSR_HPMCOUNTER7H   = U.w(12)(0xC87)
CSR_HPMCOUNTER8H   = U.w(12)(0xC88)
CSR_HPMCOUNTER9H   = U.w(12)(0xC89)
CSR_HPMCOUNTER10H  = U.w(12)(0xC8A)
CSR_HPMCOUNTER11H  = U.w(12)(0xC8B)
CSR_HPMCOUNTER12H  = U.w(12)(0xC8C)
CSR_HPMCOUNTER13H  = U.w(12)(0xC8D)
CSR_HPMCOUNTER14H  = U.w(12)(0xC8E)
CSR_HPMCOUNTER15H  = U.w(12)(0xC8F)
CSR_HPMCOUNTER16H  = U.w(12)(0xC90)
CSR_HPMCOUNTER17H  = U.w(12)(0xC91)
CSR_HPMCOUNTER18H  = U.w(12)(0xC92)
CSR_HPMCOUNTER19H  = U.w(12)(0xC93)
CSR_HPMCOUNTER20H  = U.w(12)(0xC94)
CSR_HPMCOUNTER21H  = U.w(12)(0xC95)
CSR_HPMCOUNTER22H  = U.w(12)(0xC96)
CSR_HPMCOUNTER23H  = U.w(12)(0xC97)
CSR_HPMCOUNTER24H  = U.w(12)(0xC98)
CSR_HPMCOUNTER25H  = U.w(12)(0xC99)
CSR_HPMCOUNTER26H  = U.w(12)(0xC9A)
CSR_HPMCOUNTER27H  = U.w(12)(0xC9B)
CSR_HPMCOUNTER28H  = U.w(12)(0xC9C)
CSR_HPMCOUNTER29H  = U.w(12)(0xC9D)
CSR_HPMCOUNTER30H  = U.w(12)(0xC9E)
CSR_HPMCOUNTER31H  = U.w(12)(0xC9F)

# Machine information
CSR_MVENDORID      = U.w(12)(0xF11)
CSR_MARCHID        = U.w(12)(0xF12)
CSR_MIMPID         = U.w(12)(0xF13)
CSR_MHARTID        = U.w(12)(0xF14)
