use bfk_rust::bfk;

#[cfg(test)]
mod tests {
    use crate::bfk::*;

    #[test]
    fn test_plus() {
        let mut b = BFK::new("+");
        b.step();
        assert_eq!(b.mem[b.ptr], 1);

    }

    #[test]
    fn test_plus_wrap() {
        let mut b = BFK::new("+");
        b.mem[b.ptr] = 127;
        b.step();
        assert_eq!(b.mem[b.ptr], -128);

    }

    #[test]
    fn test_minus() {
        let mut b = BFK::new("-");
        b.step();
        assert_eq!(b.mem[b.ptr], -1);

    }

    #[test]
    fn test_minus_wrap() {
        let mut b = BFK::new("-");
        b.mem[b.ptr] = -128;
        b.step();
        assert_eq!(b.mem[b.ptr], 127);

    }

    #[test]
    fn test_mem_l() {
        let mut b = BFK::new("<");
        b.ptr = 1;
        b.step();
        assert_eq!(b.ptr, 0);

    }

    #[test]
    fn test_mem_l_wrap() {
        let mut b = BFK::new("<");
        b.step();
        assert_eq!(b.ptr, MEMSIZE-1);

    }

    #[test]
    fn test_mem_r() {
        let mut b = BFK::new(">");
        b.step();
        assert_eq!(b.ptr, 1);

    }

    #[test]
    fn test_mem_r_wrap() {
        let mut b = BFK::new(">");
        b.ptr = MEMSIZE-1;
        b.step();
        assert_eq!(b.ptr, 0);

    }

    #[test]
    fn test_loop_skip() {
        let mut b = BFK::new("[+++]+");
        b.run();
        assert_eq!(b.mem[b.ptr], 1);
    }

    #[test]
    fn test_loop_broken() {
        let mut b = BFK::new("++[>++[>+<-]<-");
        b.run();
        assert_eq!(b.mem[2], 2);
    }

    #[test]
    fn test_loop_enter() {
        let mut b = BFK::new("++[>+<-]");
        b.run();
        assert_eq!(b.mem[1], 2);
    }


    #[test]
    fn test_loop_double() {
        let mut b = BFK::new("++[>++[>+<-]<-]");
        b.run();
        assert_eq!(b.mem[2], 4);
    }


    #[test]
    fn test_loop_triple() {
        let mut b = BFK::new("++[>++[>++[>+<-]<-]<-]");
        b.run();
        assert_eq!(b.mem[3], 8);
    }


    #[test]
    fn test_bad_opcodes() {
        let pgm = "
            ABC++D[EFG&>*()+&*)(&)<-ZEHD]KSL
        ";
        let mut b = BFK::new(pgm);
        b.run();
        assert_eq!(b.pos, pgm.len());
        assert_eq!(b.ptr, 0);
        assert_eq!(b.mem[0], 0);
        assert_eq!(b.mem[1], 2);
    }


    #[test]
    fn test_characters_neg_wrap() {
        let b = BFK::new("");
        let num = b.convert(-1);
        assert_eq!(num as i32, 65535);
    }


    #[test]
    fn test_characters_neg_wrap_full() {
        let b = BFK::new("");
        let num = b.convert(-128);
        assert_eq!(num, 'ﾀ');
    }

    #[test]
    fn test_characters_pos_wrap_g() {
        let b = BFK::new("");
        let num = b.convert(103);
        assert_eq!(num, 'g');
    }

    #[test]
    fn test_characters_pos_wrap_full() {
        let b = BFK::new("");
        let num = b.convert(65536);
        assert_eq!(num as i32, 0);
    }

}


