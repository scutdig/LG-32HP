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

   Author Name: Guoyi Mo
   Date: 2021-03-03
   File Name: compressed_decoder.py
   Description: decode compressed instruction for if
"""

from pyhcl import *
from src.include.pkg import *


def compressed_decoder(FPU=0):
    class COMPRESSED_DECODER(Module):
        io = IO(
            instr_i=Input(U.w(32)),
            instr_o=Output(U.w(32)),
            is_compressed_o=Output(Bool),
            illegal_instr_o=Output(Bool)
        )

        ca_format = Wire(U.w(3))
        imm = Wire(U.w(6))
        imm <<= CatBits(io.instr_i[12], io.instr_i[6:2])
        ca_format <<= CatBits(io.instr_i[12], io.instr_i[6:5])

        io.illegal_instr_o <<= U.w(1)(0)
        io.instr_o <<= U(0)

        with when(io.instr_i[1:0] == U.w(2)(0)):
            with when(io.instr_i[15:13] == U.w(3)(0)):
                # c.addi4spn -> addi rd, x2, imm
                io.instr_o <<= CatBits(U.w(2)(0), io.instr_i[10:7], io.instr_i[12:11], io.instr_i[5], io.instr_i[6],
                                       U.w(2)(0), U.w(5)(0x2), U.w(3)(0), U.w(2)(1), io.instr_i[4:2], OPCODE_OPIMM)
                with when(io.instr_i[12:5] == U.w(8)(0)):
                    io.illegal_instr_o <<= U.w(1)(1)
            with elsewhen(io.instr_i[15:13] == U.w(3)(1)):
                # c.fld -> fld rd, imm(rs1)
                if FPU:
                    io.instr_o <<= CatBits(U.w(4)(0), io.instr_i[6:5], io.instr_i[12:10], U.w(3)(0), U.w(2)(1),
                                           io.instr_i[9:7], U.w(3)(3), U.w(2)(1), io.instr_i[4:2], OPCODE_LOAD_FP)
                else:
                    io.illegal_instr_o <<= U.w(1)(1)
            with elsewhen(io.instr_i[15:13] == U.w(3)(2)):
                # c.lw  -> lw rd, imm(rs1)
                io.instr_o <<= CatBits(U.w(5)(0), io.instr_i[5], io.instr_i[12:10], io.instr_i[6], U.w(2)(0), U.w(2)(1),
                                       io.instr_i[9:7], U.w(3)(2), U.w(2)(1), io.instr_i[4:2], OPCODE_LOAD)
            with elsewhen(io.instr_i[15:13] == U.w(3)(3)):
                # c.flw -> flw rd, imm(rs1)
                if FPU:
                    io.instr_o <<= CatBits(U.w(5)(0), io.instr_i[5], io.instr_i[12:10], io.instr_i[6], U.w(2)(0),
                                           U.w(2)(1), io.instr_i[9:7], U.w(3)(2), U.w(2)(1), io.instr_i[4:2], OPCODE_LOAD_FP)
                else:
                    io.illegal_instr_o <<= U.w(1)(1)
            with elsewhen(io.instr_i[15:13] == U.w(3)(5)):
                # c.fsd -> fsd rs2, imm(rs1)
                if FPU:
                    io.instr_o <<= CatBits(U.w(4)(0), io.instr_i[6:5], io.instr_i[12], U.w(2)(1), io.instr_i[4:2],
                                           U.w(2)(1), io.instr_i[9:7], U.w(3)(3), io.instr_i[11:10], U.w(3)(0), OPCODE_STORE_FP)
                else:
                    io.illegal_instr_o <<= U.w(1)(1)
            with elsewhen(io.instr_i[15:13] == U.w(3)(6)):
                # c.sw  -> sw rs2, imm(rs1)
                io.instr_o <<= CatBits(U.w(5)(0), io.instr_i[5], io.instr_i[12], U.w(2)(1), io.instr_i[4:2], U.w(2)(1),
                                       io.instr_i[9:7], U.w(3)(2), io.instr_i[11:10], io.instr_i[6], U.w(2)(0), OPCODE_STORE)
            with elsewhen(io.instr_i[15:13] == U.w(3)(7)):
                # c.fsw -> fsw rs2, imm(rs1)
                if FPU:
                    io.instr_o <<= CatBits(U.w(5)(0), io.instr_i[5], io.instr_i[12], U.w(2)(1), io.instr_i[4:2], U.w(2)(1),
                                           io.instr_i[9:7], U.w(3)(2), io.instr_i[11:10], io.instr_i[6], U.w(2)(0), OPCODE_STORE_FP)
                else:
                    io.illegal_instr_o <<= U.w(1)(1)
            with otherwise():
                io.illegal_instr_o <<= U.w(1)(1)
        with elsewhen(io.instr_i[1:0] == U.w(2)(1)):
            with when(io.instr_i[15:13] == U.w(3)(0)):
                # c.addi -> addi rd, rd, nzimm
                # c.nop
                io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                       io.instr_i[12], io.instr_i[12], io.instr_i[6:2], io.instr_i[11:7], U.w(3)(0),
                                       io.instr_i[11:7], OPCODE_OPIMM)
            with elsewhen(io.instr_i[15:13] == U.w(3)(1)):
                # c.jal -> jal x1, imm
                io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[8], io.instr_i[10:9], io.instr_i[6], io.instr_i[7],
                                       io.instr_i[2], io.instr_i[11], io.instr_i[5:3], io.instr_i[12], io.instr_i[12],
                                       io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                       io.instr_i[12], io.instr_i[12], U.w(4)(0), ~io.instr_i[15], OPCODE_JAL)
            with elsewhen(io.instr_i[15:13] == U.w(3)(2)):
                with when(io.instr_i[11:7] == U.w(5)(0)):
                    # Hint -> addi x0, x0, nzimm
                    io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                           io.instr_i[12], io.instr_i[12], io.instr_i[6:2], U.w(5)(0), U.w(3)(0),
                                           io.instr_i[11:7], OPCODE_OPIMM)
                with otherwise():
                    # c.li -> addi rd, x0, nzimm
                    io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                           io.instr_i[12], io.instr_i[12], io.instr_i[6:2], U.w(5)(0), U.w(3)(0),
                                           io.instr_i[11:7], OPCODE_OPIMM)
            with elsewhen(io.instr_i[15:13] == U.w(3)(3)):
                with when(imm == U.w(6)(0)):
                    io.illegal_instr_o <<= U.w(1)(1)
                with otherwise():
                    with when(io.instr_i[11:7] == U.w(5)(0x2)):
                        # c.addi16sp -> addi x2, x2, nzimm
                        io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[4:3],
                                               io.instr_i[5], io.instr_i[2], io.instr_i[6], U.w(4)(0), U.w(5)(0x2),
                                               U.w(3)(0), U.w(5)(0x2), OPCODE_OPIMM)
                    with elsewhen(io.instr_i[11:7] == U.w(5)(0)):
                        # Hint -> lui x0, imm
                        io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                               io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                               io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                               io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[6:2],
                                               io.instr_i[11:7], OPCODE_LUI)
                    with otherwise():
                        io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                               io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                               io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                               io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[6:2],
                                               io.instr_i[11:7], OPCODE_LUI)
            with elsewhen(io.instr_i[15:13] == U.w(3)(4)):
                with when(io.instr_i[11:10] == U.w(2)(0)):
                    # c.srli -> srli rd, rd, shamt
                    with when(io.instr_i[12] == U.w(1)(1)):
                        # Reserved for future custom extensions
                        io.illegal_instr_o <<= U.w(1)(1)
                        io.instr_o <<= CatBits(U.w(1)(0), io.instr_i[10], U.w(5)(0), io.instr_i[6:2], U.w(2)(1),
                                               io.instr_i[9:7], U.w(3)(5), U.w(2)(1), io.instr_i[9:7], OPCODE_OPIMM)
                    with otherwise():
                        with when(io.instr_i[6:2] == U.w(5)(0)):
                            io.instr_o <<= CatBits(U.w(1)(0), io.instr_i[10], U.w(5)(0), io.instr_i[6:2], U.w(2)(1),
                                                   io.instr_i[9:7], U.w(3)(5), U.w(2)(1), io.instr_i[9:7], OPCODE_OPIMM)
                        with otherwise():
                            io.instr_o <<= CatBits(U.w(1)(0), io.instr_i[10], U.w(5)(0), io.instr_i[6:2], U.w(2)(1),
                                                   io.instr_i[9:7], U.w(3)(5), U.w(2)(1), io.instr_i[9:7], OPCODE_OPIMM)
                with elsewhen(io.instr_i[11:10] == U.w(2)(1)):
                    # c.srai -> srai rd, rd, shamt
                    with when(io.instr_i[12] == U.w(1)(1)):
                        # Reserved for future custom extensions
                        io.illegal_instr_o <<= U.w(1)(1)
                        io.instr_o <<= CatBits(U.w(1)(0), io.instr_i[10], U.w(5)(0), io.instr_i[6:2], U.w(2)(1),
                                               io.instr_i[9:7], U.w(3)(5), U.w(2)(1), io.instr_i[9:7], OPCODE_OPIMM)
                    with otherwise():
                        with when(io.instr_i[6:2] == U.w(5)(0)):
                            io.instr_o <<= CatBits(U.w(1)(0), io.instr_i[10], U.w(5)(0), io.instr_i[6:2], U.w(2)(1),
                                                   io.instr_i[9:7], U.w(3)(5), U.w(2)(1), io.instr_i[9:7], OPCODE_OPIMM)
                        with otherwise():
                            io.instr_o <<= CatBits(U.w(1)(0), io.instr_i[10], U.w(5)(0), io.instr_i[6:2], U.w(2)(1),
                                                   io.instr_i[9:7], U.w(3)(5), U.w(2)(1), io.instr_i[9:7], OPCODE_OPIMM)
                with elsewhen(io.instr_i[11:10] == U.w(2)(2)):
                    # c.andi -> andi rd, rd, imm
                    io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                           io.instr_i[12], io.instr_i[12], io.instr_i[6:2], U.w(2)(1), io.instr_i[9:7],
                                           U.w(3)(7), U.w(2)(1), io.instr_i[9:7], OPCODE_OPIMM)
                with elsewhen(io.instr_i[11:10] == U.w(2)(3)):
                    with when(ca_format == U.w(3)(0)):
                        # c.sub -> sub rd, rd, rs2
                        io.instr_o <<= CatBits(U.w(2)(1), U.w(5)(0), U.w(2)(1), io.instr_i[4:2], U.w(2)(1), io.instr_i[9:7],
                                               U.w(3)(0), U.w(2)(1), io.instr_i[9:7], OPCODE_OP)
                    with elsewhen(ca_format == U.w(3)(1)):
                        # c.xor -> xor rd, rd, rs2
                        io.instr_o <<= CatBits(U.w(7)(0), U.w(2)(1), io.instr_i[4:2], U.w(2)(1), io.instr_i[9:7],
                                               U.w(3)(4), U.w(2)(1), io.instr_i[9:7], OPCODE_OP)
                    with elsewhen(ca_format == U.w(3)(2)):
                        # c.or -> or rd, rd, rs2
                        io.instr_o <<= CatBits(U.w(7)(0), U.w(2)(1), io.instr_i[4:2], U.w(2)(1), io.instr_i[9:7],
                                               U.w(3)(6), U.w(2)(1), io.instr_i[9:7], OPCODE_OP)
                    with elsewhen(ca_format == U.w(3)(3)):
                        # c.and -> and rd, rd, rs2
                        io.instr_o <<= CatBits(U.w(7)(0), U.w(2)(1), io.instr_i[4:2], U.w(2)(1), io.instr_i[9:7],
                                               U.w(3)(7), U.w(2)(1), io.instr_i[9:7], OPCODE_OP)
                    with otherwise():
                        io.illegal_instr_o <<= U.w(1)(1)
            with elsewhen(io.instr_i[15:13] == U.w(3)(5)):
                # c.j   -> jal x0, imm
                io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[8], io.instr_i[10:9], io.instr_i[6], io.instr_i[7],
                                       io.instr_i[2], io.instr_i[11], io.instr_i[5:3], io.instr_i[12], io.instr_i[12],
                                       io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12],
                                       io.instr_i[12], io.instr_i[12], U.w(4)(0), ~io.instr_i[15], OPCODE_JAL)
            with elsewhen(io.instr_i[15:13] == U.w(3)(6)):
                # c.beqz -> beq rs1, x0, imm
                io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[6:5],
                                       io.instr_i[2], U.w(5)(0), U.w(2)(1), io.instr_i[9:7], U.w(2)(0), io.instr_i[13],
                                       io.instr_i[11:10], io.instr_i[4:3], io.instr_i[12], OPCODE_BRANCH)
            with elsewhen(io.instr_i[15:13] == U.w(3)(7)):
                # c.bnez -> bne rs1, x0, imm
                io.instr_o <<= CatBits(io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[12], io.instr_i[6:5],
                                       io.instr_i[2], U.w(5)(0), U.w(2)(1), io.instr_i[9:7], U.w(2)(0), io.instr_i[13],
                                       io.instr_i[11:10], io.instr_i[4:3], io.instr_i[12], OPCODE_BRANCH)
        with elsewhen(io.instr_i[1:0] == U.w(2)(2)):
            with when(io.instr_i[15:13] == U.w(3)(0)):
                with when(io.instr_i[12] == U.w(1)(1)):
                    # Reserved for future extensions
                    io.instr_o <<= CatBits(U.w(7)(0), io.instr_i[6:2], io.instr_i[11:7], U.w(3)(1), io.instr_i[11:7],
                                           OPCODE_OPIMM)
                    io.illegal_instr_o << U.w(1)(1)
                with otherwise():
                    with when(io.instr_i[6:2] == U.w(5)(0) | io.instr_i[11:7] == U.w(5)(0)):
                        # Hint -> slli rd, rd, shamt
                        io.instr_o <<= CatBits(U.w(7)(0), io.instr_i[6:2], io.instr_i[11:7], U.w(3)(1), io.instr_i[11:7],
                                               OPCODE_OPIMM)
                    with otherwise():
                        # c.slli -> slli rd, rd, shamt
                        io.instr_o <<= CatBits(U.w(7)(0), io.instr_i[6:2], io.instr_i[11:7], U.w(3)(1), io.instr_i[11:7],
                                               OPCODE_OPIMM)
            with elsewhen(io.instr_i[15:13] == U.w(3)(1)):
                # c.fldsp -> fld rd, imm(x2)
                if FPU:
                    io.instr_o <<= CatBits(U.w(3)(0), io.instr_i[4:2], io.instr_i[12], io.instr_i[6:5], U.w(3)(0),
                                           U.w(5)(0x2), U.w(3)(3), io.instr_i[11:7], OPCODE_LOAD_FP)
                else:
                    io.illegal_instr_o <<= U.w(1)(1)
            with elsewhen(io.instr_i[15:13] == U.w(3)(2)):
                # c.lwsp -> lw rd, imm(x2)
                io.instr_o <<= CatBits(U.w(4)(0), io.instr_i[3:2], io.instr_i[12], io.instr_i[6:4], U.w(2)(0), U.w(5)(0x2),
                                       U.w(3)(2), io.instr_i[11:7], OPCODE_LOAD)
                with when(io.instr_i[11:7] == U.w(5)(0)):
                    io.illegal_instr_o <<= U.w(1)(1)
            with elsewhen(io.instr_i[15:13] == U.w(3)(3)):
                # c.flwsp -> flw rd, imm(x2)
                if FPU:
                    io.instr_o <<= CatBits(U.w(4)(0), io.instr_i[3:2], io.instr_i[12], io.instr_i[6:4], U.w(2)(0),
                                           U.w(5)(0x2), U.w(3)(2), io.instr_i[11:7], OPCODE_LOAD_FP)
                else:
                    io.illegal_instr_o <<= U.w(1)(1)
            with elsewhen(io.instr_i[15:13] == U.w(3)(4)):
                with when(io.instr_i[12] == U.w(1)(0)):
                    with when(io.instr_i[6:2] == U.w(5)(0)):
                        # c.jr -> jalr x0, rd/rs1, 0
                        io.instr_o <<= CatBits(U.w(12)(0), io.instr_i[11:7], U.w(3)(0), U.w(5)(0), OPCODE_JALR)
                        # c.jr with rs1 = 0 is reserved
                        with when(io.instr_i[11:7] == U.w(5)(0)):
                            io.illegal_instr_o <<= U.w(1)(1)
                    with otherwise():
                        with when(io.instr_i[11:7] == U.w(5)(0)):
                            # Hint -> add x0, x0, rs2
                            io.instr_o <<= CatBits(U.w(7)(0), io.instr_i[6:2], U.w(5)(0), U.w(3)(0), io.instr_i[11:7],
                                                   OPCODE_OP)
                        with otherwise():
                            # c.mv -> add rd, x0, rs2
                            io.instr_o <<= CatBits(U.w(7)(0), io.instr_i[6:2], U.w(5)(0), U.w(3)(0), io.instr_i[11:7],
                            OPCODE_OP)
                with otherwise():
                    with when(io.instr_i[6:2] == U.w(5)(0)):
                        with when(io.instr_i[11:7] == U.w(5)(0)):
                            # c.ebreak -> ebreak
                            io.instr_o <<= CatBits(U.w(32)(0x00100073))
                        with otherwise():
                            # c.jalr -> jalr x1, rs1, 0
                            io.instr_o <<= CatBits(U.w(12)(0), io.instr_i[11:7], U.w(3)(0), U.w(5)(1), OPCODE_JALR)
                    with otherwise():
                        with when(io.instr_i[11:7] == U.w(5)(0)):
                            # Hint -> add x0, x0, rs2
                            io.instr_o <<= CatBits(U.w(7)(0), io.instr_i[6:2], io.instr_i[11:7], U.w(3)(0),
                                                   io.instr_i[11:7], OPCODE_OP)
                        with otherwise():
                            io.instr_o <<= CatBits(U.w(7)(0), io.instr_i[6:2], io.instr_i[11:7], U.w(3)(0),
                                                   io.instr_i[11:7], OPCODE_OP)
            with elsewhen(io.instr_i[15:13] == U.w(3)(5)):
                # c.fsdsp -> fsd rs2, imm(x2)
                if FPU:
                    io.instr_o <<= CatBits(U.w(3)(0), io.instr_i[9:7], io.instr_i[12], io.instr_i[6:2], U.w(5)(0x2),
                                           U.w(3)(3), io.instr_i[11:10], U.w(3)(0), OPCODE_STORE_FP)
                else:
                    io.illegal_instr_o <<= U.w(1)(1)
            with elsewhen(io.instr_i[15:13] == U.w(3)(6)):
                # c.swsp -> sw rs2, imm(x2)
                io.instr_o <<= CatBits(U.w(4)(0), io.instr_i[8:7], io.instr_i[12], io.instr_i[6:2], U.w(5)(0x2),
                                       U.w(3)(2), io.instr_i[11:9], U.w(2)(0), OPCODE_STORE)
            with elsewhen(io.instr_i[15:13] == U.w(3)(7)):
                # c.fswsp -> fsw rs2, imm(x2)
                if FPU:
                    io.instr_o <<= CatBits(U.w(4)(0), io.instr_i[8:7], io.instr_i[12], io.instr_i[6:2], U.w(5)(0x2),
                                           U.w(3)(2), io.instr_i[11:9], U.w(2)(0), OPCODE_STORE_FP)
                else:
                    io.illegal_instr_o <<= U.w(1)(1)
        with otherwise():
            io.instr_o <<= io.instr_i

        io.is_compressed_o <<= io.instr_i[1:0] != U.w(2)(3)

    return COMPRESSED_DECODER()


if __name__ == '__main__':
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(compressed_decoder(1)), "compressed_decoder.fir"))
