#!/usr/bin/env python3
"""Unittests for BFK"""

import sys
import pytest
sys.path.append('..')
from bfk import BFK

#TEST Class
class BFKTest(BFK):
    """Capture Output For Testing"""

    def __init__(self, pgm):
        """Init and Start Capture"""
        self.out = []
        super().__init__(pgm)

    def output(self):
        """Capture Output"""
        self.out.append(self.convert(self.mem[self.ptr]))

    def test(self):
        """Join Output for Test"""
        return "".join(self.out)


class TestRunProgram:
    """Test Running Programs"""

    def test_hello(self):
        """Test Hello World #1"""
        bfk = BFKTest("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+"
            "[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.")
        bfk.run()
        assert bfk.test() == "Hello World!\n"

    def test_hello2(self):
        """Test Hello World #2"""
        bfk = BFKTest("+[-->-[>>+>-----<<]<--<---]>-.>>>+.>>..+++[.>]<<<<.+++.------.<<-.>>>>+.")
        bfk.run()
        assert bfk.test() == "Hello, World!"


class TestConvert:
    """Test Convert Number to Character"""

    @pytest.mark.parametrize("num", [-128, -1, -129])
    def test_characters_neg_wrap(self, num):
        """test neg value chacter conversion"""
        assert BFK().convert(num) == chr(65536+num)

    @pytest.mark.parametrize("num", [128, 127, 1, 0, 10, 30, 103, 200, 65536])
    def test_characters_pos_wrap(self, num):
        """test neg value chacter conversion"""
        assert BFK().convert(num) == chr(num % 65536)


class TestRun:
    """Test Run Problems"""

    def test_bad_opcodes_all(self):
        """Test Skip Bad Opcodes"""
        #Hidden Loop: ++[>+<-]
        pgm = """
        ABC++D[EFG&>*()+&*)(&)<-ZEHD]KSL
        """
        bfk = BFK(pgm)
        bfk.run()
        assert bfk.pos == len(pgm)
        assert bfk.ptr == 0
        assert bfk.mem[0] == 0
        assert bfk.mem[1] == 2

class TestPlus:
    """Test Plus"""

    def test_plus(self):
        """Test Plus Method"""
        bfk = BFK()
        bfk.plus()
        assert bfk.mem[bfk.ptr] == 1

    def test_plus_run(self):
        """Test Plus Run"""
        bfk = BFK("+")
        bfk.run()
        assert bfk.mem[bfk.ptr] == 1

    def test_plus_wrap(self):
        """Test Plus Wrap"""
        bfk = BFK()
        bfk.mem[bfk.ptr] = 127
        bfk.plus()
        assert bfk.mem[bfk.ptr] == -128


class TestMinus:
    """Test Minus"""

    def test_minus(self):
        """Test Minus Method"""
        bfk = BFK()
        bfk.minus()
        assert bfk.mem[bfk.ptr] == -1

    def test_minus_run(self):
        """Test Minus Run"""
        bfk = BFK("-")
        bfk.run()
        assert bfk.mem[bfk.ptr] == -1

    def test_minus_wrap(self):
        """Test Minus Wrap"""
        bfk = BFK()
        bfk.mem[bfk.ptr] = -128
        bfk.minus()
        assert bfk.mem[bfk.ptr] == 127

class TestLeftMemShift:
    """Test Left Mem Shift"""

    def test_mem_l(self):
        """Test Mem Left Method"""
        bfk = BFK()
        bfk.ptr = 1
        bfk.cell_l()
        assert bfk.ptr == 0

    def test_cell_l_run(self):
        """Test Cell Left Run"""
        bfk = BFK("<")
        bfk.ptr = 1
        bfk.run()
        assert bfk.ptr == 0

    def test_cell_l_wrap(self):
        """Test Cell Left Wrap"""
        bfk = BFK()
        bfk.cell_l()
        assert bfk.ptr == len(bfk.mem)-1

class TestRightMemShift:
    """Test Right Mem Shift"""

    def test_cell_r(self):
        """Test Cell Right Method"""
        bfk = BFK()
        bfk.cell_r()
        assert bfk.ptr == 1

    def test_cell_r_run(self):
        """Test Cell Right Run"""
        bfk = BFK(">")
        bfk.run()
        assert bfk.ptr == 1

    def test_cell_r_wrap(self):
        """Test Cell Right Wrap"""
        bfk = BFK()
        bfk.ptr = len(bfk.mem)-2
        bfk.cell_r()
        assert bfk.ptr == len(bfk.mem)-1

class TestLoops:
    """Test Loops"""
    def test_loop_skip(self):
        """Test Loop Skip"""
        # Should Skip Loop
        bfk = BFK("[+++]+")
        bfk.run()
        assert bfk.mem[bfk.ptr] == 1

    def test_loop_broken(self):
        """Test Loop Broken"""
        # Should Enter First Loop, Run Second Loop Twice and Quit
        bfk = BFK("++[>++[>+<-]<-")
        bfk.run()
        assert bfk.mem[2] == 2

    def test_loop_enter(self):
        """Test Loop Enter"""
        # Should Enter Loop and Run Twice
        bfk = BFK("++[>+<-]")
        bfk.run()
        assert bfk.mem[1] == 2

    def test_loop_double(self):
        """Test Double Loop"""
        bfk = BFK("++[>++[>+<-]<-]")
        bfk.run()
        assert bfk.mem[2] == 4

    def test_loop_triple(self):
        """Test Triple Loop"""
        bfk = BFK("++[>++[>++[>+<-]<-]<-]")
        bfk.run()
        assert bfk.mem[3] == 8
