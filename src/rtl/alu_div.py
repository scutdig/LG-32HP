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


# FSM state
IDLE = U.w(2)(0)
DIVIDE = U.w(2)(1)
FINISH = U.w(2)(2)


def alu_div(C_WIDTH=32, C_LOG_WIDTH=6):
    class ALU_DIV(Module):
        io = IO(
            # Input IF
            OpA_DI=Input(U.w(C_WIDTH)),
            OpB_DI=Input(U.w(C_WIDTH)),
            OpBShift_DI=Input(U.w(C_LOG_WIDTH)),
            OpBIsZero_SI=Input(Bool),

            OpBSign_SI=Input(Bool),         # Gate this to 0 in case of unsigned ops
            OpCode_SI=Input(U.w(2)),        # 0:d iv, 2: urem, 1: div, 3: rem
            # Handshake
            InVld_SI=Input(Bool),
            # Output IF
            OutRdy_SI=Input(Bool),
            OutVld_SO=Output(Bool),
            Res_DO=Output(U.w(C_WIDTH))
        )

        # Signal declarations
        ResReg_DP = RegInit(U.w(C_WIDTH)(0))
        ResReg_DN = Wire(U.w(C_WIDTH))
        ResReg_DP_rev = Wire(U.w(C_WIDTH))
        AReg_DP = RegInit(U.w(C_WIDTH)(0))
        AReg_DN = Wire(U.w(C_WIDTH))
        BReg_DP = RegInit(U.w(C_WIDTH)(0))
        BReg_DN = Wire(U.w(C_WIDTH))
        RemSel_SP = RegInit(U.w(C_WIDTH)(0))
        RemSel_SN = Wire(U.w(C_WIDTH))
        CompInv_SP = RegInit(U.w(C_WIDTH)(0))
        CompInv_SN = Wire(U.w(C_WIDTH))
        ResInv_SP = RegInit(U.w(C_WIDTH)(0))
        ResInv_SN = Wire(U.w(C_WIDTH))

        AddMux_D, AddOut_D, AddTmp_D, BMux_D, OutMux_D = [Wire(U.w(C_WIDTH)) for _ in range(5)]

        Cnt_DP = RegInit(U.w(C_LOG_WIDTH)(0))
        Cnt_DN = Wire(U.w(C_LOG_WIDTH))
        CntZero_S = Wire(Bool)

        ARegEn_S, BRegEn_S, ResRegEn_S, ABComp_S, PmSel_S, LoadEn_S = [Wire(Bool) for _ in range(6)]

        State_SP = RegInit(IDLE)
        State_SN = Wire(U.w(2))

        # Datapath
        PmSel_S <<= LoadEn_S & (~(io.OpCode_SI[0] & (io.OpA_DI[C_WIDTH-1] ^ io.OpBSign_SI)))

        # Muxes
        AddMux_D <<= Mux(LoadEn_S, io.OpA_DI, BReg_DP)

        # Attention: logical shift in case of negative operand B
        BMux_D <<= Mux(LoadEn_S, io.OpB_DI, CatBits(CompInv_SP, BReg_DP[C_WIDTH-1:1]))

        # Bit swapping
        rev_swp_lst = [Wire(Bool) for _ in range(C_WIDTH)]
        for index in range(C_WIDTH):
            rev_swp_lst[index] = ResReg_DP[C_WIDTH-1-index]
        ResReg_DP_rev <<= CatBits(*rev_swp_lst)

        OutMux_D <<= Mux(RemSel_SP, AReg_DP, ResReg_DP_rev)

        # Invert if necessary
        io.Res_DO <<= Mux(ResInv_SP, (-(OutMux_D.to_sint())).to_uint(), OutMux_D)

        # Main Comparator
        or_red = Wire(Bool)
        for i in range(C_WIDTH-1, -1, -1):
            or_red <<= or_red | AReg_DP[i]
        ABComp_S <<= ((AReg_DP == BReg_DP) | ((AReg_DP > BReg_DP) ^ CompInv_SP)) & (or_red | io.OpBIsZero_SI)

        # Main adder
        AddTmp_D <<= Mux(LoadEn_S, U(0), AReg_DP)
        AddOut_D <<= Mux(PmSel_S, AddTmp_D + AddMux_D, (AddTmp_D.to_sint() - AddMux_D.to_sint()).to_uint())

        # Counter
        Cnt_DN <<= Mux(LoadEn_S, io.OpBShift_DI, Mux(~CntZero_S, Cnt_DP - U(1), Cnt_DP))
        cnt_dp_or_red = Wire(Bool)
        for i in range(C_LOG_WIDTH-1, -1, -1):
            cnt_dp_or_red <<= cnt_dp_or_red | Cnt_DP[i]
        CntZero_S <<= ~cnt_dp_or_red

        # FSM
        State_SN <<= State_SP
        io.OutVld_SO <<= Bool(False)
        LoadEn_S <<= Bool(False)
        ARegEn_S <<= Bool(False)
        BRegEn_S <<= Bool(False)
        ResRegEn_S <<= Bool(False)

        with when(State_SP == IDLE):
            io.OutVld_SO <<= Bool(True)

            with when(io.InVld_SI):
                io.OutVld_SO <<= Bool(False)
                ARegEn_S <<= Bool(True)
                BRegEn_S <<= Bool(True)
                LoadEn_S <<= Bool(True)
                State_SN <<= DIVIDE

        with elsewhen(State_SP == DIVIDE):
            ARegEn_S <<= ABComp_S
            BRegEn_S <<= Bool(True)
            ResRegEn_S <<= Bool(True)

            # Calculation finished
            # One more divide cycle (32nd divide cycle)
            with when(CntZero_S):
                State_SN <<= FINISH

        with elsewhen(State_SP == FINISH):
            io.OutVld_SO <<= Bool(True)

            with when(io.OutRdy_SI):
                State_SN <<= IDLE

        # Regs

        # Get flags
        RemSel_SN <<= Mux(LoadEn_S, io.OpCode_SI[1], RemSel_SP)
        CompInv_SN <<= Mux(LoadEn_S, io.OpBSign_SI, CompInv_SP)
        ResInv_SN <<= Mux(LoadEn_S,
                          (~io.OpBIsZero_SI | io.OpCode_SI[1]) & io.OpCode_SI[0] & (io.OpA_DI[C_WIDTH-1] ^ io.OpBSign_SI),
                          ResInv_SP)

        AReg_DN <<= Mux(ARegEn_S, AddOut_D, AReg_DP)
        BReg_DN <<= Mux(BRegEn_S, BMux_D, BReg_DP)
        ResReg_DN <<= Mux(LoadEn_S, U(0), Mux(ResRegEn_S,
                                                 CatBits(ABComp_S, ResReg_DP[C_WIDTH-1:1]), ResReg_DP))

        State_SP <<= State_SN
        AReg_DP <<= AReg_DN
        BReg_DP <<= BReg_DN
        ResReg_DP <<= ResReg_DN
        Cnt_DP <<= Cnt_DN
        RemSel_SP <<= RemSel_SN
        CompInv_SP <<= CompInv_SN
        ResInv_SP <<= ResInv_SN

    return ALU_DIV()


if __name__ == '__main__':
    Emitter.dumpVerilog_nock(Emitter.dump(Emitter.emit(alu_div()), "alu_div.fir"))
