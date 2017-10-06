import ply.lex as lex

class OurLexer(object):
    # List of token names.   This is always required
    tokens = (
        'CLASS',
        'PROGRAM',
        'LBRACKET',
        'RBRACKET',
        'VOID',
        'LPAREN',
        'RPAREN',
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
        'END',
        #'IDENTIFIER'
    )
    # Regular expression rules for simple tokens
    t_CLASS = r'class'
    t_PROGRAM = r'program'
    t_LBRACKET = r'{'
    t_RBRACKET = r'}'
    t_VOID = r'void'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ITERATE = r'iterate'
    t_ISCLEAR = r'-is-clear'
    t_ISBLOCKED = r'-is-blocked'
    t_NEXTTOBEEPER = r'next-to-a-beeper'
    t_NOTNEXTTOBEEPER = r'not-next-to-a-beeper'
    t_FACING = r'facing-'
    t_NOTFACING = r'not-facing-'
    t_ANYBEEPERS = r'any-beepers-in-beeper-bag'
    t_NOBEEPERS = r'no-beepers-in-beeper-bag'
    t_FRONT = r'front'
    t_LEFT = r'left'
    t_RIGHT = r'right'
    t_NORTH = r'north'
    t_SOUTH = r'south'
    t_EAST = r'east'
    t_WEST = r'west'
    t_MOVE = r'move'
    t_TURNLEFT = r'turnLeft'
    t_PICKBEEPER = r'pickBeeper'
    t_PUTBEEPER = r'putBeeper'
    t_END = r'end'
    t_IDENTIFIER = r'[^\s\{\}\'\"]+'


    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    #ignore tabs and spaces
    t_ignore  = ' \t'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             print(tok.type, tok.value)


karel_program = open('karel.txt').read()

# Build the lexer and try it out
lexer = OurLexer()
lexer.build()           # Build the lexer
lexer.test(karel_program)     # Test it

