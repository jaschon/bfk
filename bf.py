#!/usr/bin/env python3
#Jaschon 2023


class BF_K:

    def __init__(self, pgm):
        self.pgm = pgm 
        self.ptr = 0
        self.counter = 0
        self.stack = []
        self.cells = [0]

    def _plus(self):
        self.cells[self.ptr] += 1

    def _minus(self):
        self.cells[self.ptr] -= 1

    def _cell_r(self):
        self.ptr += 1
        if self.ptr >= len(self.cells):
            self.cells.append(0)

    def _cell_l(self):
        self.ptr = self.ptr-1 if self.ptr > 0 else 0

    def _loop_l(self):
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
        if self.cells[self.ptr] != 0:
            self.counter = self.stack[-1]
        else:
            self.stack.pop()

    def _out(self):
        print(chr(self.cells[self.ptr]), end="")

    def _in(self):
        self.cells[self.ptr] = input()[0]

    def run(self):
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
            # print(self.pgm[self.counter], self.cells, f"cell={self.ptr}", f"pgm={self.counter}", self.stack)
            # input()
            self.counter+=1

if __name__ == "__main__":

    # quick hello world tests
    b = BF_K(">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-] <.#>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[ <++++>-]<+.[-]++++++++++.").run()
    b = BF_K("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.").run()

    # 7 test
    b = BF_K("++ > +++++ [< +> -]   ++++ ++++[< +++ +++ > - ]< .").run()
    print()

