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
   Date: 2021-05-07
   File Name: utils.py
   Description: Utils functions for processor implementations
"""
from math import *
from pyhcl import *


class ff:
    def __init__(self, width, v):
        self.q = RegInit(U.w(width)(v))
        self.n = Wire(U.w(width))


class packed_ff:
    def __init__(self, q, n):
        self.q = q
        self.n = n


def gen_ff(width, v):
    """
        args:
            width: Signal's width
            v: Register's initial value
    """
    return ff(width, v)


def gen_packed_ff(q, n):
    """
        args:
            q: State elements packed subject
            n: Non-state elements packed subject
    """
    return packed_ff(q, n)


def vec_init(size, el, init):
    tmp = Reg(Vec(size, el))
    for i in range(size):
        tmp[i] <<= init
    return tmp


def vec_init_wire(size, el, init):
    tmp = Wire(Vec(size, el))
    for i in range(size):
        tmp[i] <<= init
    return tmp


def vec_assign(size, v, rhs):
    for i in range(size):
        v[i] <<= rhs[i]


def clog2(v):
    return ceil(log(v, 2))


def reduce_or(el, width):
    tmp = el[width-1]
    for i in range(width-2, -1, -1):
        tmp = tmp | el[i]
    return tmp


# For Log2
divideAndConquerThreshold = 4


def Log2(x, width: int):
    """
        Returns the base-2 integer logarithm of the least-significant width bits of an UInt
    """
    if width < 2:
        return U(0)
    elif width == 2:
        return x[1]
    elif width <= divideAndConquerThreshold:
        return Mux(x[width-1], U(width-1), Log2(x, width-1))
    else:
        mid = int(1 << (clog2(width) - 1))
        hi = x[width-1:mid]
        lo = x[mid-1:0]
        useHi = reduce_or(hi, width - mid)
        return CatBits(useHi, Mux(useHi, Log2(hi, width - mid), Log2(lo, mid)))
