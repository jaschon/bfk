#!/usr/bin/env python3

import sys

__author__ = "jaschon"
__copyright__ = "2023"

class BFK:
    """brainf*ck programming language interpreter"""

    def __init__(self, pgm):
        self.pgm = pgm
        self.pos = 0
        self.ptr = 0
        self.mem = [0]*3000
        self.stack = []

    def _plus(self):
        """opt code for + char"""
        self.mem[self.ptr] = -128 if self.mem[self.ptr] == 127 else self.mem[self.ptr] + 1

    def _minus(self):
        """opt code for - char"""
        self.mem[self.ptr] = 127 if self.mem[self.ptr] == -128 else self.mem[self.ptr] - 1

    def _cell_r(self):
        """opt code for > char"""
        self.ptr = (self.ptr+1) % len(self.mem)

    def _cell_l(self):
        """opt code for < char"""
        self.ptr = (self.ptr-1) % len(self.mem)

    def _loop_l(self):
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

    def _loop_r(self):
        """opt code for ] char"""
        if self.mem[self.ptr] != 0:
            self.pos = self.stack[-1]
        else:
            self.stack.pop()

    def _output(self):
        """opt code for . char"""
        print(self._convert(self.mem[self.ptr]), end="")

    def _input(self):
        """opt code for , char"""
        self.mem[self.ptr] = ord(sys.stdin.read(1)) % 127

    def _debug(self):
        """debug info"""
        print(f"\nPOS: {self.pos} PTR: {self.ptr} VAL: {self.mem[self.ptr]}")

    def _convert(self, num):
        """converts -128->127 number to utf"""
        return chr((num % 65536) if num > 0 else num + 65536)

    def step(self):
        """run single character opt code at pgm pos"""
        match self.pgm[self.pos]:
            case "+": self._plus()
            case "-": self._minus()
            case ">": self._cell_r()
            case "<": self._cell_l()
            case "[": self._loop_l()
            case "]": self._loop_r()
            case ".": self._output()
            case ",": self._input()
            case "#": self._debug()
            case _: pass
        self.pos+=1

    def run(self):
        """run pgm code"""
        while self.pos < len(self.pgm):
            self.step()
     
if __name__ == "__main__":
    pass
