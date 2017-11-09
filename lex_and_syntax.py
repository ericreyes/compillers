import ply.lex as lex
import pprint as pprint
import PyQt4

class OurLexer(object):
    # List of token names.     This is always required
    global reserved
    reserved = {
        'void': 'VOID',
        'class': 'CLASS',
        'program': 'PROGRAM',
        'end': 'END',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'iterate': 'ITERATE',
        'return': 'RETURN',
        '||': 'OR',
        '&&': 'AND',
        '!': 'NOT',
        'turnoff': 'TURNOFF',
        'turnleft': 'TURNLEFT',
        'move': 'MOVE',
        'pickbeeper': 'PICKBEEPER',
        'putbeeper': 'PUTBEEPER',
        'front-is-clear': 'FRONTISCLEAR',
        'left-is-clear': 'LEFTISCLEAR',
        'right-is-clear': 'RIGHTISCLEAR',
        'front-is-blocked': 'FRONTISBLOCKED',
        'left-is-blocked': 'LEFTISBLOCKED',
        'right-is-blocked': 'RGHTISBLOCKED',
        'next-to-a-beeper': 'NEXTTOABEEPER',
        'not-next-to-a-beeper': 'NOTNEXTTOABEEPER',
        'facing-north': 'FACINGNORTH',
        'facing-south': 'FACINGSOUTH',
        'facing-east': 'FACINGEAST',
        'facing-west': 'FACINGWEST',
        'not-facing-north': 'NOTFACINGNORTH',
        'not-facing-south': 'NOTFACINGSOUTH',
        'not-facing-east': 'NOTFACINGEAST',
        'not-facing-west': 'NOTFACINGWEST',
        'any-beepers-in-beeper-bag': 'ANYBEEPERSINBEEPERBAG',
        'no-beepers-in-beeper-bag': 'NOBEEPERSBAG'
    }

    tokens = [
        'LBRACKET',
        'RBRACKET',
        'LPAREN',
        'RPAREN',
        'IDENTIFIER',
        'NUMBER'
    ] + list(reserved.values())

    # Regular expression rules for simple tokens

    t_LBRACKET = r'{'
    t_RBRACKET = r'}'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_ID(self, token):
        r'[a-zA-Z_][-a-zA-Z_0-9]*'
        global reserved
        # Check for reserved words
        token.type = reserved.get(token.value, 'IDENTIFIER')

        return token

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # ignore tabs and spaces
    t_ignore = ' \t'

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

    def get_tokens(self, data):
        self.lexer.input(data)
        token_values = []
        while True:
            token = self.lexer.token()
            if not token:
                break
            token_values.append(token.value)
        return token_values

    def get_tokens_types(self, data):
        self.lexer.input(data)
        token_types = []
        while True:
            token = self.lexer.token()
            if not token:
                break
            token_types.append(token.type)
        return token_types

# Declaracion e inicializacion de CODIGO INTERMEDIO
    global stack_positions
    stack_positions = []

    global ci_list
    ci_list = []
    for i in range(10000):
        ci_list.append(0)

    # Counter para CODIGO INTERMEDIO
    global ci_count
    global symbol_count


    ci_count = 0

    # Constantes (numeros) para funciones [deben ir en TABLA DE SIMBOLOS, no?]

    global symbol_table
    symbol_table = {
      # if iterate
      'if': 510,
      'while': 550,
      'iterate': 520,
      'JMP': 530,
      'RET': 540,

      #official functions
      'move': 9001,
      'turnleft': 9002,
      'putBeeper': 9003,
      'pickBeeper': 9004,
      'end': 9005,
      'program': 9010,
      #conditionals
      'front-is-clear': 8001,
      'left-is-clear': 8002,
      'right-is-clear': 8003,
      'front-is-blocked': 8004,
      'left-is-blocked': 8005,
      'right-is-blocked': 8006,
      'next-to-a-beeper': 8007,
      'not-next-to-a-beeper': 8008,
      'facing-north': 8009,
      'facing-south': 8010,
      'facing-east': 8011,
      'facing-west': 8012,
      'not-facing-north': 8013,
      'not-facing-south': 8014,
      'not-facing-east': 8015,
      'not-facing-west': 8016,
      'any-beepers-in-beeper-bag': 8017,
      'no-beepers-in-beeper-bag': 8018,

    }
    symbol_count = len(symbol_table) + 8999


# karel_program = open('karel.txt').read()
# lexer = OurLexer()
# lexer.build()


# #lexer.test(karel_program)


# all_tokens = lexer.get_tokens(karel_program)
# all_tokens.reverse()
# print (all_tokens)

