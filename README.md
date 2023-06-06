# bf_k
A brainf*ck programming language interpreter

https://en.wikipedia.org/wiki/Brainfuck

## Characters

### Memory

* \> Increment the data pointer by one.
* \< Decrement the data pinter by one.

### Values

* \+ Increment the byte at the data pointer by one.
* \- Decrement the byte at the data pointer by one.

### Input & Output

* \. Output the byte at the data pointer.
* \, Accept one byte of input and store it in the byte at the data pointer.

### Loop

* \[ If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
* \] If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.

## Usage

```
BF_K("//CODE HERE").run()

```

### Examples

```
BF_K("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.").run()
# Hello World!

BF_K(">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-] <.#>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[ <++++>-]<+.[-]++++++++++.").run()
# Hello World!

BF_K(">++++++++++>+>+[ [+++++[>++++++++<-]>.<++++++[>--------<-]+<<<]>.>>[ [-]<[>+<-]>>[<<+>+>-]<[>+<-[>+<-[>+<-[>+<-[>+<-[>+<- [>+<-[>+<-[>+<-[>[-]>+>+<<<-[>+<-]]]]]]]]]]]+>>> ]<<< ]").run()
# 1 1 2 5 8 ....
# (fibonacci sequence. needs to be forced to stop)

```
