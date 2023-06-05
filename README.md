# bf_k
A brainf*ck programming language interpreter

https://en.wikipedia.org/wiki/Brainfuck

## Characters

* ">"	Increment the data pointer by one (to point to the next cell to the right).
* "<"	Decrement the data pointer by one (to point to the next cell to the left).
* "+"	Increment the byte at the data pointer by one.
*	"-" Decrement the byte at the data pointer by one.
* "."	Output the byte at the data pointer.
* ","	Accept one byte of input, storing its value in the byte at the data pointer.
* "["	If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
* "]"	If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.[a]
* All other characters are skipped.

## Usage

```
b = BF_K("//CODE HERE").run()

```

### Examples

```
b = BF_K("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.").run()
# Hello World!

b = BF_K(">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-] <.#>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[ <++++>-]<+.[-]++++++++++.").run()
# Hello World!

b = BF_K("++ > +++++ [< +> -]   ++++ ++++[< +++ +++ > - ]< .").run()
# 7
```
