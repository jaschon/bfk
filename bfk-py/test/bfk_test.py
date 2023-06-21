#!/usr/bin/env python3

import sys
import pytest
sys.path.append('..')
from bfk import BFK


class TestMethods:
    """Test Helper Methods"""

    @pytest.mark.parametrize("num", [-128, 0, -1, -129])
    def test_characters_neg_wrap(self, num):
        """test neg value chacter conversion"""
        assert BFK("")._convert(num) == chr(65536+num)

    @pytest.mark.parametrize("num", [128, 127, 1, 10, 30, 103, 200, 65536])
    def test_characters_pos_wrap(self, num):
        """test neg value chacter conversion"""
        assert BFK("")._convert(num) == chr(num % 65536)


class TestRun:
    """Test Run Problems"""
    def test_bad_opcodes_all(self):
        """Test Skip Bad Opcodes"""
        #Hidden Loop: ++[>+<-]
        pgm = """
        ABC++D[EFG&>*()+&*)(&)<-ZEHD]KSL
        """
        b = BFK(pgm)
        b.run()
        assert b.pos == len(pgm)
        assert b.ptr == 0
        assert b.mem[0] == 0
        assert b.mem[1] == 2

class TestPlus:
    """Test Plus"""
    def test_plus(self):
        """Test Plus Method"""
        b = BFK("")
        b._plus()
        assert b.mem[b.ptr] == 1

    def test_plus_run(self):
        """Test Plus Run"""
        b = BFK("+")
        b.run()
        assert b.mem[b.ptr] == 1

    def test_plus_wrap(self):
        """Test Plus Wrap"""
        b = BFK("")
        b.mem[b.ptr] = 127
        b._plus()
        assert b.mem[b.ptr] == -128


class TestMinus:
    """Test Minus"""
    def test_minus(self):
        """Test Minus Method"""
        b = BFK("")
        b._minus()
        assert b.mem[b.ptr] == -1

    def test_minus_run(self):
        """Test Minus Run"""
        b = BFK("-")
        b.run()
        assert b.mem[b.ptr] == -1

    def test_minus_wrap(self):
        """Test Minus Wrap"""
        b = BFK("")
        b.mem[b.ptr] = -128
        b._minus()
        assert b.mem[b.ptr] == 127

class TestLeftMemShift:
    """Test Left Mem Shift"""
    def test_mem_l(self):
        """Test Mem Left Method"""
        b = BFK("")
        b.ptr = 1
        b._cell_l()
        assert b.ptr == 0

    def test_cell_l_run(self):
        """Test Cell Left Run"""
        b = BFK("<")
        b.ptr = 1
        b.run()
        assert b.ptr == 0

    def test_cell_l_wrap(self):
        """Test Cell Left Wrap"""
        b = BFK("")
        b._cell_l()
        assert b.ptr == len(b.mem)-1

class TestRightMemShift:
    """Test Right Mem Shift"""
    def test_cell_r(self):
        """Test Cell Right Method"""
        b = BFK("")
        b._cell_r()
        assert b.ptr == 1

    def test_cell_r_run(self):
        """Test Cell Right Run"""
        b = BFK(">")
        b.run()
        assert b.ptr == 1

    def test_cell_r_wrap(self):
        """Test Cell Right Wrap"""
        b = BFK("")
        b.ptr = len(b.mem)-2
        b._cell_r()
        assert b.ptr == len(b.mem)-1

class TestLoops:
    """Test Loops"""
    def test_loop_skip(self):
        """Test Loop Skip"""
        # Should Skip Loop
        b = BFK("[+++]+")
        b.run()
        assert b.mem[b.ptr] == 1

    def test_loop_broken(self):
        """Test Loop Broken"""
        # Should Enter First Loop, Run Second Loop Twice and Quit
        b = BFK("++[>++[>+<-]<-")
        b.run()
        assert b.mem[2] == 2

    def test_loop_enter(self):
        """Test Loop Enter"""
        # Should Enter Loop and Run Twice
        b = BFK("++[>+<-]")
        b.run()
        assert b.mem[1] == 2

    def test_loop_double(self):
        """Test Double Loop"""
        b = BFK("++[>++[>+<-]<-]")
        b.run()
        assert b.mem[2] == 4

    def test_loop_triple(self):
        """Test Triple Loop"""
        b = BFK("++[>++[>++[>+<-]<-]<-]")
        b.run()
        assert b.mem[3] == 8




