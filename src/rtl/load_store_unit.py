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
   Date: 2021-04-09
   File Name: load_store_unit.py
   Description: Load Store Unit, used to eliminate multiple access during
                processor stalls, and to align bytes and halfwords
"""
from pyhcl import *
from src.rtl.obi_interface import *


def load_store_unit(PULP_OBI=0):
    DEPTH = 2                   # Maximum number of outstanding transactions

    class LOAD_STORE_UNIT(Module):
        io = IO(
            # Output to data memory
            data_req_o=Output(Bool),
            data_gnt_i=Input(Bool),
            data_rvalid_i=Input(Bool),
            data_err_i=Input(Bool),             # External bus error (validity defined by data_rvalid) (not used yet)
            data_err_pmp_i=Input(Bool),         # PMP error (validity defined by data_gnt_i)

            data_addr_o=Output(U.w(32)),
            data_we_o=Output(Bool),
            data_be_o=Output(U.w(4)),
            data_wdata_o=Output(U.w(32)),
            data_rdata_i=Input(U.w(32)),

            # Signals from ex stage
            data_we_ex_i=Input(Bool),           # Write enbale                          -> from ex stage
            data_type_ex_i=Input(U.w(2)),       # Data type word, halfword, byte        -> from ex stage
            data_wdata_ex_i=Input(U.w(32)),     # Data to write to memory               -> from ex stage
            data_reg_offset_ex_i=Input(U.w(2)), # Offset inside register for stores     -> from ex stage
            data_load_event_ex_i=Input(Bool),   # Load event                            -> from ex stage
            data_sign_ext_ex_i=Input(U.w(2)),   # Sign extension                        -> from ex stage

            data_rdata_ex_o=Output(U.w(32)),    # Requested data                        -> to ex stage
            data_req_ex_i=Input(Bool),          # Data request                          -> from ex stage
            operand_a_ex_i=Input(U.w(32)),      # Operand a from RF for address         -> from ex stage
            operand_b_ex_i=Input(U.w(32)),      # Operand b from RF for address         -> from ex stage
            addr_useincr_ex_i=Input(Bool),      # Use a + b or just a for address       -> from ex stage

            data_misaligned_ex_i=Input(Bool),   # Misaligned access in last ld/st       -> from ID/EX pipeline
            data_misaligned_o=Output(Bool),     # Misaligned access was detected        -> to controller

            # No atomic signals support

            p_elw_start_o=Output(Bool),         # Load event starts
            p_elw_finish_o=Output(Bool),        # Load event finishes

            # Stall signal
            lsu_ready_ex_o=Output(Bool),        # LSU ready for new data in EX stage
            lsu_ready_wb_o=Output(Bool),        # LSU ready for new data in WB stage

            busy_o=Output(Bool)
        )

        # Sub module init
        obi_interface_i = obi_interface()

        # Transaction request (to obi_interface)
        trans_valid = Wire(Bool)
        trans_ready = Wire(Bool)
        trans_addr = Wire(U.w(32))
        trans_we = Wire(Bool)
        trans_be = Wire(U.w(4))
        trans_wdata = Wire(U.w(32))
        trans_atop = Wire(U.w(6))

        # Transaction response interface (from obi_interface)
        resp_valid = Wire(Bool)
        resp_rdata = Wire(U.w(32))
        resp_err = Wire(Bool)           # Unused for now

        # Counter to count maximum number of outstanding transactions
        cnt_q = RegInit(U.w(2)(0))      # Transaction counter
        next_cnt = Wire(U.w(2))         # Next value for cnt_q
        count_up = Wire(Bool)           # Increment outstanding transaction count by 1 (can happen at same time as count_down)
        count_down = Wire(Bool)         # Decrement outstanding transaction count by 1 (can happen at same time as count_up)

        ctrl_update = Wire(Bool)        # Update load/store control info in WB stage

        data_addr_int = Wire(U.w(32))

        # Registers for data_rdata alignment and sign extension
        data_type_q = RegInit(U.w(2)(0))
        rdata_offset_q = RegInit(U.w(2)(0))
        data_sign_ext_q = RegInit(U.w(2)(0))
        data_we_q = RegInit(Bool(False))
        data_load_event_q = RegInit(Bool(False))

        wdata_offset = Wire(U.w(2))     # Mux control for data to be written to memory

        data_be = Wire(U.w(4))
        data_wdata = Wire(U.w(32))

        misaligned_st = Wire(Bool)      # High if we are currently performing the second part of a misaligned store
        load_err_o, store_error_o = [Wire(Bool) for _ in range(2)]

        rdata_q = RegInit(U.w(32)(0))

        #################################### BE generation ####################################
        with when(io.data_type_ex_i == U.w(2)(0b00)):           # Data type 00 Word, 01, Half word, 11/10 byte
            # Writing a word
            with when(misaligned_st == Bool(False)):
                # non-misaligned case
                data_be <<= LookUpTable(data_addr_int[1:0], {
                    U.w(2)(0b00): U.w(4)(0b1111),
                    U.w(2)(0b01): U.w(4)(0b1110),
                    U.w(2)(0b10): U.w(4)(0b1100),
                    U.w(2)(0b11): U.w(4)(0b1000),
                    ...: U.w(4)(0b1111)
                })
            with otherwise():
                data_be <<= LookUpTable(data_addr_int[1:0], {
                    U.w(2)(0b00): U.w(4)(0b0000),
                    U.w(2)(0b01): U.w(4)(0b0001),
                    U.w(2)(0b10): U.w(4)(0b0011),
                    U.w(2)(0b11): U.w(4)(0b0111),
                    ...: U.w(4)(0b0000)
                })

        with elsewhen(io.data_type_ex_i == U.w(2)(0b01)):
            # Writing a half word
            with when(misaligned_st == Bool(False)):
                # non-misaligned case
                data_be <<= LookUpTable(data_addr_int[1:0], {
                    U.w(2)(0b00): U.w(4)(0b0011),
                    U.w(2)(0b01): U.w(4)(0b0110),
                    U.w(2)(0b10): U.w(4)(0b1100),
                    U.w(2)(0b11): U.w(4)(0b1000),
                    ...: U.w(4)(0b0011)
                })
            with otherwise():
                data_be <<= U.w(4)(0b0001)

        with elsewhen((io.data_type_ex_i == U.w(2)(0b10)) | (io.data_type_ex_i == U.w(2)(0b11))):
            # Writing a byte
            data_be <<= LookUpTable(data_addr_int[1:0], {
                U.w(2)(0b00): U.w(4)(0b0001),
                U.w(2)(0b01): U.w(4)(0b0010),
                U.w(2)(0b10): U.w(4)(0b0100),
                U.w(2)(0b11): U.w(4)(0b1000),
                ...: U.w(4)(0b0001)
            })

        # prepare data to be written to the memory
        # we handle misaligned accesses, half word and byte accesses and
        # register offsets here
        wdata_offset <<= data_addr_int[1:0] - io.data_reg_offset_ex_i[1:0]
        data_wdata <<= LookUpTable(wdata_offset, {
            U.w(2)(0b00): io.data_wdata_ex_i[31:0],
            U.w(2)(0b01): CatBits(io.data_wdata_ex_i[23:0], io.data_wdata_ex_i[31:24]),
            U.w(2)(0b10): CatBits(io.data_wdata_ex_i[15:0], io.data_wdata_ex_i[31:16]),
            U.w(2)(0b11): CatBits(io.data_wdata_ex_i[7:0], io.data_wdata_ex_i[31:8]),
            ...: io.data_wdata_ex_i[31:0]
        })

        # FF for rdata alignment and sign-extension
        data_type_q <<= io.data_type_ex_i
        rdata_offset_q <<= data_addr_int[1:0]
        data_sign_ext_q <<= io.data_sign_ext_ex_i
        data_we_q <<= io.data_we_ex_i
        data_load_event_q <<= io.data_load_event_ex_i

        # Load event starts when request is sent and finishes when (final) rvalid is received
        io.p_elw_start_o <<= io.data_load_event_ex_i & io.data_req_o
        io.p_elw_finish_o <<= data_load_event_q & io.data_rvalid_i & (~io.data_misaligned_ex_i)

        ##################################################################################
        # Sign Extension
        ##################################################################################

        data_rdata_ext = Wire(U.w(32))

        rdata_w_ext = Wire(U.w(32))         # Sign extension for words, actually only misaligned assembly
        rdata_h_ext = Wire(U.w(32))         # Sign extension for half words
        rdata_b_ext = Wire(U.w(32))         # Sign extension for bytes

        # Take care of misaligned words
        rdata_w_ext <<= LookUpTable(rdata_offset_q, {
            U.w(2)(0b00): resp_rdata[31:0],
            U.w(2)(0b01): CatBits(resp_rdata[7:0], rdata_q[31:8]),
            U.w(2)(0b10): CatBits(resp_rdata[15:0], rdata_q[31:16]),
            U.w(2)(0b11): CatBits(resp_rdata[23:0], rdata_q[31:24]),
            ...: resp_rdata[31:0]
        })

        # Sign extension for half words
        

    return LOAD_STORE_UNIT()
