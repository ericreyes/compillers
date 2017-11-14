import ply.lex as lex
import pprint as pprint
from PyQt4 import QtCore, QtGui
import time
import threading

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
      'CALL': 600,

      #official functions
      'move': 9001,
      'turnleft': 9002,
      'putBeeper': 9003,
      'pickBeeper': 9004,
      'end': 9005,
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

global t_symbols
t_symbols = {}

# karel_program = open('karel.txt').read()
# lexer = OurLexer()
# lexer.build()


# #lexer.test(karel_program)


# all_tokens = lexer.get_tokens(karel_program)
# all_tokens.reverse()
# print (all_tokens)

# all_tokens2 = all_tokens
global karel_map_matrix
global karel_dict
karel_dict = {'beepers':0,'position_i':0,'position_j':0,'direction':''}


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

''' ESTO YA NO VALE MAS QUE PA PURA VERGA'''
def add_symbol_to_table(symbol):
  global symbol_table
  global symbol_count
  symbol_count += 1
  symbol_table.update({symbol: symbol_count})
  print(symbol_table)
  print('AGREGUE UNA FUNCION, BIEN VERGA')


#------------------------------------------------------------------------------------------------


def mostrarError(expected_token):
    raise Exception('Syntax Error: Expected {}.'.format(expected_token))


#------PENDIENTE_CI------
#<program> ::= "class" "program" "{" <functions> <main function> "}"
def program():
    if (exigir("class")):
        add_code_in_ci("JMP")
        stack_positions.append(ci_count)
        print (stack_positions, "la tabla de posiciones")
        if (exigir("program")):
            if (exigir("{")):
                add_one_to_ci()
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
        if (exigir("(")):
            if (exigir(")")):
                if (exigir("{")):
                    actual_position = stack_positions.pop()
                    print(actual_position, 'poooooooop')
                    ci_list[actual_position] = ci_count
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
    print ('CUSTOMEEEEEERRRRRRRRRRR!!!!!!!!!!!')
    if (exigir("void")):
        customer_function() #HERE
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
    if (verificar('move') or verificar("turnleft") or verificar("pickBeeper") or verificar("putBeeper") or verificar("end") or verificar("program")):
        #print ('obviamente entre a official fucntion')
        next_token = all_tokens[-1]
        add_code_in_ci(next_token)

        official_function()
    else:
        call_customer_function()

#------PENDIENTE_ARREGLAR------
#------PENDIENTE_ARREGLAR------
#------PENDIENTE_ARREGLAR------
#------PENDIENTE_ARREGLAR------
#------PENDIENTE_ARREGLAR------
def customer_function():
    global t_symbols
    next_token = all_tokens[-1]
    if(exigir(next_token)):
        t_symbols[next_token] = ci_count
        print ("Tabla de simbolos:", t_symbols)

def call_customer_function():
    global t_symbols
    next_token = all_tokens[-1]
    if(exigir(next_token)):
        if (next_token in t_symbols):
            print(t_symbols)
            print(next_token)
            print(t_symbols[next_token])
            add_code_in_ci("CALL")
            add_num_in_ci(t_symbols[next_token])
            stack_positions.append(ci_count)
            print ("stack", stack_positions)


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
                    print(actual_position, 'poooooooop')
                    ci_list[actual_position] = ci_count + 2
                    add_code_in_ci("JMP")
                    print(actual_position, 'poooooooop22222')
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

class MyPopup(QtGui.QWidget):
    def __init__(self):
        QtGui.QLabel.__init__(self)

    def paintEvent(self, e):
        dc = QPainter(self)
        dc.drawLine(0, 0, 100, 100)
        dc.drawLine(100, 0, 0, 100)



def check_lex_and_syntax(karel_program):
    #karel_program = open('karel.txt').read()
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

def read_board_file():
    global karel_map_matrix
    print("reading from file, reload")
    karel_map_matrix = [[0 for x in range(10)] for y in range(10)]
    karel_tokens = open("mapa.karel").read().split()
    karel_tokens.reverse()

    for i, lista in enumerate(karel_map_matrix):
        for j, element in enumerate(lista):
            karel_map_matrix[i][j] = karel_tokens.pop()

    # Use pretty print to print the matrix in console
    #pprint.pprint((karel_map_matrix))
    draw_board()



#check_lex_and_syntax()

def get_karel_position():
    return karel_dict['position_i'], karel_dict['position_j']
def set_karel_position(i, j):
    karel_dict['position_i'] = i
    karel_dict['position_j'] = j

