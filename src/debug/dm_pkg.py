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
