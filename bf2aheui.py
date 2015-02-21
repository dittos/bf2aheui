# coding: utf-8

import sys

def read_bf(code):
    current_block = ''
    current_loop = []
    loop_stack = []
    for c in code:
        if c in '><+-.,':
            current_block += c
        elif c == '[':
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

    head = [u'삭뺘우차']
    for x in xrange(height - 1):
        head.append(u'오ㅇ우ㅇ')
    head.append(u'오ㅇ아아')
    head.append(u'오어어어')

    body.append(u'아' * width)
    body.append(u'어' * width)

    tail = [u'우아']
    for x in xrange(height - 1):
        tail.append(u'우오')
    tail.append(u'ㅇ오')
    tail.append(u'어아')

    return concat(concat(head, body), tail)

def compile_basic_block(block):
    assert isinstance(block, basestring)
    result = ''
    for c in block:
        if c == '+':
            result += u'밪반타다'
        elif c == '-':
            result += u'밪반타타'
        elif c == '.':
            result += u'빠맣'
        elif c == ',':
            result += u'바밯'
        elif c == '<':
            result += u'샥바싼'
        elif c == '>':
            result += u'샨바싹삭'
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

print compile_code(read_bf(sys.stdin.read()))
