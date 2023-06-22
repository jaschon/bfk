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