def set_square(square, image_name):
    global karel_map_matrix

    if(image_name == 'blank'):
        blank_square = QtGui.QPixmap('images/blank.png')
        square.setPixmap(blank_square)

    elif(image_name == 'north'):
        karelN = QtGui.QPixmap('images/karelN.png')
        square.setPixmap(karelN)
    elif(image_name == 'east'):
        karelE = QtGui.QPixmap('images/karelE.png')
        square.setPixmap(karelE)
    elif(image_name == 'south'):
        karelS = QtGui.QPixmap('images/karelS.png')
        square.setPixmap(karelS)
    elif(image_name == 'west'):
        karelW = QtGui.QPixmap('images/karelW.png')
    elif(image_name == 'northB'):
        karelN = QtGui.QPixmap('images/karelNB.png')
        square.setPixmap(karelN)
    elif(image_name == 'eastB'):
        karelE = QtGui.QPixmap('images/karelEB.png')
        square.setPixmap(karelE)
    elif(image_name == 'southB'):
        karelS = QtGui.QPixmap('images/karelSB.png')
        square.setPixmap(karelS)
    elif(image_name == 'westB'):
        karelW = QtGui.QPixmap('images/karelWB.png')
        square.setPixmap(karelW)
    elif(image_name == 'wall'):
        wall = QtGui.QPixmap('images/wall.png')
        square.setPixmap(wall)
    elif(image_name == 'beeper'):
        beeper = QtGui.QPixmap('images/beeper.png')
        square.setPixmap(beeper)

        # #TODO, set a number in the image, to know how many beepers are there
        # i, j = get_karel_position()
        # if (karel_map_matrix[i][j] == '-'):
        #     karel_map_matrix[i][j] = '1'
        # elif(karel_map_matrix[i][j].isdigit()):
        #     karel_map_matrix[i][j] = str(int(karel_map_matrix[i][j]) + 1)

def pick_beeper_board():
    pass

def drop_beeper_board():
    pass

def draw_board():
    global karel_map_matrix
    global all_squares
    global karel_dict

    for i, array in enumerate(all_squares):
        for j, square in enumerate(array):
            if(karel_map_matrix[i][j] == '-'):
                set_square(square, 'blank')
            elif(karel_map_matrix[i][j] == 'B'):
                set_square(square, 'wall')
            elif(karel_map_matrix[i][j].isdigit()):
                set_square(square, 'beeper')
            elif(karel_map_matrix[i][j] == 'N'):
                karel_dict["position_i"] = i
                karel_dict["position_j"] = j
                karel_dict["direction"] = 'north'
                set_square(square, 'north')
                karel_map_matrix[i][j] = '-'
            elif(karel_map_matrix[i][j] == 'S'):
                karel_dict["position_i"] = i
                karel_dict["position_j"] = j
                karel_dict["direction"] = 'south'
                set_square(square, 'south')
                karel_map_matrix[i][j] = '-'
            elif(karel_map_matrix[i][j] == 'E'):
                karel_dict["position_i"] = i
                karel_dict["position_j"] = j
                karel_dict["direction"] = 'east'
                set_square(square, 'east')
                karel_map_matrix[i][j] = '-'
            elif(karel_map_matrix[i][j] == 'W'):
                karel_dict["position_i"] = i
                karel_dict["position_j"] = j
                karel_dict["direction"] = 'west'
                set_square(square, 'west')
                karel_map_matrix[i][j] = '-'
            else:
                raise Exception('Invalid symbol in Karel File, unable to load')

    #checa el dic Karel
    #pinta Karel en la posicion que sacamos del dic


def redraw():
    global all_squares
    global karel_dict

    i,j = get_karel_position()
    direction = karel_dict['direction']

    draw_board()
    set_square(all_squares[i][j], direction)