# all_tokens2 = all_tokens


def verificar(expected_token):
    global all_tokens
    next_token = all_tokens[-1]
    #print ('VERIFICAR TIENE A {} EN LA MIRA'.format(next_token))
    return expected_token == next_token


global counter
counter = 0


def verificar_identifier():
    global all_tokens
    next_token = all_tokens[-1]
    #print ('VERIFICANDO IDENTIFIER::::::', next_token)
    return len(next_token) > 2 and len(next_token) < 11


def exigir_identifier():
    global all_tokens
    next_token = all_tokens[-1]
    if (verificar_identifier()):
        next_token = all_tokens.pop()
        #print('popeeeoooooo el identifier: {}'.format(next_token))
        # global counter
        # counter = counter + 1
        # print (counter, all_tokens)
        # print ('')
    else:
        raise Exception('function has to have length between 2 and 11')


def exigir_numero():
    global all_tokens
    next_token = all_tokens[-1]
    if (verificar_numero()):
        next_token = all_tokens.pop()
        #print('popeeeoooooo el NUMERO: {}'.format(next_token))


def verificar_numero():
    global all_tokens
    next_token = all_tokens[-1]
    #print ('VERIFICANDO NUMEROOOOO::::::', next_token)
    return int(next_token) >= 1 and int(next_token) <= 100


def exigir(expected_token):
    global all_tokens
    #print (all_tokens, 'antes del pop')

    next_token = all_tokens.pop()
    global counter
    counter = counter + 1
    #print (counter, all_tokens)
    #print ('')
    return expected_token == next_token

def add_one_to_ci():
    global ci_count
    ci_count += 1

def add_num_in_ci(number):
    global ci_count
    ci_list[ci_count] = number
    add_one_to_ci()


def add_code_in_ci(word_to_find):
    global ci_count
    print('Setting {} in Codigo Intermedio'.format(word_to_find))
    if(word_to_find in symbol_table):
        ci_list[ci_count] = symbol_table[word_to_find]
        print('{} is the code to insert in ci_list[{}]'.format(ci_list[ci_count], ci_count))
        print('adding' , word_to_find, ci_count)
        print_ci()
    add_one_to_ci()

def print_ci():
    print('#################')
    for x in range(0, 30):
      print(x,ci_list[x])
    print('#################')


def add_symbol_to_table(symbol):
  global symbol_table
  global symbol_count
  symbol_count += 1
  symbol_table.update({symbol: symbol_count})




#------------------------------------------------------------------------------------------------


def mostrarError(expected_token):
    raise Exception('Syntax Error: Expected {}.'.format(expected_token))


#------PENDIENTE_CI------
#<program> ::= "class" "program" "{" <functions> <main function> "}"
def program():
    if (exigir("class")):
        if (exigir("program")):
            if (exigir("{")):
                functions()
                main_function()
                if (not exigir("}")):
                    mostrarError("}")
            else:
                mostrarError("{")
        else:
            mostrarError("program")
    else:
        mostrarError("class")


#------PENDIENTE_CI------
#<functions> ::= <function> <functions prima> | lambda
def functions():
    if (verificar("void")):
        function()
        functions_prima()


#------PENDIENTE_CI------
#<functions prima> ::= <function> <functions prima> | lambda
def functions_prima():
    if (verificar("void")):
        function()
        functions_prima()


#------PENDIENTE_CI------
def main_function():
    if (exigir("program")):
        add_code_in_ci("program")
        if (exigir("(")):
            if (exigir(")")):
                if (exigir("{")):
                    body()
                    if (not exigir("}")):
                        mostrarError("}")
                else:
                    mostrarError("{")
            else:
                mostrarError(")")
        else:
            mostrarError("(")
    else:
        mostrarError("program")


#------PENDIENTE_CI------
#<function> ::= "void" <name function> "("    ")" "{" <body> "}"
def function():
    print ('CORRIENDO FUNCIOOOOOOOOOOOOOOOOOOOOOOOOON')
    if (exigir("void")):

        name_function() #HERE
        if (exigir("(")):
            if (exigir(")")):
                print ('EXIJO BRACKETS EN FUNCTION')
                if (exigir("{")):
                    body()
                    if (not exigir("}")):
                        mostrarError("}")
                        add_code_in_ci("RET")
                else:
                    mostrarError("{")
            else:
                mostrarError(")")
        else:
            mostrarError("(")
    else:
        mostrarError("void")


#------PENDIENTE_CI------
#<body> ::= <expression> <body prima>
def body():
    print ('expresssion llamada en body normalito')
    expression()
    body_prima()


