###
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






#########################################################################################yeah




from PyQt4 import QtCore, QtGui

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
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 1211, 841))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_7 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.pos03 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos03.setObjectName(_fromUtf8("pos03"))
        self.gridLayout_5.addWidget(self.pos03, 0, 3, 1, 1)
        self.pos21 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos21.setObjectName(_fromUtf8("pos21"))
        self.gridLayout_5.addWidget(self.pos21, 2, 1, 1, 1)
        self.pos01 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos01.setObjectName(_fromUtf8("pos01"))
        self.gridLayout_5.addWidget(self.pos01, 0, 1, 1, 1)
        self.pos31 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos31.setObjectName(_fromUtf8("pos31"))
        self.gridLayout_5.addWidget(self.pos31, 3, 1, 1, 1)
        self.pos23 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos23.setObjectName(_fromUtf8("pos23"))
        self.gridLayout_5.addWidget(self.pos23, 2, 3, 1, 1)
        self.pos00 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos00.setObjectName(_fromUtf8("pos00"))
        self.gridLayout_5.addWidget(self.pos00, 0, 0, 1, 1)
        self.pos02 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos02.setObjectName(_fromUtf8("pos02"))
        self.gridLayout_5.addWidget(self.pos02, 0, 2, 1, 1)
        self.pos10 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos10.setObjectName(_fromUtf8("pos10"))
        self.gridLayout_5.addWidget(self.pos10, 1, 0, 1, 1)
        self.pos42 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos42.setObjectName(_fromUtf8("pos42"))
        self.gridLayout_5.addWidget(self.pos42, 4, 2, 1, 1)
        self.pos30 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos30.setObjectName(_fromUtf8("pos30"))
        self.gridLayout_5.addWidget(self.pos30, 3, 0, 1, 1)
        self.pos20 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos20.setObjectName(_fromUtf8("pos20"))
        self.gridLayout_5.addWidget(self.pos20, 2, 0, 1, 1)
        self.pos32 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos32.setObjectName(_fromUtf8("pos32"))
        self.gridLayout_5.addWidget(self.pos32, 3, 2, 1, 1)
        self.pos13 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos13.setObjectName(_fromUtf8("pos13"))
        self.gridLayout_5.addWidget(self.pos13, 1, 3, 1, 1)
        self.pos22 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos22.setObjectName(_fromUtf8("pos22"))
        self.gridLayout_5.addWidget(self.pos22, 2, 2, 1, 1)
        self.pos33 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos33.setObjectName(_fromUtf8("pos33"))
        self.gridLayout_5.addWidget(self.pos33, 3, 3, 1, 1)
        self.pos12 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos12.setObjectName(_fromUtf8("pos12"))
        self.gridLayout_5.addWidget(self.pos12, 1, 2, 1, 1)
        self.pos11 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos11.setObjectName(_fromUtf8("pos11"))
        self.gridLayout_5.addWidget(self.pos11, 1, 1, 1, 1)
        self.pos41 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos41.setObjectName(_fromUtf8("pos41"))
        self.gridLayout_5.addWidget(self.pos41, 4, 1, 1, 1)
        self.pos40 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos40.setObjectName(_fromUtf8("pos40"))
        self.gridLayout_5.addWidget(self.pos40, 4, 0, 1, 1)
        self.pos43 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos43.setObjectName(_fromUtf8("pos43"))
        self.gridLayout_5.addWidget(self.pos43, 4, 3, 1, 1)
        self.pos51 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos51.setObjectName(_fromUtf8("pos51"))
        self.gridLayout_5.addWidget(self.pos51, 5, 1, 1, 1)
        self.pos57 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos57.setObjectName(_fromUtf8("pos57"))
        self.gridLayout_5.addWidget(self.pos57, 5, 7, 1, 1)
        self.pos58 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos58.setObjectName(_fromUtf8("pos58"))
        self.gridLayout_5.addWidget(self.pos58, 5, 8, 1, 1)
        self.pos55 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos55.setObjectName(_fromUtf8("pos55"))
        self.gridLayout_5.addWidget(self.pos55, 5, 5, 1, 1)
        self.pos56 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos56.setObjectName(_fromUtf8("pos56"))
        self.gridLayout_5.addWidget(self.pos56, 5, 6, 1, 1)
        self.pos59 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos59.setObjectName(_fromUtf8("pos59"))
        self.gridLayout_5.addWidget(self.pos59, 5, 9, 1, 1)
        self.pos52 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos52.setObjectName(_fromUtf8("pos52"))
        self.gridLayout_5.addWidget(self.pos52, 5, 2, 1, 1)
        self.pos53 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos53.setObjectName(_fromUtf8("pos53"))
        self.gridLayout_5.addWidget(self.pos53, 5, 3, 1, 1)
        self.pos54 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos54.setObjectName(_fromUtf8("pos54"))
        self.gridLayout_5.addWidget(self.pos54, 5, 4, 1, 1)
        self.pos67 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos67.setObjectName(_fromUtf8("pos67"))
        self.gridLayout_5.addWidget(self.pos67, 6, 7, 1, 1)
        self.pos63 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos63.setObjectName(_fromUtf8("pos63"))
        self.gridLayout_5.addWidget(self.pos63, 6, 3, 1, 1)
        self.pos64 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos64.setObjectName(_fromUtf8("pos64"))
        self.gridLayout_5.addWidget(self.pos64, 6, 4, 1, 1)
        self.pos65 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos65.setObjectName(_fromUtf8("pos65"))
        self.gridLayout_5.addWidget(self.pos65, 6, 5, 1, 1)
        self.pos66 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos66.setObjectName(_fromUtf8("pos66"))
        self.gridLayout_5.addWidget(self.pos66, 6, 6, 1, 1)
        self.pos68 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos68.setObjectName(_fromUtf8("pos68"))
        self.gridLayout_5.addWidget(self.pos68, 6, 8, 1, 1)
        self.pos69 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos69.setObjectName(_fromUtf8("pos69"))
        self.gridLayout_5.addWidget(self.pos69, 6, 9, 1, 1)
        self.pos35 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos35.setObjectName(_fromUtf8("pos35"))
        self.gridLayout_5.addWidget(self.pos35, 3, 5, 1, 1)
        self.pos25 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos25.setObjectName(_fromUtf8("pos25"))
        self.gridLayout_5.addWidget(self.pos25, 2, 5, 1, 1)
        self.pos45 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos45.setObjectName(_fromUtf8("pos45"))
        self.gridLayout_5.addWidget(self.pos45, 4, 5, 1, 1)
        self.pos15 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos15.setObjectName(_fromUtf8("pos15"))
        self.gridLayout_5.addWidget(self.pos15, 1, 5, 1, 1)
        self.pos75 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos75.setObjectName(_fromUtf8("pos75"))
        self.gridLayout_5.addWidget(self.pos75, 7, 5, 1, 1)
        self.pos74 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos74.setObjectName(_fromUtf8("pos74"))
        self.gridLayout_5.addWidget(self.pos74, 7, 4, 1, 1)
        self.pos72 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos72.setObjectName(_fromUtf8("pos72"))
        self.gridLayout_5.addWidget(self.pos72, 7, 2, 1, 1)
        self.pos71 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos71.setObjectName(_fromUtf8("pos71"))
        self.gridLayout_5.addWidget(self.pos71, 7, 1, 1, 1)
        self.pos73 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos73.setObjectName(_fromUtf8("pos73"))
        self.gridLayout_5.addWidget(self.pos73, 7, 3, 1, 1)
        self.pos77 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos77.setObjectName(_fromUtf8("pos77"))
        self.gridLayout_5.addWidget(self.pos77, 7, 7, 1, 1)
        self.pos70 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos70.setObjectName(_fromUtf8("pos70"))
        self.gridLayout_5.addWidget(self.pos70, 7, 0, 1, 1)
        self.pos90 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos90.setObjectName(_fromUtf8("pos90"))
        self.gridLayout_5.addWidget(self.pos90, 9, 0, 1, 1)
        self.pos80 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos80.setObjectName(_fromUtf8("pos80"))
        self.gridLayout_5.addWidget(self.pos80, 8, 0, 1, 1)
        self.pos76 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos76.setObjectName(_fromUtf8("pos76"))
        self.gridLayout_5.addWidget(self.pos76, 7, 6, 1, 1)
        self.pos50 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos50.setObjectName(_fromUtf8("pos50"))
        self.gridLayout_5.addWidget(self.pos50, 5, 0, 1, 1)
        self.pos60 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos60.setObjectName(_fromUtf8("pos60"))
        self.gridLayout_5.addWidget(self.pos60, 6, 0, 1, 1)
        self.pos78 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos78.setObjectName(_fromUtf8("pos78"))
        self.gridLayout_5.addWidget(self.pos78, 7, 8, 1, 1)
        self.pos79 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos79.setObjectName(_fromUtf8("pos79"))
        self.gridLayout_5.addWidget(self.pos79, 7, 9, 1, 1)
        self.pos05 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos05.setObjectName(_fromUtf8("pos05"))
        self.gridLayout_5.addWidget(self.pos05, 0, 5, 1, 1)
        self.pos28 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos28.setObjectName(_fromUtf8("pos28"))
        self.gridLayout_5.addWidget(self.pos28, 2, 8, 1, 1)
        self.pos16 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos16.setObjectName(_fromUtf8("pos16"))
        self.gridLayout_5.addWidget(self.pos16, 1, 6, 1, 1)
        self.pos26 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos26.setObjectName(_fromUtf8("pos26"))
        self.gridLayout_5.addWidget(self.pos26, 2, 6, 1, 1)
        self.pos17 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos17.setObjectName(_fromUtf8("pos17"))
        self.gridLayout_5.addWidget(self.pos17, 1, 7, 1, 1)
        self.pos08 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pos08.sizePolicy().hasHeightForWidth())
        self.pos08.setSizePolicy(sizePolicy)
        self.pos08.setObjectName(_fromUtf8("pos08"))
        self.gridLayout_5.addWidget(self.pos08, 0, 8, 1, 1)
        self.pos27 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos27.setObjectName(_fromUtf8("pos27"))
        self.gridLayout_5.addWidget(self.pos27, 2, 7, 1, 1)
        self.pos04 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos04.setObjectName(_fromUtf8("pos04"))
        self.gridLayout_5.addWidget(self.pos04, 0, 4, 1, 1)
        self.pos07 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos07.setObjectName(_fromUtf8("pos07"))
        self.gridLayout_5.addWidget(self.pos07, 0, 7, 1, 1)
        self.pos29 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos29.setObjectName(_fromUtf8("pos29"))
        self.gridLayout_5.addWidget(self.pos29, 2, 9, 1, 1)
        self.pos06 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos06.setObjectName(_fromUtf8("pos06"))
        self.gridLayout_5.addWidget(self.pos06, 0, 6, 1, 1)
        self.pos39 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos39.setObjectName(_fromUtf8("pos39"))
        self.gridLayout_5.addWidget(self.pos39, 3, 9, 1, 1)
        self.pos48 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos48.setObjectName(_fromUtf8("pos48"))
        self.gridLayout_5.addWidget(self.pos48, 4, 8, 1, 1)
        self.pos47 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos47.setObjectName(_fromUtf8("pos47"))
        self.gridLayout_5.addWidget(self.pos47, 4, 7, 1, 1)
        self.pos24 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos24.setObjectName(_fromUtf8("pos24"))
        self.gridLayout_5.addWidget(self.pos24, 2, 4, 1, 1)
        self.pos14 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos14.setObjectName(_fromUtf8("pos14"))
        self.gridLayout_5.addWidget(self.pos14, 1, 4, 1, 1)
        self.pos19 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos19.setObjectName(_fromUtf8("pos19"))
        self.gridLayout_5.addWidget(self.pos19, 1, 9, 1, 1)
        self.pos18 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos18.setObjectName(_fromUtf8("pos18"))
        self.gridLayout_5.addWidget(self.pos18, 1, 8, 1, 1)
        self.pos34 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos34.setObjectName(_fromUtf8("pos34"))
        self.gridLayout_5.addWidget(self.pos34, 3, 4, 1, 1)
        self.pos36 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos36.setObjectName(_fromUtf8("pos36"))
        self.gridLayout_5.addWidget(self.pos36, 3, 6, 1, 1)
        self.pos38 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos38.setObjectName(_fromUtf8("pos38"))
        self.gridLayout_5.addWidget(self.pos38, 3, 8, 1, 1)
        self.pos46 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos46.setObjectName(_fromUtf8("pos46"))
        self.gridLayout_5.addWidget(self.pos46, 4, 6, 1, 1)
        self.pos37 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos37.setObjectName(_fromUtf8("pos37"))
        self.gridLayout_5.addWidget(self.pos37, 3, 7, 1, 1)
        self.pos44 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos44.setObjectName(_fromUtf8("pos44"))
        self.gridLayout_5.addWidget(self.pos44, 4, 4, 1, 1)
        self.pos61 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos61.setObjectName(_fromUtf8("pos61"))
        self.gridLayout_5.addWidget(self.pos61, 6, 1, 1, 1)
        self.pos62 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos62.setObjectName(_fromUtf8("pos62"))
        self.gridLayout_5.addWidget(self.pos62, 6, 2, 1, 1)
        self.pos49 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos49.setObjectName(_fromUtf8("pos49"))
        self.gridLayout_5.addWidget(self.pos49, 4, 9, 1, 1)
        self.pos09 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos09.setObjectName(_fromUtf8("pos09"))
        self.gridLayout_5.addWidget(self.pos09, 0, 9, 1, 1)
        self.pos93 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos93.setObjectName(_fromUtf8("pos93"))
        self.gridLayout_5.addWidget(self.pos93, 9, 3, 1, 1)
        self.pos83 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos83.setObjectName(_fromUtf8("pos83"))
        self.gridLayout_5.addWidget(self.pos83, 8, 3, 1, 1)
        self.pos84 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos84.setObjectName(_fromUtf8("pos84"))
        self.gridLayout_5.addWidget(self.pos84, 8, 4, 1, 1)
        self.pos85 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos85.setObjectName(_fromUtf8("pos85"))
        self.gridLayout_5.addWidget(self.pos85, 8, 5, 1, 1)
        self.pos82 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos82.setObjectName(_fromUtf8("pos82"))
        self.gridLayout_5.addWidget(self.pos82, 8, 2, 1, 1)
        self.pos92 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos92.setObjectName(_fromUtf8("pos92"))
        self.gridLayout_5.addWidget(self.pos92, 9, 2, 1, 1)
        self.pos86 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos86.setObjectName(_fromUtf8("pos86"))
        self.gridLayout_5.addWidget(self.pos86, 8, 6, 1, 1)
        self.pos81 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos81.setObjectName(_fromUtf8("pos81"))
        self.gridLayout_5.addWidget(self.pos81, 8, 1, 1, 1)
        self.pos94 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos94.setObjectName(_fromUtf8("pos94"))
        self.gridLayout_5.addWidget(self.pos94, 9, 4, 1, 1)
        self.pos91 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos91.setObjectName(_fromUtf8("pos91"))
        self.gridLayout_5.addWidget(self.pos91, 9, 1, 1, 1)
        self.pos95 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos95.setObjectName(_fromUtf8("pos95"))
        self.gridLayout_5.addWidget(self.pos95, 9, 5, 1, 1)
        self.pos89 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos89.setObjectName(_fromUtf8("pos89"))
        self.gridLayout_5.addWidget(self.pos89, 8, 9, 1, 1)
        self.pos88 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos88.setObjectName(_fromUtf8("pos88"))
        self.gridLayout_5.addWidget(self.pos88, 8, 8, 1, 1)
        self.pos96 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos96.setObjectName(_fromUtf8("pos96"))
        self.gridLayout_5.addWidget(self.pos96, 9, 6, 1, 1)
        self.pos97 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos97.setObjectName(_fromUtf8("pos97"))
        self.gridLayout_5.addWidget(self.pos97, 9, 7, 1, 1)
        self.pos87 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos87.setObjectName(_fromUtf8("pos87"))
        self.gridLayout_5.addWidget(self.pos87, 8, 7, 1, 1)
        self.pos98 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pos98.setObjectName(_fromUtf8("pos98"))
        self.gridLayout_5.addWidget(self.pos98, 9, 8, 1, 1)
        self.pos99 = QtGui.QPushButton(self.gridLayoutWidget)
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
        self.gridLayout_7.addWidget(self.reload_board, 2, 1, 1, 1)
        self.execute_code = QtGui.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.execute_code.setFont(font)
        self.execute_code.setObjectName(_fromUtf8("execute_code"))
        self.gridLayout_7.addWidget(self.execute_code, 2, 0, 1, 1)
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



    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pos00.setText(_translate("MainWindow", "00", None))
        self.pos01.setText(_translate("MainWindow", "01", None))
        self.pos02.setText(_translate("MainWindow", "02", None))
        self.pos03.setText(_translate("MainWindow", "03", None))
        self.pos04.setText(_translate("MainWindow", "04", None))
        self.pos05.setText(_translate("MainWindow", "05", None))
        self.pos06.setText(_translate("MainWindow", "06", None))
        self.pos07.setText(_translate("MainWindow", "07", None))
        self.pos08.setText(_translate("MainWindow", "08", None))
        self.pos09.setText(_translate("MainWindow", "09", None))

        self.pos10.setText(_translate("MainWindow", "10", None))
        self.pos11.setText(_translate("MainWindow", "11", None))
        self.pos12.setText(_translate("MainWindow", "12", None))
        self.pos13.setText(_translate("MainWindow", "13", None))
        self.pos14.setText(_translate("MainWindow", "14", None))
        self.pos15.setText(_translate("MainWindow", "15", None))
        self.pos16.setText(_translate("MainWindow", "16", None))
        self.pos17.setText(_translate("MainWindow", "17", None))
        self.pos18.setText(_translate("MainWindow", "18", None))
        self.pos19.setText(_translate("MainWindow", "19", None))

        self.pos20.setText(_translate("MainWindow", "20", None))
        self.pos21.setText(_translate("MainWindow", "21", None))
        self.pos22.setText(_translate("MainWindow", "22", None))
        self.pos23.setText(_translate("MainWindow", "23", None))
        self.pos24.setText(_translate("MainWindow", "24", None))
        self.pos25.setText(_translate("MainWindow", "25", None))
        self.pos26.setText(_translate("MainWindow", "26", None))
        self.pos27.setText(_translate("MainWindow", "27", None))
        self.pos28.setText(_translate("MainWindow", "28", None))
        self.pos29.setText(_translate("MainWindow", "29", None))


        self.pos30.setText(_translate("MainWindow", "30", None))
        self.pos31.setText(_translate("MainWindow", "31", None))
        self.pos32.setText(_translate("MainWindow", "32", None))
        self.pos33.setText(_translate("MainWindow", "33", None))
        self.pos34.setText(_translate("MainWindow", "34", None))
        self.pos35.setText(_translate("MainWindow", "35", None))
        self.pos36.setText(_translate("MainWindow", "36", None))
        self.pos37.setText(_translate("MainWindow", "37", None))
        self.pos38.setText(_translate("MainWindow", "38", None))
        self.pos39.setText(_translate("MainWindow", "39", None))

        self.pos40.setText(_translate("MainWindow", "40", None))
        self.pos41.setText(_translate("MainWindow", "41", None))
        self.pos42.setText(_translate("MainWindow", "42", None))
        self.pos43.setText(_translate("MainWindow", "43", None))
        self.pos44.setText(_translate("MainWindow", "44", None))
        self.pos45.setText(_translate("MainWindow", "45", None))
        self.pos46.setText(_translate("MainWindow", "46", None))
        self.pos47.setText(_translate("MainWindow", "47", None))
        self.pos48.setText(_translate("MainWindow", "48", None))
        self.pos49.setText(_translate("MainWindow", "49", None))

        self.pos50.setText(_translate("MainWindow", "50", None))
        self.pos51.setText(_translate("MainWindow", "51", None))
        self.pos52.setText(_translate("MainWindow", "52", None))
        self.pos53.setText(_translate("MainWindow", "53", None))
        self.pos54.setText(_translate("MainWindow", "54", None))
        self.pos55.setText(_translate("MainWindow", "55", None))
        self.pos56.setText(_translate("MainWindow", "56", None))
        self.pos57.setText(_translate("MainWindow", "57", None))
        self.pos58.setText(_translate("MainWindow", "58", None))
        self.pos59.setText(_translate("MainWindow", "59", None))


        self.pos60.setText(_translate("MainWindow", "60", None))
        self.pos61.setText(_translate("MainWindow", "61", None))
        self.pos62.setText(_translate("MainWindow", "62", None))
        self.pos63.setText(_translate("MainWindow", "63", None))
        self.pos64.setText(_translate("MainWindow", "64", None))
        self.pos65.setText(_translate("MainWindow", "65", None))
        self.pos66.setText(_translate("MainWindow", "66", None))
        self.pos67.setText(_translate("MainWindow", "67", None))
        self.pos68.setText(_translate("MainWindow", "68", None))
        self.pos69.setText(_translate("MainWindow", "69", None))


        self.pos70.setText(_translate("MainWindow", "70", None))
        self.pos71.setText(_translate("MainWindow", "71", None))
        self.pos72.setText(_translate("MainWindow", "72", None))
        self.pos73.setText(_translate("MainWindow", "73", None))
        self.pos74.setText(_translate("MainWindow", "74", None))
        self.pos75.setText(_translate("MainWindow", "75", None))
        self.pos76.setText(_translate("MainWindow", "76", None))
        self.pos77.setText(_translate("MainWindow", "77", None))
        self.pos78.setText(_translate("MainWindow", "78", None))
        self.pos79.setText(_translate("MainWindow", "79", None))


        self.pos80.setText(_translate("MainWindow", "80", None))
        self.pos81.setText(_translate("MainWindow", "81", None))
        self.pos82.setText(_translate("MainWindow", "82", None))
        self.pos83.setText(_translate("MainWindow", "83", None))
        self.pos84.setText(_translate("MainWindow", "84", None))
        self.pos85.setText(_translate("MainWindow", "85", None))
        self.pos86.setText(_translate("MainWindow", "86", None))
        self.pos87.setText(_translate("MainWindow", "87", None))
        self.pos88.setText(_translate("MainWindow", "88", None))
        self.pos89.setText(_translate("MainWindow", "89", None))

        self.pos90.setText(_translate("MainWindow", "90", None))
        self.pos91.setText(_translate("MainWindow", "91", None))
        self.pos92.setText(_translate("MainWindow", "92", None))
        self.pos93.setText(_translate("MainWindow", "93", None))
        self.pos94.setText(_translate("MainWindow", "94", None))
        self.pos95.setText(_translate("MainWindow", "95", None))
        self.pos96.setText(_translate("MainWindow", "96", None))
        self.pos97.setText(_translate("MainWindow", "97", None))
        self.pos98.setText(_translate("MainWindow", "98", None))
        self.pos99.setText(_translate("MainWindow", "99", None))








        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">class program {</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">    program() {</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        move()</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">    }</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">}</span></p></body></html>", None))
        self.reload_board.setText(_translate("MainWindow", "Reload Board", None))
        self.execute_code.setText(_translate("MainWindow", "Execute code", None))
        self.label.setText(_translate("MainWindow", "Karel code", None))
        self.label_2.setText(_translate("MainWindow", "Board", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())








