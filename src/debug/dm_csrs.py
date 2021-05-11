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
   File Name: dm_csrs.py
   Description: Debug CSRs. Communication over Debug Transport Module (DTM)
"""
from pyhcl import *


def dm_csrs(NrHarts: int = 1, BusWidth: int = 32):
    SelectableHarts = CatBits(*[U.w(1)(1) * NrHarts])

    class DM_CSRS(Module):
        io = IO(
            testmode_i=Input(Bool),
            dmi_rst_ni=Input(Bool),         # Debug Module Intf reset active-low
            dmi_req_valid_i=Input(Bool),
            dmi_req_ready_o=Output(Bool),

            # dmi_req_t, expend
            dmi_req_i_addr=Input(U.w(7)),
            dmi_req_i_op=Input(U.w(2)),
            dmi_req_i_data=Input(U.w(32))
        )

    return DM_CSRS()