#------PENDIENTE_CI------
#<body prima> ::= <expression> <body prima> | lambda
def body_prima():
    #print ('entra a body prima ')

    if (verificar("if") or verificar("while") or verificar("iterate") or verificar('move') or verificar("turnleft") or verificar("pickBeeper") or verificar("putBeeper") or verificar("end") or verificar_identifier()):
        expression()
        body_prima()
    # else lambda


#------PENDIENTE_CI------
#<expression> ::= <call function> | <if expression> | <while expression> | <iterate expression>
def expression():
    if (verificar("if")):
        if_expression()
    elif (verificar("while")):
        while_expression()
    elif (verificar("iterate")):
        iterate_expression()
    else:
        call_function()



#------PENDIENTE_CI------
# verificar que no es palabra reservada
# <call function> ::= <name function> "(" ")"
def call_function():
    name_function()
    #print ('exigiendo parentesis en call function')

    if (exigir("(")):
        if (not exigir(")")):
            mostrarError(")")
    else:
        mostrarError("(")
    #print ('CALL FUNCTION, SE CHINGO PARENTESIS')


#------PENDIENTE_CI------
#<name function> ::= <official function> | <customer function>
def name_function():
    if (verificar('move') or verificar("turnleft") or verificar("pickBeeper") or verificar("putBeeper") or verificar("end")):
        #print ('obviamente entre a official fucntion')
        next_token = all_tokens[-1]
        add_code_in_ci(next_token)

        official_function()
    else:
        customer_function()


def customer_function():
    global all_tokens
    next_token = all_tokens[-1]
    if (not next_token in symbol_table):
        add_symbol_to_table(next_token)
    add_code_in_ci(next_token)
    print('CUSTOMER FUNCTION TOKEN {}'.format(next_token))
    exigir_identifier()

#------PENDIENTE_CI------
#<if expression> ::= "if" "(" <condition> ")" "{" <body>    "}" <else>


def if_expression():
    global ci_count
    if (exigir("if")):
        add_code_in_ci("if")
        if (exigir("(")):
            condition()
            add_code_in_ci("JMP")
            stack_positions.append(ci_count)
            stack_positions.append(ci_count)
            add_one_to_ci()
            if (exigir(")")):
                if (exigir("{")):
                    body()

                    if (exigir("}")):
                        else_expression()
                    else:
                        mostrarError("}")
                    actual_position = stack_positions.pop()
                    ci_list[actual_position] = ci_count
                else:
                    mostrarError("{")
            else:
                mostrarError(")")
        else:
            mostrarError("(")
    else:
        mostrarError("if")


#------PENDIENTE_CI------
#<else> ::= "else" "{" <body> "}"    | lambda
def else_expression():
    if (verificar("else")):
        if (exigir("else")):
            add_code_in_ci("JMP")
            actual_position = stack_positions.pop()
            print(actual_position, 'poooooooop')
            ci_list[actual_position] = ci_count + 1

            stack_positions.append(ci_count)
            add_one_to_ci()
            if (exigir("{")):
                body()
                if (not exigir("}")):
                    mostrarError("}")
                actual_position = stack_positions.pop()
                print(actual_position, 'poooooooop')
                ci_list[actual_position] = ci_count
                print_ci()
            else:
                mostrarError("{")
        else:
            mostrarError("else")
    # else Lambda


#------PENDIENTE_CI------
#<while> ::= "while" "(" <condition> ")" "{" <body> "}"
def while_expression():
    global ci_count
    if (exigir("while")):
        stack_positions.append(ci_count)
        add_code_in_ci("while")
        if (exigir("(")):
            condition()
            add_code_in_ci("JMP")
            stack_positions.append(ci_count)
            add_one_to_ci()
            if (exigir(")")):
                if (exigir("{")):
                    body()
                    if (not exigir("}")):
                        mostrarError("}")
                    actual_position = stack_positions.pop()
                    #print(actual_position, 'poooooooop')
                    ci_list[actual_position] = ci_count + 2
                    add_code_in_ci("JMP")
                    #print(actual_position, 'poooooooop')
                    ci_list[ci_count] = stack_positions.pop()
                    add_one_to_ci()
                    print_ci()
                else:
                    mostrarError("{")
            else:
                mostrarError(")")
        else:
            mostrarError("(")
    else:
        mostrarError("while")


