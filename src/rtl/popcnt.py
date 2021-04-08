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
   File Name: popcnt.py
   Description: Count the number of '1's in a word
"""
from pyhcl import *


def popcnt():
    class POPCNT(Module):
        io = IO(
            in_i=Input(U.w(32)),
            result_o=Output(U.w(6))
        )

        cnt_l1 = Wire(Vec(16, U.w(2)))
        cnt_l2 = Wire(Vec(8, U.w(3)))
        cnt_l3 = Wire(Vec(4, U.w(4)))
        cnt_l4 = Wire(Vec(2, U.w(5)))

        for i in range(16):
            cnt_l1[i] <<= CatBits(U.w(1)(0), io.in_i[2*i]) + CatBits(U.w(1)(0), io.in_i[2*i+1])

        for i in range(8):
            cnt_l2[i] <<= CatBits(U.w(1)(0), cnt_l1[2*i]) + CatBits(U.w(1)(0), cnt_l1[2*i+1])

        for i in range(4):
            cnt_l3[i] <<= CatBits(U.w(1)(0), cnt_l2[2*i]) + CatBits(U.w(1)(0), cnt_l2[2*i+1])

        for i in range(2):
            cnt_l4[i] <<= CatBits(U.w(1)(0), cnt_l3[2*i]) + CatBits(U.w(1)(0), cnt_l3[2*i+1])

        io.result_o <<= CatBits(U.w(1)(0), cnt_l4[0]) + CatBits(U.w(1)(0), cnt_l4[1])

    return POPCNT()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(popcnt()), "popcnt.fir"))
