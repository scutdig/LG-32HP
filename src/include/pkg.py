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
OPCODe_OP_FMSUB  = U.w(7)(0x47)
OPCODE_OP_FNMSUB = U.w(7)(0x4b)
OPCODE_STORE_FP  = U.w(7)(0x27)
OPCODE_LOAD_FP   = U.w(7)(0x07)
OPCODE_AMO       = U.w(7)(0x2f)


##################################################################################
# ALU Operations
##################################################################################
ALU_OP_WIDTH = 7

# Enum logic
ALU_ADD   = U.w(7)(0x0011000)
ALU_SUB   = U.w(7)(0x0011001)
ALU_ADDU  = U.w(7)(0x0011010)
ALU_SUBU  = U.w(7)(0x0011011)
ALU_ADDR  = U.w(7)(0x0011100)
ALU_SUBR  = U.w(7)(0x0011101)
ALU_ADDUR = U.w(7)(0x0011110)
ALU_SUBUR = U.w(7)(0x0011111)

ALU_XOR   = U.w(7)(0x0101111)
ALU_OR    = U.w(7)(0x0101110)
ALU_AND   = U.w(7)(0x0010101)

#  Shifts
ALU_SRA   = U.w(7)(0x0100100)
ALU_SRL   = U.w(7)(0x0100101)
ALU_ROR   = U.w(7)(0x0100110)
ALU_SLL   = U.w(7)(0x0100111)

#  bit manipulation
ALU_BEXT  = U.w(7)(0x0101000)
ALU_BEXTU = U.w(7)(0x0101001)
ALU_BINS  = U.w(7)(0x0101010)
ALU_BCLR  = U.w(7)(0x0101011)
ALU_BSET  = U.w(7)(0x0101100)
ALU_BREV  = U.w(7)(0x1001001)

#  Bit counting
ALU_FF1   = U.w(7)(0x0110110)
ALU_FL1   = U.w(7)(0x0110111)
ALU_CNT   = U.w(7)(0x0110100)
ALU_CLB   = U.w(7)(0x0110101)

#  Sign-/zero-extensions
ALU_EXTS  = U.w(7)(0x0111110)
ALU_EXT   = U.w(7)(0x0111111)

#  Comparisons
ALU_LTS   = U.w(7)(0x0000000)
ALU_LTU   = U.w(7)(0x0000001)
ALU_LES   = U.w(7)(0x0000100)
ALU_LEU   = U.w(7)(0x0000101)
ALU_GTS   = U.w(7)(0x0001000)
ALU_GTU   = U.w(7)(0x0001001)
ALU_GES   = U.w(7)(0x0001010)
ALU_GEU   = U.w(7)(0x0001011)
ALU_EQ    = U.w(7)(0x0001100)
ALU_NE    = U.w(7)(0x0001101)

#  Set Lower Than operations
ALU_SLTS  = U.w(7)(0x0000010)
ALU_SLTU  = U.w(7)(0x0000011)
ALU_SLETS = U.w(7)(0x0000110)
ALU_SLETU = U.w(7)(0x0000111)

#  Absolute value
ALU_ABS   = U.w(7)(0x0010100)
ALU_CLIP  = U.w(7)(0x0010110)
ALU_CLIPU = U.w(7)(0x0010111)

#  Insert/extract
ALU_INS   = U.w(7)(0x0101101)

#  min/max
ALU_MIN   = U.w(7)(0x0010000)
ALU_MINU  = U.w(7)(0x0010001)
ALU_MAX   = U.w(7)(0x0010010)
ALU_MAXU  = U.w(7)(0x0010011)

#  div/rem
ALU_DIVU  = U.w(7)(0x0110000)  # bit 0 is used for signed mode, bit 1 is used for remdiv
ALU_DIV   = U.w(7)(0x0110001)  # bit 0 is used for signed mode, bit 1 is used for remdiv
ALU_REMU  = U.w(7)(0x0110010)  # bit 0 is used for signed mode, bit 1 is used for remdiv
ALU_REM   = U.w(7)(0x0110011)  # bit 0 is used for signed mode, bit 1 is used for remdiv

ALU_SHUF  = U.w(7)(0x0111010)
ALU_SHUF2 = U.w(7)(0x0111011)
ALU_PCKLO = U.w(7)(0x0111000)
ALU_PCKHI = U.w(7)(0x0111001)

MUL_OP_WIDTH = 3

