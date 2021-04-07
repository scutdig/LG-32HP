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
   Date: 2021-04-07
   File Name: alu_div.py
   Description: Simple serial divider for signed integers (int32)
"""
from pyhcl import *


def alu_div(C_WIDTH=32, C_LOG_WIDTH=6):
    class ALU_DIV(Module):
        io = IO(
            # Input IF
            OpA_DI=Input(U.w(C_WIDTH)),
            OpB_DI=Input(U.w(C_WIDTH)),
            OpBShift_DI=Input(U.w(C_LOG_WIDTH)),
            OpBIsZero_SI=Input(Bool),

            OpBSign_SI=Input(Bool),         # Gate this to 0 in case of unsigned ops
            OpCode_SI=Input(U.w(2)),
            # Handshake
            InVld_SI=Input(Bool),
            # Output IF
            OutRdy_SI=Input(Bool),
            OutVld_SO=Output(Bool),
            Res_DO=Output(U.w(C_WIDTH))
        )

        # Signal declarations
        

    return ALU_DIV()
