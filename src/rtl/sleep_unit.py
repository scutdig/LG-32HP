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
   Date: 2021-04-12
   File Name: sleep_unit.py
   Description: Sleep unit containing the instantiated clock gate which
                provides the gated clock (clk_gated_o) for the rest
                of the design.

                The clock is gated for the following scenarios:

                - While waiting for fetch to become enabled
                - While blocked on a WFI (PULP_CLUSTER = 0)
                - While clock_en_i = 0 during a p.elw (PULP_CLUSTER = 1)

                Sleep is signaled via core_sleep_o when:

                - During a p.elw (except in debug (i.e. pending debug
                  request, debug mode, single stepping, trigger match)
                - During a WFI (except in debug)
"""
from pyhcl import *


# This module has gated clock, need to modify the firrtl
# or use blackbox
def sleep_unit():
    class SLEEP_UNIT(Module):
        io = IO()

    return SLEEP_UNIT()