def move_board():
    global all_squares
    global karel_dict
    print('executing move')
    i, j = get_karel_position()

    try:
        if (karel_dict['direction'] == 'north'):
            if (i-1 < 0):
                raise Exception('Invalid move: Cannot play off the board')
            if (karel_map_matrix[i-1][j] == 'B'):
                raise Exception('Invalid move: Cannot move to a wall')
            if(karel_map_matrix[i-1][j].isdigit()):
                set_square(all_squares[i-1][j], 'northB')
            else:
                set_square(all_squares[i-1][j], 'north')
            set_karel_position(i-1, j)

        elif (karel_dict['direction'] == 'south'):
            if (i+1 > 9):
                raise Exception('Invalid move: Cannot play off the board')
            if (karel_map_matrix[i+1][j] == 'B'):
                raise Exception('Invalid move: Cannot move to a wall')
            if(karel_map_matrix[i+1][j].isdigit()):
                set_square(all_squares[i+1][j], 'southB')
            else:
                set_square(all_squares[i+1][j], 'south')
            set_karel_position(i+1, j)

        elif (karel_dict['direction'] == 'east'):
            if (j+1 > 9):
                raise Exception('Invalid move: Cannot play off the board')
            if (karel_map_matrix[i][j+1] == 'B'):
                raise Exception('Invalid move: Cannot move to a wall')
            if(karel_map_matrix[i][j+1].isdigit()):
                set_square(all_squares[i][j+1], 'eastB')
            else:
                set_square(all_squares[i][j+1], 'east')
            set_karel_position(i, j+1)

        elif (karel_dict['direction'] == 'west'):
            if (j-1 < 0):
                raise Exception('Invalid move: Cannot play off the board')
            if (karel_map_matrix[i][j-1] == 'B'):
                raise Exception('Invalid move: Cannot move to a wall')
            if(karel_map_matrix[i][j-1].isdigit()):
                set_square(all_squares[i][j-1], 'westB')
            else:
                set_square(all_squares[i][j-1], 'west')
            set_karel_position(i, j-1)

        print(karel_map_matrix[i][j], 'lo que dejo atras')
        if (karel_map_matrix[i][j] == '-'):
            set_square(all_squares[i][j], 'blank')
        elif (karel_map_matrix[i][j].isdigit()):
            set_square(all_squares[i][j], 'beeper')

    except (Exception) as e:
        print (e)
        #Ui_MainWindow.create_error_popup()

def turn_left_board():
    global karel_dict
    global all_squares
    print('executing turnleft')
    i, j = get_karel_position()

    if (karel_dict['direction'] == 'north'):
        karel_dict['direction'] = 'west'
        set_square(all_squares[i][j] ,'west')
    elif (karel_dict['direction'] == 'west'):
        karel_dict['direction'] = 'south'
        set_square(all_squares[i][j] ,'south')
    elif (karel_dict['direction'] == 'south'):
        karel_dict['direction'] = 'east'
        set_square(all_squares[i][j] ,'east')
    elif (karel_dict['direction'] == 'east'):
        karel_dict['direction'] = 'north'
        set_square(all_squares[i][j] ,'north')


def put_beeper_board():
    pass

def pick_beeper_board():
    pass

def if_condition_board():
    pass

def iterate_condition_board():
    pass

def JMP_board():
    #TODO: Revisit jump to see if it's right
    global ci_list
    global position
    print("Esta posicion", ci_list[position])
    print("La de adelante", ci_list[position + 1])
    nombre = ci_list[position + 1]
    position = position + 1
    print(nombre, 'nombre')

def RET_board():
    pass

def while_condition_board():
    pass

def CALL_board():
    pass

def front_is_clear_board():
    pass

def left_is_clear_board():
    pass

def right_is_clear_board():
    pass

def front_is_blocked_board():
    pass

def left_is_blocked_board():
    pass

def right_is_blocked_board():
    pass

def next_to_a_beeper_board():
    pass

def not_next_to_a_beeper_board():
    pass

def facing_north_board():
    pass

def facing_south_board():
    pass

def facing_east_board():
    pass

def facing_west_board():
    pass

def not_facing_north_board():
    pass

def not_facing_south_board():
    pass

def not_facing_east_board():
    pass

def not_facing_west_board():
    pass

def any_beepers_in_beeper_bag_board():
    pass

def no_beepers_in_beeper_bag_board():
    pass

def program_board():
    print('executing program')

def execute_semantic():
    global semantic_functions
    global ci_list
    global position
    position = 0

    while(ci_list[position] != 9005):
        semantic_functions[str(ci_list[position])]()
        position = position + 1
        # if(ci_list[position] == 9001):
        #     print('executing move')
        #     move_board()

        #     i, j = get_karel_position()
        #     set_square(all_squares[i][j],'southB')

        # elif(ci_list[position] == 9002):
        #     print('executing turnleft')
        #     turn_left_board()

        # elif(ci_list[position] == 9003):
        #     pass
        #     #ejecutar codigo de putbeeper
        # elif(ci_list[position] == 9004):
        #     pass
        #     #ejecutar codigo de pickbeeper
        # elif(ci_list[position] == 510 or ci_list[position] == 520 or ci_list[position] == 550):
        #     print("condicional")
        #     if (ci_list[position + 1] is True):
        #         pass
        # elif(ci_list[position] == 530 or ci_list[position] == 600):
        #     print("Esta posicion", ci_list[position])
        #     print("La de adelante", ci_list[position + 1])
        #     nombre = ci_list[position + 1]
        #     #position = position - 1
        #     print("Que pedo")
        # elif(ci_list[position] == 540):
        #     print ("staaaaaack", stack_positions)
        #     #position =
        # position = position + 1