# mul_opcode_e
MUL_MAC32 = U.w(3)(0x000)
MUL_MSU32 = U.w(3)(0x001)
MUL_I     = U.w(3)(0x010)
MUL_IR    = U.w(3)(0x011)
MUL_DOT8  = U.w(3)(0x100)
MUL_DOT16 = U.w(3)(0x101)
MUL_H     = U.w(3)(0x110)

##################################################################################
# CSR operations
##################################################################################
CSR_OP_WIDTH = 2

# csr_opcode_e
CSR_OP_READ  = U.w(2)(0x00)
CSR_OP_WRITE = U.w(2)(0x01)
CSR_OP_SET   = U.w(2)(0x10)
CSR_OP_CLEAR = U.w(2)(0x11)

##################################################################################
# Privileged mode
##################################################################################
PRIV_SEL_WIDTH = 2

# PrivLvl_t
PRIV_LVL_M = U.w(2)(0x11)
PRIV_LVL_H = U.w(2)(0x10)
PRIV_LVL_S = U.w(2)(0x01)
PRIV_LVL_U = U.w(2)(0x00)

##################################################################################
# IF Stage
##################################################################################
# PC mux selector defines
PC_BOOT      = U.w(4)(0)
PC_FENCEI    = U.w(4)(1)
PC_JUMP      = U.w(4)(2)
PC_BRANCH    = U.w(4)(3)
PC_EXCEPTION = U.w(4)(4)
PC_MRET      = U.w(4)(5)
PC_URET      = U.w(4)(6)
PC_DRET      = U.w(4)(7)

# Trap mux selector
TRAP_MACHINE = U.w(2)(0)
TRAP_USER    = U.w(2)(1)

# EXception PC mux selector defines
EXC_PC_EXCEPTION = U.w(3)(0)
EXC_PC_IRQ       = U.w(3)(1)
EXC_PC_DBD       = U.w(3)(2)
EXC_PC_DBE       = U.w(3)(3)


##################################################################################
# ID Stage
##################################################################################
# forwarding operand mux
SEL_REGFILE      = U.w(2)(0x00)
SEL_FW_EX        = U.w(2)(0x01)
SEL_FW_WB        = U.w(2)(0x10)

# operand a selection
OP_A_REGA_OR_FWD = U.w(3)(0x000)
OP_A_CURRPC      = U.w(3)(0x001)
OP_A_IMM         = U.w(3)(0x010)
OP_A_REGB_OR_FWD = U.w(3)(0x011)
OP_A_REGC_OR_FWD = U.w(3)(0x100)

# immediate a selection
IMMA_Z      = U.w(1)(0x0)
IMMA_ZERO   = U.w(1)(0x1)

# operand b selection
OP_B_REGB_OR_FWD = U.w(3)(0x000)
OP_B_REGC_OR_FWD = U.w(3)(0x001)
OP_B_IMM         = U.w(3)(0x010)
OP_B_REGA_OR_FWD = U.w(3)(0x011)
OP_B_BMASK       = U.w(3)(0x100)

# immediate b selection
IMMB_I      = U.w(4)(0x0000)
IMMB_S      = U.w(4)(0x0001)
IMMB_U      = U.w(4)(0x0010)
IMMB_PCINCR = U.w(4)(0x0011)
IMMB_S2     = U.w(4)(0x0100)
IMMB_S3     = U.w(4)(0x0101)
IMMB_VS     = U.w(4)(0x0110)
IMMB_VU     = U.w(4)(0x0111)
IMMB_SHUF   = U.w(4)(0x1000)
IMMB_CLIP   = U.w(4)(0x1001)
IMMB_BI     = U.w(4)(0x1011)

# multiplication immediates
MIMM_ZERO    = U.w(1)(0x0)
MIMM_S3      = U.w(1)(0x1)

# operand c selection
OP_C_REGC_OR_FWD = U.w(2)(0x00)
OP_C_REGB_OR_FWD = U.w(2)(0x01)
OP_C_JT          = U.w(2)(0x10)

# branch types
BRANCH_NONE = U.w(2)(0x00)
BRANCH_JAL  = U.w(2)(0x01)
BRANCH_JALR = U.w(2)(0x10)
BRANCH_COND = U.w(2)(0x11)  # conditional branches

# jump target mux
JT_JAL  = U.w(2)(0x01)
JT_JALR = U.w(2)(0x10)
JT_COND = U.w(2)(0x11)
