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

   Author Name:
   Date:
   File Name:
   Description:
"""

from pyhcl import *


def aligner():
    class ALIGNER(Module):
        io = IO(
            fetch_valid_i=Input(Bool),
            aligner_ready_o=Output(Bool),
            if_valid_i=Input(Bool),
            fetch_rdata_i=Input(U.w(32)),
            instr_aligned_o=Output(U.w(32)),
            instr_valid_o=Output(Bool),
            branch_addr_i=Input(U.w(32)),
            branch_i=Input(Bool),
            hwlp_addr_i=Input(U.w(32)),
            hwlp_update_pc_i=Input(Bool),
            pc_o=Output(U.w(32))
        )

    return ALIGNER()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(aligner()), "aligner.fir"))
