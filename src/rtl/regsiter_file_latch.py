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
   Date: 2021-03-08
   File Name: register_file_latch.py
   Description: "Register file with 31x 32 bit wide registers. Register 0
                is fixed to 0. This register file is based on latches and
                is thus smaller than the flip-flop based register file.
                Also supports the fp-register file now if FPU=1
                If PULP_ZFINX is 1, floating point operations take values
                from the X register file" -- Original RI5CY annotation
"""

"""
    NOTICE: PyHCL doesn't support latch
    If you need register file based on latch, please directly use the 
    original RI5SY Code as blackbox and interact with your own pipeline.
"""
