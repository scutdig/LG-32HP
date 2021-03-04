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


# Prefetch controller state (for FSM)
PState_IDLE = U.w(1)(0)
PState_BRANCH_WAIT = U.w(1)(1)


# OpCodes
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