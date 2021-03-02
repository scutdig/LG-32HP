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
   File Name: obi_interface.py
   Description: "Open Bus Interface adapter. Translates transaction request
                on the trans_* interface into an OBI A channel transfer.
                The OBI R channel transfer translated (i.e. passed on) as
                a transaction response on the resp_* interface.

                This adapter does not limit the number of outstanding
                OBI transactions in any way." -- original RIS5Y annotation
"""
from pyhcl import *


def obi_interface(TRANS_STABLE=0):
    """
        args:
            TRANS_STABLE: TODO: missing description here
    """

    class OBI_INTERFACE(Module):
        io = IO(
            # Transaction request interface
            trans_valid_i=Input(Bool),
            trans_ready_o=Output(Bool),
            trans_addr_i=Input(U.w(32)),
            trans_we_i=Input(Bool),
            trans_be_i=Input(U.w(4)),
            trans_wdata_i=Input(U.w(32)),
            trans_atop_i=Input(U.w(6)),         # Future proof addition, no use

            # Transaction response interface
            resp_valid_o=Output(Bool),
            resp_rdata_o=Output(U.w(32)),
            resp_err_o=Output(Bool),

            # OBI interface
            obi_req_o=Output(Bool),
            obi_gnt_i=Input(Bool),
            obi_addr_o=Output(U.w(32)),
            obi_we_o=Output(Bool),
            obi_be_o=Output(U.w(4)),
            obi_wdata_o=Output(U.w(32)),
            obi_atop_o=Output(U.w(6)),
            obi_rdata_i=Input(U.w(32)),
            obi_rvalid_i=Input(Bool),
            obi_err_i=Input(Bool)
        )

    return OBI_INTERFACE()
