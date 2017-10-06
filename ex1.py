
import nltk
import numpy as np
import matplotlib.pyplot as plt


file_content = open("GramaticaKarel.txt").read()
tokens = nltk.word_tokenize(file_content)

token_count = {}

for token in tokens:
    if token not in token_count:
        token_count[token] = 1
    else:
        token_count[token] += 1

#desde lex
print (token_count)

tokens = (
'CLASS',
'PROGRAM',
'LBRACKET',
'RBRACKET',
'VOID',
'LPAREN',
'RPAREN',
'PAREN',
'ITERATE',
'ISCLEAR',
'ISBLOCKED',
'NEXTTOBEEPER',
'NOTNEXTTOBEEPER',
'FACING',
'NOTFACING',
'ANYBEEPERS',
'NOBEEPERS',
'FRONT',
'LEFT',
'RIGHT',
'NORTH',
'SOUTH',
'EAST',
'WEST',
'MOVE',
'TURNLEFT',
'PICKBEEPER',
'PUTBEEPER',
'END'
)


t_CLASS = r'class'
t_PROGRAM = r'program'
t_LBRACKET = r'{'
t_RBRACKET = r'}'
t_VOID = r'void'
t_LPAREN = r'('
t_RPAREN = r')'
t_PAREN = r'()'
t_ITERATE = r'iterate'
t_ISCLEAR = r'-is-clear'
t_ISBLOCKED = r'-is-blocked'
t_NEXTTOBEEPER = r'next-to-a-beeper'
t_NOTNEXTTOBEEPER = r'not-next-to-a-beeper'
t_FACING = r'facing-'
t_NOTFACING = r'not-facing-'
t_ANYBEEPERS = r'any-beepers-in-beeper-bag'
t_NOBEEPERS = r'no-beepers-in-beeper-bag'
t_NOBEEPERS = r'no-beepers-in-beeper-bag'
t_FRONT = r' front'
t_LEFT = r'left'
t_RIGHT = r' right'
t_NORTH = r'north'
t_SOUTH = r'south'
t_EAST = r'east'
t_WEST = r'west'
t_MOVE = r'move'
t_TURNLEFT = r' turnLeft'
t_PICKBEEPER = r'pickBeeper'
t_PUTBEEPER = r'putBeeper'
t_END = r'end'
