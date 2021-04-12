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


def fifo(FALL_THROUGH=0, DATA_WIDTH=32, DEPTH=8):
    """
        args:
            FALL_THROUGH: fifo is in fall-through mode
            DATA_WIDTH: default data width if the fifo is of type
            DEPTH: depth can be arbitrary from 0 to 2**32
    """
    ADDR_DEPTH = int(log(DEPTH, 2)) if DEPTH > 1 else 1
    FIFO_DEPTH = DEPTH if DEPTH > 0 else 1
    assert 0 <= FALL_THROUGH <= 1

    class FIFO(Module):
        # local parameter
        # FIFO depth - handle the case of pass-through, synthesizer will do constant propagation

        io = IO(
            flush_i=Input(Bool),            # flush the queue
            flush_but_first_i=Input(Bool),  # flush the queue except the first instruction
            testmode_i=Input(Bool),         # test_mode to bypass clock gating

            # status flags
            full_o=Output(Bool),            # queue is full
            empty_o=Output(Bool),           # queue is empty
            cnt_o=Output(U.w(ADDR_DEPTH+1)),  # FIFO counter

            # The queue is not full, push new data
            data_i=Input(U.w(DATA_WIDTH)),  # data to push into the queue
            push_i=Input(Bool),             # data is valid and can be pushed to the queue

            #  The queue is not empty, pop data
            data_o=Output(U.w(DATA_WIDTH)),     # output data
            pop_i=Input(Bool),                  # pop head form queue
        )

        # Clock gating control
        gate_clock = Wire(Bool)

        # Pointer to the read and write section of the queue
        read_pointer_q, write_pointer_q = [RegInit(U.w(ADDR_DEPTH)(0)) for _ in range(2)]
        read_pointer_n, write_pointer_n = [Wire(U.w(ADDR_DEPTH)) for _ in range(2)]

        # Keep a counter to keep track of the current queue status
        status_cnt_q = RegInit(U.w(ADDR_DEPTH+1)(0))
        status_cnt_n = Wire(U.w(ADDR_DEPTH+1))

        # Actual memory
        mem_q = Reg(Vec(FIFO_DEPTH, U.w(DATA_WIDTH)))
        mem_n = Wire(Vec(FIFO_DEPTH, U.w(DATA_WIDTH)))

        # keep data_i
        data_in = Reg(U.w(DATA_WIDTH))
        data_in <<= io.data_i

        io.cnt_o <<= status_cnt_q

        # Status flags
        if DEPTH == 0:
            io.empty_o <<= ~io.push_i
            io.full_o <<= ~io.pop_i
        else:
            io.empty_o <<= (status_cnt_q == U(0)) & (~(U.w(1)(FALL_THROUGH) & io.push_i))
            io.full_o <<= (status_cnt_q[ADDR_DEPTH:0] == U(FIFO_DEPTH))

        # Read and write the queue logic
        read_pointer_n <<= read_pointer_q
        write_pointer_n <<= write_pointer_q
        status_cnt_n <<= status_cnt_q
        io.data_o <<= io.data_i if DEPTH == 0 else mem_q[read_pointer_q]
        mem_n <<= mem_q
        gate_clock <<= U.w(1)(1)

        # Push a new element to the queue
        with when(io.push_i & (~io.full_o)):
            # Push the data onto the queue
            mem_n[write_pointer_q] <<= data_in
            # Un-gate the clock, we want to write something
            gate_clock <<= U.w(1)(0)
            # Increment the write counter
            with when(write_pointer_q == U.w(ADDR_DEPTH)(FIFO_DEPTH-1)):
                write_pointer_n <<= U(0)
            with otherwise():
                write_pointer_n <<= write_pointer_q + U(1)
            # Increment the overall counter
            # status_cnt_q/n width = ADDR_DEPTH+1, ignore overflow/underflow
            status_cnt_n <<= status_cnt_q + U(1)

        # Read from the queue
        with when(io.pop_i & (~io.empty_o)):
            with when(read_pointer_q == U.w(ADDR_DEPTH)(FIFO_DEPTH-1)):
                read_pointer_n <<= U(0)
            with otherwise():
                read_pointer_n <<= read_pointer_q + U(1)
            # Decrement the overall counter
            status_cnt_n <<= status_cnt_q - U(1)

        # Keep the count pointer stable if we push and pop at the same time
        with when(io.push_i & io.pop_i & (~io.full_o) & (~io.empty_o)):
            status_cnt_n <<= status_cnt_q

        # FIFO is in pass through mode -> do not change the pointers
        with when(U.w(1)(FALL_THROUGH) & (status_cnt_q == U(0)) & io.push_i):
            io.data_o <<= io.data_i
            with when(io.pop_i):
                status_cnt_n <<= status_cnt_q
                read_pointer_n <<= read_pointer_q
                write_pointer_n <<= write_pointer_q

        # Sequential process
        with when(Module.reset):
            read_pointer_q <<= U(0)
            write_pointer_q <<= U(0)
            status_cnt_q <<= U(0)
        with elsewhen(io.flush_i):
            # Flush the FIFO
            read_pointer_q <<= U(0)
            write_pointer_q <<= U(0)
            status_cnt_q <<= U(0)
        with elsewhen(io.flush_but_first_i):
            # Flush the FIFO but keep the first instruction alive if present
            read_pointer_q <<= Mux(status_cnt_q > U(0), read_pointer_q, U(0))
            write_pointer_q <<= Mux(status_cnt_q > U(0), read_pointer_q + U(1), U(0))
            status_cnt_q <<= Mux(status_cnt_q > U(0), U(1), U(0))
        with otherwise():
            # Default
            read_pointer_q <<= read_pointer_n
            write_pointer_q <<= write_pointer_n
            status_cnt_q <<= status_cnt_n

        with when(Module.reset):
            for i in range(FIFO_DEPTH):
                mem_q[i] <<= U(0)
        with elsewhen(~gate_clock):
            # mem_q <<= mem_n
            for i in range(FIFO_DEPTH):
                mem_q[i] <<= mem_n[i]

    return FIFO()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(fifo()), "fifo.fir"))
