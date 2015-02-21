# coding: utf-8

import argparse
import io
import sys

def read_bf(code):
    current_block = ''
    current_loop = []
    loop_stack = []
    for c in code:
        if c in '><+-.,':
            current_block += c
        elif c == '[':
            if current_block:
                current_loop.append(current_block)
            current_block = ''
            loop_stack.append(current_loop)
            current_loop = []
        elif c == ']':
            current_loop.append(current_block)
            current_block = ''
            parent_loop = loop_stack.pop()
            parent_loop.append(current_loop)
            current_loop = parent_loop
    if current_block:
        current_loop.append(current_block)
    return current_loop

def concat(a, b):
    # invariant:
    #  a, b starts from upper left with direction toward right
    #  and ends at upper right with direction toward right.
    if not a:
        return b
    if not b:
        return a
    awidth = len(a[0])
    bwidth = len(b[0])
    for row in a:
        assert len(row) == awidth
    if len(a) < len(b):
        for x in xrange(len(b) - len(a)):
            a.append(u'ㅇ' * awidth)
    else:
        for x in xrange(len(a) - len(b)):
            b.append(u'ㅇ' * bwidth)
    for y, row in enumerate(b):
        a[y] += row
    return a

def make_loop(body):
    # invariant:
    #  body starts from upper left with direction toward right
    #  and ends at upper right with direction toward right.
    height = len(body)
    width = len(body[0])

    head = [u'뺘우차']
    for x in xrange(height - 1):
        head.append(u'오우ㅇ')
    head.append(u'오아아')
    head.append(u'오어어')

    body.append(u'아' * width)
    body.append(u'어' * width)

    tail = [u'우아']
    for x in xrange(height - 1):
        tail.append(u'우오')
    tail.append(u'ㅇ오')
    tail.append(u'어ㅇ')

    return concat(concat(head, body), tail)

def merge_repeat(s):
    prev = None
    count = 0
    for c in s:
        if prev != c:
            if count:
                yield (prev, count)
            count = 0
        count += 1
        prev = c
    if count:
        yield (prev, count)

AHEUI_NUM_EXPR = {
    1: u'밪반타',
    2: u'박',
    3: u'받',
    4: u'밤',
    5: u'발',
    6: u'밦',
    7: u'밝',
    8: u'밣',
    9: u'밞',
}

def aheui_number(n):
    postfix = u'다' if n > 0 else u'타'
    expr = AHEUI_NUM_EXPR.get(abs(n))
    if expr:
        return expr + postfix
    if abs(n) <= 18:
        n1 = abs(n) // 2
        n2 = abs(n) - n1
        return AHEUI_NUM_EXPR[n1] + postfix + AHEUI_NUM_EXPR[n2] + postfix
    # TODO: better algorithm
    return (AHEUI_NUM_EXPR[1] + postfix) * abs(n)

def compile_basic_block(block):
    assert isinstance(block, basestring)
    result = ''
    for c, n in merge_repeat(block):
        if c == '+':
            result += aheui_number(n)
        elif c == '-':
            result += aheui_number(-n)
        elif c == '.':
            result += u'빠맣' * n
        elif c == ',':
            result += u'마밯' * n
        elif c == '<':
            result += u'샥바싼' * n
        elif c == '>':
            result += u'샨바싹' * n + u'삭'
    return [result]

def compile_blocks(blocks):
    result = []
    for block in blocks:
        if isinstance(block, basestring):
            blockresult = compile_basic_block(block)
        else:
            blockresult = make_loop(compile_blocks(block))
        result = concat(result, blockresult)
    return result

def compile_code(code):
    main = compile_blocks(code)
    main = concat([u'삭바'], main)
    main = concat(main, [u'희'])
    return u'\n'.join(main)

parser = argparse.ArgumentParser()
parser.add_argument('input', help="path of input Brainfuck file")
parser.add_argument('-o', '--output', help="output path (default: stdout)", default='-')

args = parser.parse_args()
with open(args.input, 'r') as fp:
    code = read_bf(fp.read())
result = compile_code(code)
if args.output == '-':
    print result
else:
    with io.open(args.output, 'w', encoding='utf-8') as fp:
        fp.write(result)
