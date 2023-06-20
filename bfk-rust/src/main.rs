use std::io::Read;

fn main() {
   let mut b = BFK::new("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.");
   b.run();
}

struct BFK {
    pgm: Vec<char>,
    ptr: usize,
    counter: usize,
    stack: Vec<usize>,
    cells: [u8;30000],
}


impl BFK {

    fn new(pgm: &str) -> Self {
        Self { pgm: pgm.chars().collect(), ptr: 0, counter: 0, stack: Vec::new(), cells: [0;30000] }
    }

    fn plus(&mut self) {
        self.cells[self.ptr] = if self.cells[self.ptr] < 127 { self.cells[self.ptr] + 1 } else { 0 };
    }

    fn minus(&mut self) {
        self.cells[self.ptr] = if self.cells[self.ptr] > 0 { self.cells[self.ptr] - 1 } else { 127 };
    }

    fn cell_r(&mut self) {
        self.ptr += 1;
    }

    fn cell_l(&mut self) {
        self.ptr = if self.ptr > 0 { self.ptr - 1 } else { 0 } ;
    }

    fn loop_l(&mut self) {
        if self.cells[self.ptr] != 0 {
            self.stack.push(self.counter);
        } else {
            let mut stk = vec!();
            while self.counter < self.pgm.len(){
                if self.pgm[self.counter] == '[' {
                    stk.push(self.counter);
                } else if self.pgm[self.counter] == ']' {
                    stk.pop();
                    if stk.len() == 0 {
                        break;
                    }
                }
                self.counter += 1
            }
        }
    }


    fn loop_r(&mut self) {
        if self.cells[self.ptr] != 0 {
            self.counter = self.stack.last().unwrap().clone();
        } else {
            self.stack.pop();
        }
    }

    fn output(&self) {
        print!("{}", self.cells[self.ptr] as char);
    }

    fn input(&mut self) {
        let input: Option<u8> = std::io::stdin()
            .bytes()
            .next()
            .and_then(|result| result.ok())
            .map(|byte| byte as u8);
        self.cells[self.ptr] = input.unwrap_or(0);
    }

    fn run(&mut self) {
        while self.counter < self.pgm.len() {
            match self.pgm[self.counter] {
                '+' => self.plus(),
                '-' => self.minus(),
                '<' => self.cell_l(),
                '>' => self.cell_r(),
                '[' => self.loop_l(),
                ']' => self.loop_r(),
                '.' => self.output(),
                ',' => self.input(),
                _ => ()
            }
            self.counter += 1
        }
    }



}
