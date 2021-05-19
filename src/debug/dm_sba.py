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
   Date: 2021-05-17
   File Name: dm_sba.py
   Description: System Bus Access Module
"""
from pyhcl import *
from src.debug.dm_pkg import *
from src.include.utils import *


def dm_sba(BusWidth: int = 32, ReadByteEnable: bool = True):
    class DM_SBA(Module):
        io = IO(
            dmactive_i=Input(Bool),         # Synchronous reset active low

            master_req_o=Output(Bool),
            master_add_o=Output(U.w(BusWidth)),
            master_we_o=Output(Bool),
            master_wdata_o=Output(U.w(BusWidth)),
            master_be_o=Output(U.w(int(BusWidth/8))),
            master_gnt_i=Input(Bool),
            master_r_valid_i=Input(Bool),
            master_r_rdata_i=Input(U.w(BusWidth)),

            sbaddress_i=Input(U.w(BusWidth)),
            sbaddress_write_valid_i=Input(Bool),
            # control signals in
            sbreadonaddr_i=Input(Bool),
            sbaddress_o=Output(U.w(BusWidth)),
            sbautoincrement_i=Input(Bool),
            sbaccess_i=Input(U.w(3)),
            # data in
            sbreadondata_i=Input(Bool),
            sbdata_i=Input(U.w(BusWidth)),
            sbdata_read_valid_i=Input(Bool),
            sbdata_write_valid_i=Input(Bool),
            # read data out
            sbdata_o=Output(U.w(BusWidth)),
            sbdata_valid_o=Output(Bool),
            # control signals
            sbbusy_o=Output(Bool),
            sberror_valid_o=Output(Bool),       # bus error occurred
            sberror_o=Output(U.w(3)),           # bus error occurred
        )

        state = gen_ff(SBA_STATE_E_WIDTH, 0)

        address = Wire(U.w(BusWidth))
        req = Wire(Bool)
        gnt = Wire(Bool)
        we = Wire(Bool)
        be = Wire(U.w(int(BusWidth/8)))
        be_mask = Wire(U.w(int(BusWidth/8)))
        be_idx = Wire(U.w(clog2(BusWidth/8)))

        io.sbbusy_o <<= (state.q == Idle)

        be_mask <<= U(0)

        # generate byte enable mask
        # helper vec for be_mask
        be_mask_vec = Wire(Vec(int(BusWidth/8), Bool))
        for i in range(int(BusWidth/8)):
            be_mask_vec[i] <<= be_mask[i]

        with when(io.sbaccess_i == U.w(3)(0)):
            be_mask_vec[be_idx] <<= Bool(True)
        with elsewhen(io.sbaccess_i == U.w(3)(1)):
            base_idx = CatBits(be_idx[clog2(BusWidth/8)-1:1], U.w(1)(0))
            # be_mask_vec[base_idx+U(1):base_idx] <<= U(1)
            be_mask_vec[base_idx] <<= U(1)
            be_mask_vec[base_idx+U(1)] <<= U(0)
        with elsewhen(io.sbaccess_i == U.w(3)(2)):
            with when(U(BusWidth) == U.w(32)(64)):
                base_idx = CatBits(be_idx[clog2(BusWidth/8)-1], U.w(2)(0))
                # be_mask_vec[base_idx+U(3):base_idx] <<= U(1)
                be_mask_vec[base_idx] <<= U(1)
                be_mask_vec[base_idx+U(1)] <<= U(0)
                be_mask_vec[base_idx+U(2)] <<= U(0)
                be_mask_vec[base_idx+U(3)] <<= U(0)
            with otherwise():
                for i in range(int(BusWidth/8)):
                    if i == 0:
                        be_mask_vec[i] <<= U(1)
                    else:
                        be_mask_vec[i] <<= U(0)
        be_mask <<= CatBits(*be_mask_vec)

        req <<= Bool(False)
        address <<= io.sbaddress_i
        we <<= Bool(False)
        be <<= Bool(False)
        be_idx <<= io.sbaddress_i[clog2(BusWidth/8)-1:0]

        io.sberror_o <<= U(0)
        io.sberror_valid_o <<= Bool(False)
        io.sbaddress_o <<= io.sbaddress_i

        state.n <<= state.q

        with when(state.q == Idle):
            # debugger requested a read
            with when(io.sbaddress_write_valid_i & io.sbreadonaddr_i):
                state.n <<= Read
            # debugger requested a write
            with when(io.sbdata_write_valid_i):
                state.n <<= Write
            # perform another read
            with when(io.sbdata_read_valid_i & io.sbreadondata_i):
                state.n <<= Read
        with elsewhen(state.q == Read):
            req <<= Bool(True)
            with when(U(ReadByteEnable)):
                be <<= be_mask
            with when(gnt):
                state.n <<= WaitRead
        with elsewhen(state.q == Write):
            req <<= Bool(True)
            we <<= Bool(True)
            be <<= be_mask
            with when(gnt):
                state.n <<= WaitWrite
        with elsewhen(state.q == WaitRead):
            with when(io.sbdata_valid_o):
                state.n <<= Idle
                # auto-increment address
                with when(io.sbautoincrement_i):
                    io.sbaddress_o <<= io.sbaddress_i + (U.w(32)(1) << io.sbaccess_i)
        with elsewhen(state.q == WaitWrite):
            with when(io.sbdata_valid_o):
                state.n <<= Idle
                # auto-increment address
                with when(io.sbautoincrement_i):
                    io.sbaddress_o <<= io.sbaddress_i + (U.w(32)(1) << io.sbaccess_i)
        with otherwise():
            state.n <<= Idle    # Catch parasitic state

        # handle error case
        with when((io.sbaccess_i > U(0)) & (state.q != Idle)):
            req <<= Bool(False)
            state.n <<= Idle
            io.sberror_valid_o <<= Bool(True)
            io.sberror_o <<= U.w(3)(3)

        # ff
        state.q <<= state.n

        io.master_req_o <<= req
        io.master_add_o <<= address[BusWidth-1:0]
        io.master_we_o <<= we
        io.master_wdata_o <<= io.sbdata_i[BusWidth-1:0]
        io.master_be_o <<= be[int(BusWidth/8)-1:0]
        gnt <<= io.master_gnt_i
        io.sbdata_valid_o <<= io.master_r_valid_i
        io.sbdata_o <<= io.master_r_rdata_i[BusWidth-1:0]

    return DM_SBA()


if __name__ == '__main__':
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(dm_sba()), "dm_sba.fir"))
