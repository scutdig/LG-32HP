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
DbgVersion013 = U.w(4)(2)
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

        self.packed = Wire(U.w(32))
        self.packed <<= CatBits(self.zero1, self.impebreak, self.zero0, self.allhavereset,
                              self.anyhavereset, self.allresumeack, self.anyresumeack,
                              self.allnonexistent, self.anynonexistent, self.allunavail,
                              self.anyunavail, self.allrunning, self.anyrunning, self.allhalted,
                              self.anyhalted, self.authenticated, self.authbusy, self.hasresethaltreq,
                              self.devtreevalid, self.version)

        self.clear()

    def clear(self):
        self.zero1 <<= U(0)
        self.impebreak <<= U(0)
        self.zero0 <<= U(0)
        self.allhavereset <<= U(0)
        self.anyhavereset <<= U(0)
        self.allresumeack <<= U(0)
        self.anyresumeack <<= U(0)
        self.allnonexistent <<= U(0)
        self.anynonexistent <<= U(0)
        self.allunavail <<= U(0)
        self.anyunavail <<= U(0)
        self.allrunning <<= U(0)
        self.anyrunning <<= U(0)
        self.allhalted <<= U(0)
        self.anyhalted <<= U(0)
        self.authenticated <<= U(0)
        self.authbusy <<= U(0)
        self.hasresethaltreq <<= U(0)
        self.devtreevalid <<= U(0)
        self.version <<= U(0)


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
        self.zero0 = RegInit(U.w(2)(0)) if q else Wire(U.w(2))
        self.setresethaltreq = RegInit(Bool(False)) if q else Wire(Bool)
        self.clrresethaltreq = RegInit(Bool(False)) if q else Wire(Bool)
        self.ndmreset = RegInit(Bool(False)) if q else Wire(Bool)
        self.dmactive = RegInit(Bool(False)) if q else Wire(Bool)

        self.packed = Wire(U.w(32))
        self.packed <<= CatBits(self.haltreq, self.resumereq, self.hartreset, self.ackhavereset,
                              self.zero1, self.hasel, self.hartsello, self.hartselhi, self.zero0,
                              self.setresethaltreq, self.clrresethaltreq, self.ndmreset, self.dmactive)

        if not q:
            self.clear()

    def clear(self):
        self.haltreq <<= U(0)
        self.resumereq <<= U(0)
        self.hartreset <<= U(0)
        self.ackhavereset <<= U(0)
        self.zero1 <<= U(0)
        self.hasel <<= U(0)
        self.hartsello <<= U(0)
        self.hartselhi <<= U(0)
        self.zero0 <<= U(0)
        self.setresethaltreq <<= U(0)
        self.clrresethaltreq <<= U(0)
        self.ndmreset <<= U(0)
        self.dmactive <<= U(0)

# def con_dmcontrol_t(l: dmcontrol_t, r: dmcontrol_t):
#     l.haltreq <<= r.haltreq
#     l.resumereq <<= r.resumereq
#     l.hartreset <<= r.hartreset
#     l.ackhavereset <<= r.ackhavereset
#     l.zero1 <<= r.zero1
#     l.hasel <<= r.hasel
#     l.hartsello <<= r.hartsello
#     l.hartselhi <<= r.hartselhi
#     l.zero <<= r.zero
#     l.setresethaltreq <<= r.setresethaltreq
#     l.clrresethaltreq <<= r.clrresethaltreq
#     l.ndmreset <<= r.ndmreset
#     l.dmactive <<= r.dmactive


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

        self.packed = Wire(U.w(32))
        self.packed <<= CatBits(self.zero3, self.progbufsize, self.zero2, self.busy,
                              self.zero1, self.cmderr, self.zero0, self.datacount)

        self.clear()

    def clear(self):
        self.zero3 <<= U(0)
        self.progbufsize <<= U(0)
        self.zero2 <<= U(0)
        self.busy <<= U(0)
        self.zero1 <<= U(0)
        self.cmderr <<= U(0)
        self.zero0 <<= U(0)
        self.datacount <<= U(0)


