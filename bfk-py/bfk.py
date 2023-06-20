#!/usr/bin/env python3
"""brainf*ck programming language interpreter"""

import sys

__author__ = "jaschon"
__copyright__ = "2023"

class BFK:
    def __init__(self, pgm):
        self.pgm = pgm
        self.ptr = 0
        self.counter = 0
        self.stack = []
        self.cells = [0]

    def _plus(self):
        """opt code for + char"""
        self.cells[self.ptr] = 0 if self.cells[self.ptr] == 127 else self.cells[self.ptr] + 1

    def _minus(self):
        """opt code for - char"""
        self.cells[self.ptr] = 127 if self.cells[self.ptr] == 0 else self.cells[self.ptr] - 1

    def _cell_r(self):
        """opt code for > char"""
        self.ptr += 1
        if self.ptr >= len(self.cells):
            self.cells.append(0)

    def _cell_l(self):
        """opt code for < char"""
        self.ptr = self.ptr-1 if self.ptr > 0 else 0

    def _loop_l(self):
        """opt code for [ char"""
        if self.cells[self.ptr] != 0:
            self.stack.append(self.counter)
        else:
            stk = []
            while self.counter < len(self.pgm):
                if self.pgm[self.counter] == "[":
                    stk.append(self.counter)
                elif self.pgm[self.counter] == "]":
                    stk.pop()
                    if len(stk) == 0:
                        break
                self.counter += 1

    def _loop_r(self):
        """opt code for ] char"""
        if self.cells[self.ptr] != 0:
            self.counter = self.stack[-1]
        else:
            self.stack.pop()

    def _out(self):
        """opt code for . char"""
        print(chr(self.cells[self.ptr]), end="")

    def _in(self):
        """opt code for , char"""
        self.cells[self.ptr] = ord(sys.stdin.read(1))

    def run(self):
        """run each character opt code"""
        while self.counter < len(self.pgm):
            match self.pgm[self.counter]:
                case "+": self._plus()
                case "-": self._minus()
                case ">": self._cell_r()
                case "<": self._cell_l()
                case "[": self._loop_l()
                case "]": self._loop_r()
                case ".": self._out()
                case ",": self._in()
                case _: pass
            self.counter+=1

if __name__ == "__main__":
    BFK("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.").run()