def iterate_expression():
    global ci_count
    global all_tokens
    if (exigir("iterate")):
        stack_positions.append(ci_count)
        add_code_in_ci("iterate")
        if (exigir("(")):
            print(all_tokens[-1],'IMPRIMIR EL NUMERO 3')
            add_num_in_ci(all_tokens[-1])
            number()
            add_code_in_ci("JMP")
            stack_positions.append(ci_count)
            add_one_to_ci()
            if (exigir(")")):
                if (exigir("{")):
                    body()
                    if (not exigir("}")):
                        mostrarError("}")
                    actual_position = stack_positions.pop()
                    #print(actual_position, 'poooooooop')
                    ci_list[actual_position] = ci_count + 2
                    add_code_in_ci("JMP")
                    #print(actual_position, 'poooooooop')
                    ci_list[ci_count] = stack_positions.pop()
                    add_one_to_ci()
                    print_ci()
                else:
                    mostrarError("{")
            else:
                mostrarError(")")
        else:
            mostrarError("(")
    else:
        mostrarError("iterate")


#------PENDIENTE_CI------
#<condition> ::=
    # "front-is-clear" |
    # "left-is-clear" |
    # "right-is-clear" |
    # "front-is-blocked" |
    # "left-is-blocked" |
    # "right-is-blocked" |
    # "next-to-a-beeper" |
    # "not-next to a beeper" |
    # "facing-north" |
    # "facing-south" |
    # "facing-east" |
    # "facing-west" |
    # "not-facing-north" |
    # "not-facing-south" |
    # "not-facing-east" |
    # "not-facing-west" |
    # "any-beepers-in-beeper-bag" |
    # "no-beepers-in-beeper-bag"
def condition():
    global all_tokens
    next_token = all_tokens[-1]

    if (verificar("front-is-clear")):
        exigir("front-is-clear")

    elif (verificar("left-is-clear")):
        exigir("left-is-clear")

    elif (verificar("right-is-clear")):
        exigir("right-is-clear")

    elif (verificar("front-is-blocked")):
        exigir("front-is-blocked")

    elif (verificar("left-is-blocked")):
        exigir("left-is-blocked")

    elif (verificar("right-is-blocked")):
        exigir("right-is-blocked")

    elif (verificar("next-to-a-beeper")):
        exigir("next-to-a-beeper")

    elif (verificar("not-next-to-a-beeper")):
        exigir("not-next-to-a-beeper")

    elif (verificar("facing-north")):
        exigir("facing-north")

    elif (verificar("facing-south")):
        exigir("facing-south")

    elif (verificar("facing-east")):
        exigir("facing-east")

    elif (verificar("facing-west")):
        exigir("facing-west")

    elif (verificar("not-facing-north")):
        exigir("not-facing-north")

    elif (verificar("not-facing-south")):
        exigir("not-facing-south")

    elif (verificar("not-facing-east")):
        exigir("not-facing-east")

    elif (verificar("not-facing-west")):
        exigir("not-facing-west")

    elif (verificar("any-beepers-in-beeper-bag")):
        exigir("any-beepers-in-beeper-bag")

    elif (verificar("no-beepers-in-beeper-bag")):
        exigir("no-beepers-in-beeper-bag")
    else:
        mostrarError("a defined condition")
    add_code_in_ci(next_token)

#------PENDIENTE_CI------
#<official function> ::= "move" | "turnleft" | "pickBeeper" | "putBeeper" | "end"
def official_function():
    #print ('official FUNCTIOOOOOOOOOOON')
    if (verificar("move")):
        #print('POP DE MOVEEEEEEEEEEEEEEEEEEEEEE')
        exigir("move")
    elif (verificar("turnleft")):
        exigir("turnleft")
    elif (verificar("pickBeeper")):
        exigir("pickBeeper")
    elif (verificar("putBeeper")):
        exigir("putBeeper")
    elif (verificar("end")):
        exigir("end")
    else:
        mostrarError("a defined function")

def number():
    exigir_numero()

def check_lex_and_syntax():
    karel_program = open('karel.txt').read()
    lexer = OurLexer()
    lexer.build()

    # lexer.test(karel_program)
    global all_tokens
    all_tokens = lexer.get_tokens(karel_program)
    #token_types = lexer.get_tokens_types(karel_program)

    # token_types.reverse()
    all_tokens.reverse()
    #print (all_tokens)

    # Pa debuggear
    #print (all_tokens)
    #print (token_types)
    program()

def read_board_file(karel_file):
    karel_matrix = [[0 for x in range(10)] for y in range(10)]
    karel_tokens = open(karel_file).read().split()
    karel_tokens.reverse()

    for i, lista in enumerate(karel_matrix):
        for j, element in enumerate(lista):
            karel_matrix[i][j] = karel_tokens.pop()

    pprint.pprint((karel_matrix))
    return karel_matrix



#check_lex_and_syntax()
read_board_file('mapa.karel')

#source activate py35_qt4