class command_t:
    def __init__(self, q: bool):
        self.cmdtype = RegInit(U.w(CMD_E_WIDTH)(0)) if q else Wire(U.w(CMD_E_WIDTH))
        self.control = RegInit(U.w(24)(0)) if q else Wire(U.w(24))

        self.packed = Wire(U.w(32))
        self.packed <<= CatBits(self.cmdtype, self.control)

        if not q:
            self.clear()

    def clear(self):
        self.cmdtype <<= U(0)
        self.control <<= U(0)


# def con_command_t(l: command_t, r: command_t):
#     l.cmdtype <<= r.cmdtype
#     l.control <<= r.control


class abstractauto_t:
    def __init__(self, q: bool):
        self.autoexecprogbuf = RegInit(U.w(16)(0)) if q else Wire(U.w(16))
        self.zero0 = RegInit(U.w(4)(0)) if q else Wire(U.w(4))
        self.autoexecdata = RegInit(U.w(12)(0)) if q else Wire(U.w(12))

        self.autoexecdata_vec = Wire(Vec(12, Bool))
        for i in range(12):
            self.autoexecdata_vec[i] <<= U(0)
        self.autoexecdata <<= CatBits(*self.autoexecdata_vec)

        self.autoexecprogbuf_vec = Wire(Vec(16, Bool))
        for i in range(16):
            self.autoexecprogbuf_vec[i] <<= U(0)
        self.autoexecprogbuf <<= CatBits(*self.autoexecprogbuf_vec)

        self.packed = Wire(U.w(32))
        self.packed <<= CatBits(self.autoexecprogbuf, self.zero0, self.autoexecdata)

        if not q:
            self.clear()

    def clear(self):
        self.autoexecprogbuf <<= U(0)
        self.zero0 <<= U(0)
        self.autoexecdata <<= U(0)


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

        self.packed = Wire(U.w(32))
        self.packed <<= CatBits(self.sbversion, self.zero0, self.sbbusyerror, self.sbbusy,
                              self.sbreadonaddr, self.sbaccess, self.sbautoincrement,
                              self.sbreadondata, self.sberror, self.sbasize, self.sbaccess128,
                              self.sbaccess64, self.sbaccess32, self.sbaccess16, self.sbaccess8)

        if not q:
            self.clear()

    def clear(self):
        self.sbversion <<= U(0)
        self.zero0 <<= U(0)
        self.sbbusyerror <<= U(0)
        self.sbbusy <<= U(0)
        self.sbreadonaddr <<= U(0)
        self.sbaccess <<= U(0)
        self.sbautoincrement <<= U(0)
        self.sbreadondata <<= U(0)
        self.sberror <<= U(0)
        self.sbasize <<= U(0)
        self.sbaccess128 <<= U(0)
        self.sbaccess64 <<= U(0)
        self.sbaccess32 <<= U(0)
        self.sbaccess16 <<= U(0)
        self.sbaccess8 <<= U(0)


# def con_sbcs_t(l: sbcs_t, r: sbcs_t):
#     l.sbversion <<= r.sbversion
#     l.zero0 <<= r.zero0
#     l.sbbusyerror <<= r.sbbusyerror
#     l.sbbusy <<= r.sbbusy
#     l.sbreadonaddr <<= r.sbreadonaddr
#     l.sbaccess <<= r.sbaccess
#     l.sbautoincrement <<= r.sbautoincrement
#     l.sbreadondata <<= r.sbreadondata
#     l.sberror <<= r.sberror
#     l.sbasize <<= r.sbasize
#     l.sbaccess128 <<= r.sbaccess128
#     l.sbaccess64 <<= r.sbaccess64
#     l.sbaccess32 <<= r.sbaccess32
#     l.sbaccess16 <<= r.sbaccess16
#     l.sbaccess8 <<= r.sbaccess8

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

# SBA state

SBA_STATE_E_WIDTH = 3

Idle = U.w(3)(0)
Read = U.w(3)(1)
Write = U.w(3)(2)
WaitRead = U.w(3)(3)
WaitWrite = U.w(3)(4)
