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


def clog2(v):
    return ceil(log(v, 2))
