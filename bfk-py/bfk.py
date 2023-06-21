#!/usr/bin/env python3
"""brainf*ck programming language interpreter"""

import sys

__author__ = "jaschon"
__copyright__ = "2023"

class BFK:
    """brainf*ck programming language interpreter"""

    def __init__(self, pgm=""):
        self.pgm = pgm
        self.pos = 0
        self.ptr = 0
        self.mem = [0]*3000
        self.stack = []

    def plus(self):
        """opt code for + char"""
        self.mem[self.ptr] = -128 if self.mem[self.ptr] == 127 else self.mem[self.ptr] + 1

    def minus(self):
        """opt code for - char"""
        self.mem[self.ptr] = 127 if self.mem[self.ptr] == -128 else self.mem[self.ptr] - 1

    def cell_r(self):
        """opt code for > char"""
        self.ptr = (self.ptr+1) % len(self.mem)

    def cell_l(self):
        """opt code for < char"""
        self.ptr = (self.ptr-1) % len(self.mem)

    def loop_l(self):
        """opt code for [ char"""
        if self.mem[self.ptr] != 0:
            self.stack.append(self.pos)
        else:
            stk = []
            while self.pos < len(self.pgm):
                if self.pgm[self.pos] == "[":
                    stk.append(self.pos)
                elif self.pgm[self.pos] == "]":
                    stk.pop()
                    if len(stk) == 0:
                        break
                self.pos += 1

    def loop_r(self):
        """opt code for ] char"""
        if self.mem[self.ptr] != 0:
            self.pos = self.stack[-1]
        else:
            self.stack.pop()

    def output(self):
        """opt code for . char"""
        print(self.convert(self.mem[self.ptr]), end="")

    def input(self):
        """opt code for , char"""
        self.mem[self.ptr] = ord(sys.stdin.read(1)) % 127

    def debug(self):
        """debug info"""
        print(f"\nPOS: {self.pos} PTR: {self.ptr} VAL: {self.mem[self.ptr]}")

    def convert(self, num):
        """converts -128->127 number to utf"""
        return chr((num % 65536) if num > -1 else num + 65536)

    def step(self):
        """run single character opt code at pgm pos"""
        match self.pgm[self.pos]:
            case "+": self.plus()
            case "-": self.minus()
            case ">": self.cell_r()
            case "<": self.cell_l()
            case "[": self.loop_l()
            case "]": self.loop_r()
            case ".": self.output()
            case ",": self.input()
            case "#": self.debug()
            case _: pass
        self.pos+=1

    def run(self):
        """run pgm code"""
        while self.pos < len(self.pgm):
            self.step()
