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


def compressed_decoder(FPU=0):
    class COMPRESSED_DECODER(Module):
        io = IO(
            instr_i=Input(U.w(32)),
            instr_o=Output(U.w(32)),
            is_compressed_o=Output(Bool),
            illegal_instr_o=Output(Bool)
        )

    return COMPRESSED_DECODER()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(compressed_decoder()), "compressed_decoder.fir"))