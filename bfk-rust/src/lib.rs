
pub mod bfk {

    use std::io::{stdin, Read};
    pub const MEMSIZE: usize = 3000;

    pub struct BFK {
        pgm: Vec<char>,
        pub ptr: usize,
        pub pos: usize,
        stack: Vec<usize>,
        pub mem: [i32; MEMSIZE],
    }

    impl BFK {
        pub fn new(pgm: &str) -> Self {
            Self {
                pgm: pgm.chars().collect(),
                ptr: 0,
                pos: 0,
                stack: Vec::new(),
                mem: [0; MEMSIZE],
            }
        }

        fn plus(&mut self) {
            self.mem[self.ptr] = if self.mem[self.ptr] == 127 {
                -128
            } else {
                self.mem[self.ptr] + 1
            };
        }

        fn minus(&mut self) {
            self.mem[self.ptr] = if self.mem[self.ptr] == -128 {
                127
            } else {
                self.mem[self.ptr] - 1
            };
        }

        fn mem_r(&mut self) {
            self.ptr = (self.ptr + 1) % MEMSIZE
        }

        fn mem_l(&mut self) {
            self.ptr = if self.ptr == 0 {
                MEMSIZE - 1
            } else {
                self.ptr - 1
            }
        }

        fn loop_l(&mut self) {
            if self.mem[self.ptr] != 0 {
                self.stack.push(self.pos);
            } else {
                let mut stk = vec![];
                while self.pos < self.pgm.len() {
                    if self.pgm[self.pos] == '[' {
                        stk.push(self.pos);
                    } else if self.pgm[self.pos] == ']' {
                        stk.pop();
                        if stk.len() == 0 {
                            break;
                        }
                    }
                    self.pos += 1
                }
            }
        }

        fn loop_r(&mut self) {
            if self.mem[self.ptr] != 0 {
                self.pos = self.stack.last().unwrap().clone();
            } else {
                self.stack.pop();
            }
        }

        fn output(&self) {
            print!("{}", self.convert(self.mem[self.ptr]));
        }

        pub fn convert(&self, num: i32) -> char {
            let num: i32 = if num > -1 { num % 65536 } else { num + 65536 };
            char::from_u32(num.try_into().unwrap()).unwrap()
        }

        fn input(&mut self) {
            let input: Option<i32> = stdin()
                .bytes()
                .next()
                .and_then(|result| result.ok())
                .map(|byte| byte as i32);
            self.mem[self.ptr] = input.unwrap_or(0);
        }

        pub fn step(&mut self) {
            match self.pgm[self.pos] {
                '+' => self.plus(),
                '-' => self.minus(),
                '<' => self.mem_l(),
                '>' => self.mem_r(),
                '[' => self.loop_l(),
                ']' => self.loop_r(),
                '.' => self.output(),
                ',' => self.input(),
                _ => (),
            }
            self.pos += 1
        }

        pub fn run(&mut self) {
            while self.pos < self.pgm.len() {
                self.step();
            }
        }
    }
}


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


