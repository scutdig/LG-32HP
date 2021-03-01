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
   File Name: fifo.py
   Description: FIFO data structure for prefetch buffer.
"""
from math import log
from pyhcl import *


def fifo(FALL_THROUGH=U.w(1)(0), DATA_WIDTH=32, DEPTH=8):
    """
        args:
            FALL_THROUGH: fifo is in fall-through mode
            DATA_WIDTH: default data width if the fifo is of type
            DEPTH: depth can be arbitrary from 0 to 2**32
    """
    ADDR_DEPTH = int(log(DEPTH, 2)) if DEPTH > 1 else 1

    class FIFO(Module):
        io = IO(
            flush_i=Input(Bool),            # flush the queue
            flush_but_first_i=Input(Bool),  # flush the queue except the first instruction
            testmode_i=Input(Bool),         # test_mode to bypass clock gating

            # status flags
            full_o=Output(Bool),            # queue is full
            empty_o=Output(Bool),           # queue is empty
            cnt_o=Output(U.w(ADDR_DEPTH)),  # FIFO counter

            # The queue is not full, push new data
            data_i=Input(U.w(DATA_WIDTH)),  # data to push into the queue
            push_i=Input(Bool),             # data is valid and can be pushed to the queue

            #  The queue is not empty, pop data
            data_o=Output(U.w(DATA_WIDTH)),     # output data
            pop_i=Input(Bool),                  # pop head form queue
        )

    return FIFO()
