# bf2aheui

Transpile Brainfuck code into Aheui code.


## Usage

    python bf2aheui.py path-to-bf-code -o output.aheui


## Implementation status

Currently, very inefficient code is generated. The output could be improved by understanding Brainfuck code in higher-level, with something like [esotope-bfc](http://mearie.org/projects/esotope/bfc/).

### Tape data structure

We use two stacks, ㄱ and ㄴ, to implement the tape.

```
<--    v    -->
a .. b c d .. e
|  ㄱ  | | ㄴ |

a: bottom of ㄱ
c: top of ㄱ (= current position of tape always)
d: top of ㄴ
e: bottom of ㄴ
```

* `<`: move `c` to the top of stack ㄴ(`삭싼`), then `b` becomes current position.
* `>`: move `d` to the top of stack ㄱ(`산싹`), then `d` becomes current position.

Since the tape's length is unlimited, we should initialize the value when moving to unaccessed position. Stack underflow behavior of Aheui is used in bf2aheui. Consequently, `<` is translated into `샥바싼`, and `>` is translated into `샨바싹삭` (the last `삭` is used to keep stay in stack ㄱ in normal case).
