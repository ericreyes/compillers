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
        self.pushButton_31 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_31.setObjectName(_fromUtf8("pushButton_31"))
        self.gridLayout_5.addWidget(self.pushButton_31, 0, 3, 1, 1)
        self.pushButton_21 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_21.setObjectName(_fromUtf8("pushButton_21"))
        self.gridLayout_5.addWidget(self.pushButton_21, 2, 1, 1, 1)
        self.pushButton_22 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_22.setObjectName(_fromUtf8("pushButton_22"))
        self.gridLayout_5.addWidget(self.pushButton_22, 0, 1, 1, 1)
        self.pushButton_25 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_25.setObjectName(_fromUtf8("pushButton_25"))
        self.gridLayout_5.addWidget(self.pushButton_25, 3, 1, 1, 1)
        self.pushButton_23 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_23.setObjectName(_fromUtf8("pushButton_23"))
        self.gridLayout_5.addWidget(self.pushButton_23, 2, 3, 1, 1)
        self.pushButton_26 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_26.setObjectName(_fromUtf8("pushButton_26"))
        self.gridLayout_5.addWidget(self.pushButton_26, 0, 0, 1, 1)
        self.pushButton_24 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_24.setObjectName(_fromUtf8("pushButton_24"))
        self.gridLayout_5.addWidget(self.pushButton_24, 0, 2, 1, 1)
        self.pushButton_27 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_27.setObjectName(_fromUtf8("pushButton_27"))
        self.gridLayout_5.addWidget(self.pushButton_27, 1, 0, 1, 1)
        self.pushButton_30 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_30.setObjectName(_fromUtf8("pushButton_30"))
        self.gridLayout_5.addWidget(self.pushButton_30, 4, 2, 1, 1)
        self.pushButton_28 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_28.setObjectName(_fromUtf8("pushButton_28"))
        self.gridLayout_5.addWidget(self.pushButton_28, 3, 0, 1, 1)
        self.pushButton_29 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_29.setObjectName(_fromUtf8("pushButton_29"))
        self.gridLayout_5.addWidget(self.pushButton_29, 2, 0, 1, 1)
        self.pushButton_34 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_34.setObjectName(_fromUtf8("pushButton_34"))
        self.gridLayout_5.addWidget(self.pushButton_34, 3, 2, 1, 1)
        self.pushButton_32 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_32.setObjectName(_fromUtf8("pushButton_32"))
        self.gridLayout_5.addWidget(self.pushButton_32, 1, 3, 1, 1)
        self.pushButton_33 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_33.setObjectName(_fromUtf8("pushButton_33"))
        self.gridLayout_5.addWidget(self.pushButton_33, 2, 2, 1, 1)
        self.pushButton_35 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_35.setObjectName(_fromUtf8("pushButton_35"))
        self.gridLayout_5.addWidget(self.pushButton_35, 3, 3, 1, 1)
        self.pushButton_37 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_37.setObjectName(_fromUtf8("pushButton_37"))
        self.gridLayout_5.addWidget(self.pushButton_37, 1, 2, 1, 1)
        self.pushButton_38 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_38.setObjectName(_fromUtf8("pushButton_38"))
        self.gridLayout_5.addWidget(self.pushButton_38, 1, 1, 1, 1)
        self.pushButton_36 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_36.setObjectName(_fromUtf8("pushButton_36"))
        self.gridLayout_5.addWidget(self.pushButton_36, 4, 1, 1, 1)
        self.pushButton_39 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_39.setObjectName(_fromUtf8("pushButton_39"))
        self.gridLayout_5.addWidget(self.pushButton_39, 4, 0, 1, 1)
        self.pushButton_40 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_40.setObjectName(_fromUtf8("pushButton_40"))
        self.gridLayout_5.addWidget(self.pushButton_40, 4, 3, 1, 1)
        self.pushButton_130 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_130.setObjectName(_fromUtf8("pushButton_130"))
        self.gridLayout_5.addWidget(self.pushButton_130, 5, 1, 1, 1)
        self.pushButton_77 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_77.setObjectName(_fromUtf8("pushButton_77"))
        self.gridLayout_5.addWidget(self.pushButton_77, 5, 7, 1, 1)
        self.pushButton_76 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_76.setObjectName(_fromUtf8("pushButton_76"))
        self.gridLayout_5.addWidget(self.pushButton_76, 5, 8, 1, 1)
        self.pushButton_127 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_127.setObjectName(_fromUtf8("pushButton_127"))
        self.gridLayout_5.addWidget(self.pushButton_127, 5, 5, 1, 1)
        self.pushButton_79 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_79.setObjectName(_fromUtf8("pushButton_79"))
        self.gridLayout_5.addWidget(self.pushButton_79, 5, 6, 1, 1)
        self.pushButton_129 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_129.setObjectName(_fromUtf8("pushButton_129"))
        self.gridLayout_5.addWidget(self.pushButton_129, 5, 9, 1, 1)
        self.pushButton_78 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_78.setObjectName(_fromUtf8("pushButton_78"))
        self.gridLayout_5.addWidget(self.pushButton_78, 5, 2, 1, 1)
        self.pushButton_128 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_128.setObjectName(_fromUtf8("pushButton_128"))
        self.gridLayout_5.addWidget(self.pushButton_128, 5, 3, 1, 1)
        self.pushButton_126 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_126.setObjectName(_fromUtf8("pushButton_126"))
        self.gridLayout_5.addWidget(self.pushButton_126, 5, 4, 1, 1)
        self.pushButton_132 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_132.setObjectName(_fromUtf8("pushButton_132"))
        self.gridLayout_5.addWidget(self.pushButton_132, 6, 7, 1, 1)
        self.pushButton_133 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_133.setObjectName(_fromUtf8("pushButton_133"))
        self.gridLayout_5.addWidget(self.pushButton_133, 6, 3, 1, 1)
        self.pushButton_135 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_135.setObjectName(_fromUtf8("pushButton_135"))
        self.gridLayout_5.addWidget(self.pushButton_135, 6, 4, 1, 1)
        self.pushButton_131 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_131.setObjectName(_fromUtf8("pushButton_131"))
        self.gridLayout_5.addWidget(self.pushButton_131, 6, 5, 1, 1)
        self.pushButton_138 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_138.setObjectName(_fromUtf8("pushButton_138"))
        self.gridLayout_5.addWidget(self.pushButton_138, 6, 6, 1, 1)
        self.pushButton_136 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_136.setObjectName(_fromUtf8("pushButton_136"))
        self.gridLayout_5.addWidget(self.pushButton_136, 6, 8, 1, 1)
        self.pushButton_137 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_137.setObjectName(_fromUtf8("pushButton_137"))
        self.gridLayout_5.addWidget(self.pushButton_137, 6, 9, 1, 1)
        self.pushButton_61 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_61.setObjectName(_fromUtf8("pushButton_61"))
        self.gridLayout_5.addWidget(self.pushButton_61, 3, 5, 1, 1)
        self.pushButton_56 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_56.setObjectName(_fromUtf8("pushButton_56"))
        self.gridLayout_5.addWidget(self.pushButton_56, 2, 5, 1, 1)
        self.pushButton_66 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_66.setObjectName(_fromUtf8("pushButton_66"))
        self.gridLayout_5.addWidget(self.pushButton_66, 4, 5, 1, 1)
        self.pushButton_51 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_51.setObjectName(_fromUtf8("pushButton_51"))
        self.gridLayout_5.addWidget(self.pushButton_51, 1, 5, 1, 1)
        self.pushButton_143 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_143.setObjectName(_fromUtf8("pushButton_143"))
        self.gridLayout_5.addWidget(self.pushButton_143, 7, 5, 1, 1)
        self.pushButton_144 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_144.setObjectName(_fromUtf8("pushButton_144"))
        self.gridLayout_5.addWidget(self.pushButton_144, 7, 4, 1, 1)
        self.pushButton_146 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_146.setObjectName(_fromUtf8("pushButton_146"))
        self.gridLayout_5.addWidget(self.pushButton_146, 7, 2, 1, 1)
        self.pushButton_148 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_148.setObjectName(_fromUtf8("pushButton_148"))
        self.gridLayout_5.addWidget(self.pushButton_148, 7, 1, 1, 1)
        self.pushButton_147 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_147.setObjectName(_fromUtf8("pushButton_147"))
        self.gridLayout_5.addWidget(self.pushButton_147, 7, 3, 1, 1)
        self.pushButton_140 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_140.setObjectName(_fromUtf8("pushButton_140"))
        self.gridLayout_5.addWidget(self.pushButton_140, 7, 7, 1, 1)
        self.pushButton_71 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_71.setObjectName(_fromUtf8("pushButton_71"))
        self.gridLayout_5.addWidget(self.pushButton_71, 7, 0, 1, 1)
        self.pushButton_75 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_75.setObjectName(_fromUtf8("pushButton_75"))
        self.gridLayout_5.addWidget(self.pushButton_75, 9, 0, 1, 1)
        self.pushButton_72 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_72.setObjectName(_fromUtf8("pushButton_72"))
        self.gridLayout_5.addWidget(self.pushButton_72, 8, 0, 1, 1)
        self.pushButton_145 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_145.setObjectName(_fromUtf8("pushButton_145"))
        self.gridLayout_5.addWidget(self.pushButton_145, 7, 6, 1, 1)
        self.pushButton_74 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_74.setObjectName(_fromUtf8("pushButton_74"))
        self.gridLayout_5.addWidget(self.pushButton_74, 5, 0, 1, 1)
        self.pushButton_73 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_73.setObjectName(_fromUtf8("pushButton_73"))
        self.gridLayout_5.addWidget(self.pushButton_73, 6, 0, 1, 1)
        self.pushButton_141 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_141.setObjectName(_fromUtf8("pushButton_141"))
        self.gridLayout_5.addWidget(self.pushButton_141, 7, 8, 1, 1)
        self.pushButton_142 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_142.setObjectName(_fromUtf8("pushButton_142"))
        self.gridLayout_5.addWidget(self.pushButton_142, 7, 9, 1, 1)
        self.pushButton_42 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_42.setObjectName(_fromUtf8("pushButton_42"))
        self.gridLayout_5.addWidget(self.pushButton_42, 0, 5, 1, 1)
        self.pushButton_54 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_54.setObjectName(_fromUtf8("pushButton_54"))
        self.gridLayout_5.addWidget(self.pushButton_54, 2, 8, 1, 1)
        self.pushButton_49 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_49.setObjectName(_fromUtf8("pushButton_49"))
        self.gridLayout_5.addWidget(self.pushButton_49, 1, 6, 1, 1)
        self.pushButton_55 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_55.setObjectName(_fromUtf8("pushButton_55"))
        self.gridLayout_5.addWidget(self.pushButton_55, 2, 6, 1, 1)
        self.pushButton_48 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_48.setObjectName(_fromUtf8("pushButton_48"))
        self.gridLayout_5.addWidget(self.pushButton_48, 1, 7, 1, 1)
        self.pushButton_45 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_45.sizePolicy().hasHeightForWidth())
        self.pushButton_45.setSizePolicy(sizePolicy)
        self.pushButton_45.setObjectName(_fromUtf8("pushButton_45"))
        self.gridLayout_5.addWidget(self.pushButton_45, 0, 8, 1, 1)
        self.pushButton_53 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_53.setObjectName(_fromUtf8("pushButton_53"))
        self.gridLayout_5.addWidget(self.pushButton_53, 2, 7, 1, 1)
        self.pushButton_41 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_41.setObjectName(_fromUtf8("pushButton_41"))
        self.gridLayout_5.addWidget(self.pushButton_41, 0, 4, 1, 1)
        self.pushButton_44 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_44.setObjectName(_fromUtf8("pushButton_44"))
        self.gridLayout_5.addWidget(self.pushButton_44, 0, 7, 1, 1)
        self.pushButton_52 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_52.setObjectName(_fromUtf8("pushButton_52"))
        self.gridLayout_5.addWidget(self.pushButton_52, 2, 9, 1, 1)
        self.pushButton_43 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_43.setObjectName(_fromUtf8("pushButton_43"))
        self.gridLayout_5.addWidget(self.pushButton_43, 0, 6, 1, 1)
        self.pushButton_59 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_59.setObjectName(_fromUtf8("pushButton_59"))
        self.gridLayout_5.addWidget(self.pushButton_59, 3, 9, 1, 1)
        self.pushButton_64 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_64.setObjectName(_fromUtf8("pushButton_64"))
        self.gridLayout_5.addWidget(self.pushButton_64, 4, 8, 1, 1)
        self.pushButton_63 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_63.setObjectName(_fromUtf8("pushButton_63"))
        self.gridLayout_5.addWidget(self.pushButton_63, 4, 7, 1, 1)
        self.pushButton_68 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_68.setObjectName(_fromUtf8("pushButton_68"))
        self.gridLayout_5.addWidget(self.pushButton_68, 2, 4, 1, 1)
        self.pushButton_67 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_67.setObjectName(_fromUtf8("pushButton_67"))
        self.gridLayout_5.addWidget(self.pushButton_67, 1, 4, 1, 1)
        self.pushButton_50 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_50.setObjectName(_fromUtf8("pushButton_50"))
        self.gridLayout_5.addWidget(self.pushButton_50, 1, 9, 1, 1)
        self.pushButton_47 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_47.setObjectName(_fromUtf8("pushButton_47"))
        self.gridLayout_5.addWidget(self.pushButton_47, 1, 8, 1, 1)
        self.pushButton_69 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_69.setObjectName(_fromUtf8("pushButton_69"))
        self.gridLayout_5.addWidget(self.pushButton_69, 3, 4, 1, 1)
        self.pushButton_58 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_58.setObjectName(_fromUtf8("pushButton_58"))
        self.gridLayout_5.addWidget(self.pushButton_58, 3, 6, 1, 1)
        self.pushButton_57 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_57.setObjectName(_fromUtf8("pushButton_57"))
        self.gridLayout_5.addWidget(self.pushButton_57, 3, 8, 1, 1)
        self.pushButton_65 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_65.setObjectName(_fromUtf8("pushButton_65"))
        self.gridLayout_5.addWidget(self.pushButton_65, 4, 6, 1, 1)
        self.pushButton_60 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_60.setObjectName(_fromUtf8("pushButton_60"))
        self.gridLayout_5.addWidget(self.pushButton_60, 3, 7, 1, 1)
        self.pushButton_70 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_70.setObjectName(_fromUtf8("pushButton_70"))
        self.gridLayout_5.addWidget(self.pushButton_70, 4, 4, 1, 1)
        self.pushButton_139 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_139.setObjectName(_fromUtf8("pushButton_139"))
        self.gridLayout_5.addWidget(self.pushButton_139, 6, 1, 1, 1)
        self.pushButton_134 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_134.setObjectName(_fromUtf8("pushButton_134"))
        self.gridLayout_5.addWidget(self.pushButton_134, 6, 2, 1, 1)
        self.pushButton_62 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_62.setObjectName(_fromUtf8("pushButton_62"))
        self.gridLayout_5.addWidget(self.pushButton_62, 4, 9, 1, 1)
        self.pushButton_46 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_46.setObjectName(_fromUtf8("pushButton_46"))
        self.gridLayout_5.addWidget(self.pushButton_46, 0, 9, 1, 1)
        self.pushButton_158 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_158.setObjectName(_fromUtf8("pushButton_158"))
        self.gridLayout_5.addWidget(self.pushButton_158, 9, 3, 1, 1)
        self.pushButton_151 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_151.setObjectName(_fromUtf8("pushButton_151"))
        self.gridLayout_5.addWidget(self.pushButton_151, 8, 3, 1, 1)
        self.pushButton_150 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_150.setObjectName(_fromUtf8("pushButton_150"))
        self.gridLayout_5.addWidget(self.pushButton_150, 8, 4, 1, 1)
        self.pushButton_153 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_153.setObjectName(_fromUtf8("pushButton_153"))
        self.gridLayout_5.addWidget(self.pushButton_153, 8, 5, 1, 1)
        self.pushButton_155 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_155.setObjectName(_fromUtf8("pushButton_155"))
        self.gridLayout_5.addWidget(self.pushButton_155, 8, 2, 1, 1)
        self.pushButton_161 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_161.setObjectName(_fromUtf8("pushButton_161"))
        self.gridLayout_5.addWidget(self.pushButton_161, 9, 2, 1, 1)
        self.pushButton_149 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_149.setObjectName(_fromUtf8("pushButton_149"))
        self.gridLayout_5.addWidget(self.pushButton_149, 8, 6, 1, 1)
        self.pushButton_157 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_157.setObjectName(_fromUtf8("pushButton_157"))
        self.gridLayout_5.addWidget(self.pushButton_157, 8, 1, 1, 1)
        self.pushButton_164 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_164.setObjectName(_fromUtf8("pushButton_164"))
        self.gridLayout_5.addWidget(self.pushButton_164, 9, 4, 1, 1)
        self.pushButton_166 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_166.setObjectName(_fromUtf8("pushButton_166"))
        self.gridLayout_5.addWidget(self.pushButton_166, 9, 1, 1, 1)
        self.pushButton_165 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_165.setObjectName(_fromUtf8("pushButton_165"))
        self.gridLayout_5.addWidget(self.pushButton_165, 9, 5, 1, 1)
        self.pushButton_156 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_156.setObjectName(_fromUtf8("pushButton_156"))
        self.gridLayout_5.addWidget(self.pushButton_156, 8, 9, 1, 1)
        self.pushButton_154 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_154.setObjectName(_fromUtf8("pushButton_154"))
        self.gridLayout_5.addWidget(self.pushButton_154, 8, 8, 1, 1)
        self.pushButton_159 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_159.setObjectName(_fromUtf8("pushButton_159"))
        self.gridLayout_5.addWidget(self.pushButton_159, 9, 6, 1, 1)
        self.pushButton_162 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_162.setObjectName(_fromUtf8("pushButton_162"))
        self.gridLayout_5.addWidget(self.pushButton_162, 9, 7, 1, 1)
        self.pushButton_152 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_152.setObjectName(_fromUtf8("pushButton_152"))
        self.gridLayout_5.addWidget(self.pushButton_152, 8, 7, 1, 1)
        self.pushButton_160 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_160.setObjectName(_fromUtf8("pushButton_160"))
        self.gridLayout_5.addWidget(self.pushButton_160, 9, 8, 1, 1)
        self.pushButton_163 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_163.setObjectName(_fromUtf8("pushButton_163"))
        self.gridLayout_5.addWidget(self.pushButton_163, 9, 9, 1, 1)
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
        self.pushButton_62.raise_()
        self.pushButton_46.raise_()
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
        self.pushButton_31.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_21.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_22.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_25.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_23.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_26.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_24.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_27.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_30.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_28.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_29.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_34.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_32.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_33.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_35.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_37.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_38.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_36.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_39.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_40.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_130.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_77.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_76.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_127.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_79.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_129.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_78.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_128.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_126.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_132.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_133.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_135.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_131.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_138.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_136.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_137.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_61.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_56.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_66.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_51.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_143.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_144.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_146.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_148.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_147.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_140.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_71.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_75.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_72.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_145.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_74.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_73.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_141.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_142.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_42.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_54.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_49.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_55.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_48.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_45.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_53.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_41.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_44.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_52.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_43.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_59.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_64.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_63.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_68.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_67.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_50.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_47.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_69.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_58.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_57.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_65.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_60.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_70.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_139.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_134.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_62.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_46.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_158.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_151.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_150.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_153.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_155.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_161.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_149.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_157.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_164.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_166.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_165.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_156.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_154.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_159.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_162.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_152.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_160.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_163.setText(_translate("MainWindow", "PushButton", None))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">class program {</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">    program() {</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">        move()</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">    }</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">}</span></p></body></html>", None))
        self.reload_board.setText(_translate("MainWindow", "Reload Board", None))
        self.execute_code.setText(_translate("MainWindow", "Execute code", None))
        self.label.setText(_translate("MainWindow", "Karel code", None))
        self.label_2.setText(_translate("MainWindow", "Board", None))


# if __name__ == "__main__":
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     MainWindow = QtGui.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())








