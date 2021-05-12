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
   File Name: dm_pkg.py
   Description: Debug-module package, contains common system definitions
"""
from pyhcl import *

# pkg dm
ProgBufSize = 8             # size of program buffer in junks of 32-bit words
DataCount = 2               # amount of data count registers implemented

# DTM
DTM_OP_WIDTH = 2

DTM_NOP = U.w(2)(0)
DTM_READ = U.w(2)(1)
DTM_WRITE = U.w(2)(2)

# cmd_e
CMD_E_WIDTH = 8

AccessRegister = U.w(8)(0)
QuickAccess = U.w(8)(1)
AccessMemory = U.w(8)(2)

# cmderr_e
CMDERR_E_WIDTH = 3

CmdErrNone = U.w(3)(0)
CmdErrBusy = U.w(3)(1)
CmdErrNotSupported = U.w(3)(2)
CmdErrorException = U.w(3)(3)
CmdErrorHaltResume = U.w(3)(4)
CmdErrorBus = U.w(3)(5)
CmdErrorOther = U.w(3)(7)

DTM_SUCCESS = U.w(2)(0)

# debug registers
DM_CSR_E_WIDTH = 8

Data0        = U.w(8)(0x04)
Data1        = U.w(8)(0x05)
Data2        = U.w(8)(0x06)
Data3        = U.w(8)(0x07)
Data4        = U.w(8)(0x08)
Data5        = U.w(8)(0x09)
Data6        = U.w(8)(0x0A)
Data7        = U.w(8)(0x0B)
Data8        = U.w(8)(0x0C)
Data9        = U.w(8)(0x0D)
Data10       = U.w(8)(0x0E)
Data11       = U.w(8)(0x0F)
DMControl    = U.w(8)(0x10)
DMStatus     = U.w(8)(0x11)
Hartinfo     = U.w(8)(0x12)
HaltSum1     = U.w(8)(0x13)
HAWindowSel  = U.w(8)(0x14)
HAWindow     = U.w(8)(0x15)
AbstractCS   = U.w(8)(0x16)
Command      = U.w(8)(0x17)
AbstractAuto = U.w(8)(0x18)
DevTreeAddr0 = U.w(8)(0x19)
DevTreeAddr1 = U.w(8)(0x1A)
DevTreeAddr2 = U.w(8)(0x1B)
DevTreeAddr3 = U.w(8)(0x1C)
NextDM       = U.w(8)(0x1D)
ProgBuf0     = U.w(8)(0x20)
ProgBuf1     = U.w(8)(0x21)
ProgBuf2     = U.w(8)(0x22)
ProgBuf3     = U.w(8)(0x23)
ProgBuf4     = U.w(8)(0x24)
ProgBuf5     = U.w(8)(0x25)
ProgBuf6     = U.w(8)(0x26)
ProgBuf7     = U.w(8)(0x27)
ProgBuf8     = U.w(8)(0x28)
ProgBuf9     = U.w(8)(0x29)
ProgBuf10    = U.w(8)(0x2A)
ProgBuf11    = U.w(8)(0x2B)
ProgBuf12    = U.w(8)(0x2C)
ProgBuf13    = U.w(8)(0x2D)
ProgBuf14    = U.w(8)(0x2E)
ProgBuf15    = U.w(8)(0x2F)
AuthData     = U.w(8)(0x30)
HaltSum2     = U.w(8)(0x34)
HaltSum3     = U.w(8)(0x35)
SBAddress3   = U.w(8)(0x37)
SBCS         = U.w(8)(0x38)
SBAddress0   = U.w(8)(0x39)
SBAddress1   = U.w(8)(0x3A)
SBAddress2   = U.w(8)(0x3B)
SBData0      = U.w(8)(0x3C)
SBData1      = U.w(8)(0x3D)
SBData2      = U.w(8)(0x3E)
SBData3      = U.w(8)(0x3F)
HaltSum0     = U.w(8)(0x40)


# Packed structs
class dmstatus_t:
    def __init__(self):
        # This struct only use in non-state elements
        self.zero1 = Wire(U.w(9))
        self.impebreak = Wire(Bool)
        self.zero0 = Wire(U.w(2))
        self.allhavereset = Wire(Bool)
        self.anyhavereset = Wire(Bool)
        self.allresumeack = Wire(Bool)
        self.anyresumeack = Wire(Bool)
        self.allnonexistent = Wire(Bool)
        self.anynonexistent = Wire(Bool)
        self.allunavail = Wire(Bool)
        self.anyunavail = Wire(Bool)
        self.allrunning = Wire(Bool)
        self.anyrunning = Wire(Bool)
        self.allhalted = Wire(Bool)
        self.anyhalted = Wire(Bool)
        self.authenticated = Wire(Bool)
        self.authbusy = Wire(Bool)
        self.hasresethaltreq = Wire(Bool)
        self.devtreevalid = Wire(Bool)
        self.version = Wire(U.w(4))


class dmcontrol_t:
    def __init__(self, q: bool):
        self.haltreq = RegInit(Bool(False)) if q else Wire(Bool)
        self.resumereq = RegInit(Bool(False)) if q else Wire(Bool)
        self.hartreset = RegInit(Bool(False)) if q else Wire(Bool)
        self.ackhavereset = RegInit(Bool(False)) if q else Wire(Bool)
        self.zero1 = RegInit(Bool(False)) if q else Wire(Bool)
        self.hasel = RegInit(Bool(False)) if q else Wire(Bool)
        self.hartsello = RegInit(U.w(10)(0)) if q else Wire(U.w(10))
        self.hartselhi = RegInit(U.w(10)(0)) if q else Wire(U.w(10))
        self.zero = RegInit(U.w(2)(0)) if q else Wire(U.w(2))
        self.setresethaltreq = RegInit(Bool(False)) if q else Wire(Bool)
        self.clrresethaltreq = RegInit(Bool(False)) if q else Wire(Bool)
        self.ndmreset = RegInit(Bool(False)) if q else Wire(Bool)
        self.dmactive = RegInit(Bool(False)) if q else Wire(Bool)


class abstractcs_t:
    def __init__(self):
        self.zero3 = Wire(U.w(3))
        self.progbufsize = Wire(U.w(5))
        self.zero2 = Wire(U.w(11))
        self.busy = Wire(Bool)
        self.zero1 = Wire(Bool)
        self.cmderr = Wire(U.w(CMDERR_E_WIDTH))
        self.zero0 = Wire(U.w(4))
        self.datacount = Wire(U.w(4))


class command_t:
    def __init__(self, q: bool):
        self.cmdtype = RegInit(U.w(CMD_E_WIDTH)(0)) if q else Wire(U.w(CMD_E_WIDTH))
        self.control = RegInit(U.w(24)(0)) if q else Wire(U.w(24))


class abstractauto_t:
    def __init__(self, q: bool):
        self.autoexecprogbuf = RegInit(U.w(16)(0)) if q else Wire(U.w(16))
        self.zero0 = RegInit(U.w(4)(0)) if q else Wire(U.w(4))
        self.autoexecdata = RegInit(U.w(12)(0)) if q else Wire(U.w(12))


class sbcs_t:
    def __init__(self, q: bool):
        self.sbversion = RegInit(U.w(3)(0)) if q else Wire(U.w(3))
        self.zero0 = RegInit(U.w(6)(0)) if q else Wire(U.w(6))
        self.sbbusyerror = RegInit(Bool(False)) if q else Wire(Bool)
        self.sbbusy = RegInit(Bool(False)) if q else Wire(Bool)
        self.sbreadonaddr = RegInit(Bool(False)) if q else Wire(Bool)
        self.sbaccess = RegInit(U.w(3)(0)) if q else Wire(U.w(3))
        self.sbautoincrement = RegInit(Bool(False)) if q else Wire(Bool)
        self.sbreadondata = RegInit(Bool(False)) if q else Wire(Bool)
        self.sberror = RegInit(U.w(3)(0)) if q else Wire(U.w(3))
        self.sbasize = RegInit(U.w(7)(0)) if q else Wire(U.w(7))
        self.sbaccess128 = RegInit(Bool(False)) if q else Wire(Bool)
        self.sbaccess64 = RegInit(Bool(False)) if q else Wire(Bool)
        self.sbaccess32 = RegInit(Bool(False)) if q else Wire(Bool)
        self.sbaccess16 = RegInit(Bool(False)) if q else Wire(Bool)
        self.sbaccess8 = RegInit(Bool(False)) if q else Wire(Bool)