global semantic_functions
semantic_functions = {
    "9001": move_board,
    "9002": turn_left_board,
    "9003": put_beeper_board,
    "9004": pick_beeper_board,
    "510": if_condition_board,
    "520": iterate_condition_board,
    "530": JMP_board,
    "540": RET_board,
    "550": while_condition_board,
    "600": CALL_board,
    "8001": front_is_clear_board,
    "8002": left_is_clear_board,
    "8003": right_is_clear_board,
    "8004": front_is_blocked_board,
    "8005": left_is_blocked_board,
    "8006": right_is_blocked_board,
    "8007": next_to_a_beeper_board,
    "8008": not_next_to_a_beeper_board,
    "8009": facing_north_board,
    "8010": facing_south_board,
    "8011": facing_east_board,
    "8012": facing_west_board,
    "8013": not_facing_north_board,
    "8014": not_facing_south_board,
    "8015": not_facing_east_board,
    "8016": not_facing_west_board,
    "8017": any_beepers_in_beeper_bag_board,
    "8018": no_beepers_in_beeper_bag_board,
    '1000': program_board,
}


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1228, 891)

        #self.EAST = True
        #self.NORTH = False
        #self.WEST = False
        #self.SOUTH = False

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 1211, 841))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_7 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.pos03 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos03.setObjectName(_fromUtf8("pos03"))
        self.gridLayout_5.addWidget(self.pos03, 0, 3, 1, 1)
        self.pos21 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos21.setObjectName(_fromUtf8("pos21"))
        self.gridLayout_5.addWidget(self.pos21, 2, 1, 1, 1)
        self.pos01 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos01.setObjectName(_fromUtf8("pos01"))
        self.gridLayout_5.addWidget(self.pos01, 0, 1, 1, 1)
        self.pos31 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos31.setObjectName(_fromUtf8("pos31"))
        self.gridLayout_5.addWidget(self.pos31, 3, 1, 1, 1)
        self.pos23 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos23.setObjectName(_fromUtf8("pos23"))
        self.gridLayout_5.addWidget(self.pos23, 2, 3, 1, 1)
        self.pos00 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos00.setObjectName(_fromUtf8("pos00"))
        self.gridLayout_5.addWidget(self.pos00, 0, 0, 1, 1)
        self.pos02 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos02.setObjectName(_fromUtf8("pos02"))
        self.gridLayout_5.addWidget(self.pos02, 0, 2, 1, 1)
        self.pos10 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos10.setObjectName(_fromUtf8("pos10"))
        self.gridLayout_5.addWidget(self.pos10, 1, 0, 1, 1)
        self.pos42 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos42.setObjectName(_fromUtf8("pos42"))
        self.gridLayout_5.addWidget(self.pos42, 4, 2, 1, 1)
        self.pos30 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos30.setObjectName(_fromUtf8("pos30"))
        self.gridLayout_5.addWidget(self.pos30, 3, 0, 1, 1)
        self.pos20 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos20.setObjectName(_fromUtf8("pos20"))
        self.gridLayout_5.addWidget(self.pos20, 2, 0, 1, 1)
        self.pos32 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos32.setObjectName(_fromUtf8("pos32"))
        self.gridLayout_5.addWidget(self.pos32, 3, 2, 1, 1)
        self.pos13 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos13.setObjectName(_fromUtf8("pos13"))
        self.gridLayout_5.addWidget(self.pos13, 1, 3, 1, 1)
        self.pos22 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos22.setObjectName(_fromUtf8("pos22"))
        self.gridLayout_5.addWidget(self.pos22, 2, 2, 1, 1)
        self.pos33 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos33.setObjectName(_fromUtf8("pos33"))
        self.gridLayout_5.addWidget(self.pos33, 3, 3, 1, 1)
        self.pos12 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos12.setObjectName(_fromUtf8("pos12"))
        self.gridLayout_5.addWidget(self.pos12, 1, 2, 1, 1)
        self.pos11 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos11.setObjectName(_fromUtf8("pos11"))
        self.gridLayout_5.addWidget(self.pos11, 1, 1, 1, 1)
        self.pos41 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos41.setObjectName(_fromUtf8("pos41"))
        self.gridLayout_5.addWidget(self.pos41, 4, 1, 1, 1)
        self.pos40 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos40.setObjectName(_fromUtf8("pos40"))
        self.gridLayout_5.addWidget(self.pos40, 4, 0, 1, 1)
        self.pos43 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos43.setObjectName(_fromUtf8("pos43"))
        self.gridLayout_5.addWidget(self.pos43, 4, 3, 1, 1)
        self.pos51 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos51.setObjectName(_fromUtf8("pos51"))
        self.gridLayout_5.addWidget(self.pos51, 5, 1, 1, 1)
        self.pos57 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos57.setObjectName(_fromUtf8("pos57"))
        self.gridLayout_5.addWidget(self.pos57, 5, 7, 1, 1)
        self.pos58 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos58.setObjectName(_fromUtf8("pos58"))
        self.gridLayout_5.addWidget(self.pos58, 5, 8, 1, 1)
        self.pos55 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos55.setObjectName(_fromUtf8("pos55"))
        self.gridLayout_5.addWidget(self.pos55, 5, 5, 1, 1)
        self.pos56 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos56.setObjectName(_fromUtf8("pos56"))
        self.gridLayout_5.addWidget(self.pos56, 5, 6, 1, 1)
        self.pos59 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos59.setObjectName(_fromUtf8("pos59"))
        self.gridLayout_5.addWidget(self.pos59, 5, 9, 1, 1)
        self.pos52 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos52.setObjectName(_fromUtf8("pos52"))
        self.gridLayout_5.addWidget(self.pos52, 5, 2, 1, 1)
        self.pos53 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos53.setObjectName(_fromUtf8("pos53"))
        self.gridLayout_5.addWidget(self.pos53, 5, 3, 1, 1)
        self.pos54 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos54.setObjectName(_fromUtf8("pos54"))
        self.gridLayout_5.addWidget(self.pos54, 5, 4, 1, 1)
        self.pos67 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos67.setObjectName(_fromUtf8("pos67"))
        self.gridLayout_5.addWidget(self.pos67, 6, 7, 1, 1)
        self.pos63 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos63.setObjectName(_fromUtf8("pos63"))
        self.gridLayout_5.addWidget(self.pos63, 6, 3, 1, 1)
        self.pos64 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos64.setObjectName(_fromUtf8("pos64"))
        self.gridLayout_5.addWidget(self.pos64, 6, 4, 1, 1)
        self.pos65 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos65.setObjectName(_fromUtf8("pos65"))
        self.gridLayout_5.addWidget(self.pos65, 6, 5, 1, 1)
        self.pos66 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos66.setObjectName(_fromUtf8("pos66"))
        self.gridLayout_5.addWidget(self.pos66, 6, 6, 1, 1)
        self.pos68 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos68.setObjectName(_fromUtf8("pos68"))
        self.gridLayout_5.addWidget(self.pos68, 6, 8, 1, 1)
        self.pos69 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos69.setObjectName(_fromUtf8("pos69"))
        self.gridLayout_5.addWidget(self.pos69, 6, 9, 1, 1)
        self.pos35 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos35.setObjectName(_fromUtf8("pos35"))
        self.gridLayout_5.addWidget(self.pos35, 3, 5, 1, 1)
        self.pos25 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos25.setObjectName(_fromUtf8("pos25"))
        self.gridLayout_5.addWidget(self.pos25, 2, 5, 1, 1)
        self.pos45 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos45.setObjectName(_fromUtf8("pos45"))
        self.gridLayout_5.addWidget(self.pos45, 4, 5, 1, 1)
        self.pos15 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos15.setObjectName(_fromUtf8("pos15"))
        self.gridLayout_5.addWidget(self.pos15, 1, 5, 1, 1)
        self.pos75 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos75.setObjectName(_fromUtf8("pos75"))
        self.gridLayout_5.addWidget(self.pos75, 7, 5, 1, 1)
        self.pos74 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos74.setObjectName(_fromUtf8("pos74"))
        self.gridLayout_5.addWidget(self.pos74, 7, 4, 1, 1)
        self.pos72 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos72.setObjectName(_fromUtf8("pos72"))
        self.gridLayout_5.addWidget(self.pos72, 7, 2, 1, 1)
        self.pos71 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos71.setObjectName(_fromUtf8("pos71"))
        self.gridLayout_5.addWidget(self.pos71, 7, 1, 1, 1)
        self.pos73 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos73.setObjectName(_fromUtf8("pos73"))
        self.gridLayout_5.addWidget(self.pos73, 7, 3, 1, 1)
        self.pos77 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos77.setObjectName(_fromUtf8("pos77"))
        self.gridLayout_5.addWidget(self.pos77, 7, 7, 1, 1)
        self.pos70 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos70.setObjectName(_fromUtf8("pos70"))
        self.gridLayout_5.addWidget(self.pos70, 7, 0, 1, 1)
        self.pos90 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos90.setObjectName(_fromUtf8("pos90"))
        self.gridLayout_5.addWidget(self.pos90, 9, 0, 1, 1)
        self.pos80 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos80.setObjectName(_fromUtf8("pos80"))
        self.gridLayout_5.addWidget(self.pos80, 8, 0, 1, 1)
        self.pos76 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos76.setObjectName(_fromUtf8("pos76"))
        self.gridLayout_5.addWidget(self.pos76, 7, 6, 1, 1)
        self.pos50 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos50.setObjectName(_fromUtf8("pos50"))
        self.gridLayout_5.addWidget(self.pos50, 5, 0, 1, 1)
        self.pos60 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos60.setObjectName(_fromUtf8("pos60"))
        self.gridLayout_5.addWidget(self.pos60, 6, 0, 1, 1)
        self.pos78 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos78.setObjectName(_fromUtf8("pos78"))
        self.gridLayout_5.addWidget(self.pos78, 7, 8, 1, 1)
        self.pos79 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos79.setObjectName(_fromUtf8("pos79"))
        self.gridLayout_5.addWidget(self.pos79, 7, 9, 1, 1)
        self.pos05 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos05.setObjectName(_fromUtf8("pos05"))
        self.gridLayout_5.addWidget(self.pos05, 0, 5, 1, 1)
        self.pos28 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos28.setObjectName(_fromUtf8("pos28"))
        self.gridLayout_5.addWidget(self.pos28, 2, 8, 1, 1)
        self.pos16 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos16.setObjectName(_fromUtf8("pos16"))
        self.gridLayout_5.addWidget(self.pos16, 1, 6, 1, 1)
        self.pos26 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos26.setObjectName(_fromUtf8("pos26"))
        self.gridLayout_5.addWidget(self.pos26, 2, 6, 1, 1)
        self.pos17 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos17.setObjectName(_fromUtf8("pos17"))
        self.gridLayout_5.addWidget(self.pos17, 1, 7, 1, 1)
        self.pos08 = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pos08.sizePolicy().hasHeightForWidth())
        self.pos08.setSizePolicy(sizePolicy)
        self.pos08.setObjectName(_fromUtf8("pos08"))
        self.gridLayout_5.addWidget(self.pos08, 0, 8, 1, 1)
        self.pos27 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos27.setObjectName(_fromUtf8("pos27"))
        self.gridLayout_5.addWidget(self.pos27, 2, 7, 1, 1)
        self.pos04 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos04.setObjectName(_fromUtf8("pos04"))
        self.gridLayout_5.addWidget(self.pos04, 0, 4, 1, 1)
        self.pos07 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos07.setObjectName(_fromUtf8("pos07"))
        self.gridLayout_5.addWidget(self.pos07, 0, 7, 1, 1)
        self.pos29 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos29.setObjectName(_fromUtf8("pos29"))
        self.gridLayout_5.addWidget(self.pos29, 2, 9, 1, 1)
        self.pos06 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos06.setObjectName(_fromUtf8("pos06"))
        self.gridLayout_5.addWidget(self.pos06, 0, 6, 1, 1)
        self.pos39 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos39.setObjectName(_fromUtf8("pos39"))
        self.gridLayout_5.addWidget(self.pos39, 3, 9, 1, 1)
        self.pos48 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos48.setObjectName(_fromUtf8("pos48"))
        self.gridLayout_5.addWidget(self.pos48, 4, 8, 1, 1)
        self.pos47 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos47.setObjectName(_fromUtf8("pos47"))
        self.gridLayout_5.addWidget(self.pos47, 4, 7, 1, 1)
        self.pos24 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos24.setObjectName(_fromUtf8("pos24"))
        self.gridLayout_5.addWidget(self.pos24, 2, 4, 1, 1)
        self.pos14 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos14.setObjectName(_fromUtf8("pos14"))
        self.gridLayout_5.addWidget(self.pos14, 1, 4, 1, 1)
        self.pos19 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos19.setObjectName(_fromUtf8("pos19"))
        self.gridLayout_5.addWidget(self.pos19, 1, 9, 1, 1)
        self.pos18 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos18.setObjectName(_fromUtf8("pos18"))
        self.gridLayout_5.addWidget(self.pos18, 1, 8, 1, 1)
        self.pos34 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos34.setObjectName(_fromUtf8("pos34"))
        self.gridLayout_5.addWidget(self.pos34, 3, 4, 1, 1)
        self.pos36 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos36.setObjectName(_fromUtf8("pos36"))
        self.gridLayout_5.addWidget(self.pos36, 3, 6, 1, 1)
        self.pos38 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos38.setObjectName(_fromUtf8("pos38"))
        self.gridLayout_5.addWidget(self.pos38, 3, 8, 1, 1)
        self.pos46 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos46.setObjectName(_fromUtf8("pos46"))
        self.gridLayout_5.addWidget(self.pos46, 4, 6, 1, 1)
        self.pos37 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos37.setObjectName(_fromUtf8("pos37"))
        self.gridLayout_5.addWidget(self.pos37, 3, 7, 1, 1)
        self.pos44 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos44.setObjectName(_fromUtf8("pos44"))
        self.gridLayout_5.addWidget(self.pos44, 4, 4, 1, 1)
        self.pos61 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos61.setObjectName(_fromUtf8("pos61"))
        self.gridLayout_5.addWidget(self.pos61, 6, 1, 1, 1)
        self.pos62 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos62.setObjectName(_fromUtf8("pos62"))
        self.gridLayout_5.addWidget(self.pos62, 6, 2, 1, 1)
        self.pos49 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos49.setObjectName(_fromUtf8("pos49"))
        self.gridLayout_5.addWidget(self.pos49, 4, 9, 1, 1)
        self.pos09 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos09.setObjectName(_fromUtf8("pos09"))
        self.gridLayout_5.addWidget(self.pos09, 0, 9, 1, 1)
        self.pos93 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos93.setObjectName(_fromUtf8("pos93"))
        self.gridLayout_5.addWidget(self.pos93, 9, 3, 1, 1)
        self.pos83 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos83.setObjectName(_fromUtf8("pos83"))
        self.gridLayout_5.addWidget(self.pos83, 8, 3, 1, 1)
        self.pos84 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos84.setObjectName(_fromUtf8("pos84"))
        self.gridLayout_5.addWidget(self.pos84, 8, 4, 1, 1)
        self.pos85 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos85.setObjectName(_fromUtf8("pos85"))
        self.gridLayout_5.addWidget(self.pos85, 8, 5, 1, 1)
        self.pos82 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos82.setObjectName(_fromUtf8("pos82"))
        self.gridLayout_5.addWidget(self.pos82, 8, 2, 1, 1)
        self.pos92 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos92.setObjectName(_fromUtf8("pos92"))
        self.gridLayout_5.addWidget(self.pos92, 9, 2, 1, 1)
        self.pos86 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos86.setObjectName(_fromUtf8("pos86"))
        self.gridLayout_5.addWidget(self.pos86, 8, 6, 1, 1)
        self.pos81 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos81.setObjectName(_fromUtf8("pos81"))
        self.gridLayout_5.addWidget(self.pos81, 8, 1, 1, 1)
        self.pos94 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos94.setObjectName(_fromUtf8("pos94"))
        self.gridLayout_5.addWidget(self.pos94, 9, 4, 1, 1)
        self.pos91 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos91.setObjectName(_fromUtf8("pos91"))
        self.gridLayout_5.addWidget(self.pos91, 9, 1, 1, 1)
        self.pos95 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos95.setObjectName(_fromUtf8("pos95"))
        self.gridLayout_5.addWidget(self.pos95, 9, 5, 1, 1)
        self.pos89 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos89.setObjectName(_fromUtf8("pos89"))
        self.gridLayout_5.addWidget(self.pos89, 8, 9, 1, 1)
        self.pos88 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos88.setObjectName(_fromUtf8("pos88"))
        self.gridLayout_5.addWidget(self.pos88, 8, 8, 1, 1)
        self.pos96 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos96.setObjectName(_fromUtf8("pos96"))
        self.gridLayout_5.addWidget(self.pos96, 9, 6, 1, 1)
        self.pos97 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos97.setObjectName(_fromUtf8("pos97"))
        self.gridLayout_5.addWidget(self.pos97, 9, 7, 1, 1)
        self.pos87 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos87.setObjectName(_fromUtf8("pos87"))
        self.gridLayout_5.addWidget(self.pos87, 8, 7, 1, 1)
        self.pos98 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos98.setObjectName(_fromUtf8("pos98"))
        self.gridLayout_5.addWidget(self.pos98, 9, 8, 1, 1)
        self.pos99 = QtGui.QLabel(self.gridLayoutWidget)
        self.pos99.setObjectName(_fromUtf8("pos99"))
        self.gridLayout_5.addWidget(self.pos99, 9, 9, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_5, 1, 1, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.gridLayoutWidget)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_7.addWidget(self.textEdit, 1, 0, 1, 1)
        self.reload_board = QtGui.QPushButton(self.gridLayoutWidget)
        self.reload_board.setMaximumSize(QtCore.QSize(995, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.reload_board.setFont(font)
        self.reload_board.setObjectName(_fromUtf8("reload_board"))
        self.reload_board.clicked.connect(read_board_file) #move_board read_board_file turn_left_board
        self.gridLayout_7.addWidget(self.reload_board, 2, 1, 1, 1)
        self.execute_code = QtGui.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.execute_code.setFont(font)
        self.execute_code.setObjectName(_fromUtf8("execute_code"))
        self.gridLayout_7.addWidget(self.execute_code, 2, 0, 1, 1)
        self.execute_code.clicked.connect(self.execute_code_from_board) # drop_beeper_board  pick_beeper_board
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_7.addWidget(self.label_2, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayoutWidget.raise_()
        self.pos49.raise_()
        self.pos09.raise_()
        self.gridLayoutWidget.raise_()
        self.textEdit.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        global all_squares
        all_squares = [ [self.pos00, self.pos01, self.pos02, self.pos03, self.pos04, self.pos05, self.pos06, self.pos07, self.pos08, self.pos09], [self.pos10, self.pos11, self.pos12, self.pos13, self.pos14, self.pos15, self.pos16, self.pos17, self.pos18, self.pos19], [self.pos20, self.pos21, self.pos22, self.pos23, self.pos24, self.pos25, self.pos26, self.pos27, self.pos28, self.pos29] , [self.pos30, self.pos31, self.pos32, self.pos33, self.pos34, self.pos35, self.pos36, self.pos37, self.pos38, self.pos39], [self.pos40, self.pos41, self.pos42, self.pos43, self.pos44, self.pos45, self.pos46, self.pos47, self.pos48, self.pos49], [self.pos50, self.pos51, self.pos52, self.pos53, self.pos54, self.pos55, self.pos56, self.pos57, self.pos58, self.pos59] ,[self.pos60, self.pos61, self.pos62, self.pos63, self.pos64, self.pos65, self.pos66, self.pos67, self.pos68, self.pos69] , [self.pos70, self.pos71, self.pos72, self.pos73, self.pos74, self.pos75, self.pos76, self.pos77, self.pos78, self.pos79], [self.pos80, self.pos81, self.pos82, self.pos83, self.pos84, self.pos85, self.pos86, self.pos87, self.pos88, self.pos89], [self.pos90, self.pos91, self.pos92, self.pos93, self.pos94, self.pos95, self.pos96, self.pos97, self.pos98, self.pos99]]

    def create_error_popup(self):
        self.w = MyPopup()
        self.w.setGeometry(QtGui.QLabel(100, 100, 400, 200))
        self.w.setText(_translate("MainWindow", "INVALID MOVE", None))
        self.w.show()

    def execute_code_from_board(self):
        # Reset our CI and its counter
        global ci_count
        ci_count = 0
        global ci_list
        ci_list = []
        for i in range(10000):
            ci_list.append(0)

        karel_program = self.textEdit.toPlainText()
        check_lex_and_syntax(karel_program)
        print('reading form board')
        execute_semantic()
        return karel_program


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))


        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; font-size: 30px; }\n"
            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">class program {</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">    program() {</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        move()</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        move()</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        turnleft()</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        move()</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        move()</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        move()</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        turnleft()</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        turnleft()</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        turnleft()</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        end()</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">    }</span></p>\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">}</span></p></body></html>", None))
        # self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        #     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        #     "p, li { white-space: pre-wrap; font-size: 30px; }\n"
        #     "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
        #     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">class program {</span></p>\n"
        #     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">    program() {</span></p>\n"
        #     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        if(left-is-blocked){</span></p>\n"
        #     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">            move()</span></p>\n"
        #     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        }</span></p>\n"
        #     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        end()</span></p>\n"
        #     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">    }</span></p>\n"
        #     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">}</span></p></body></html>", None))
        self.reload_board.setText(_translate("MainWindow", "Reload Board", None))
        self.execute_code.setText(_translate("MainWindow", "Execute code", None))
        self.label.setText(_translate("MainWindow", "Karel code", None))
        self.label_2.setText(_translate("MainWindow", "Board", None))
#    def set_icons(self, buttons_list):






if __name__ == "__main__":
    global karel_map_matrix
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    read_board_file()
    pprint.pprint(karel_map_matrix)

    MainWindow.show()
    sys.exit(app.exec_())
