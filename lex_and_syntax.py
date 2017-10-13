import ply.lex as lex

class OurLexer(object):
    # List of token names.   This is always required
    global reserved
    reserved = {
        'class': 'CLASS',
        'program':'PROGRAM',
        'void':'VOID',
        'iterate':'ITERATE',
        'isclear':'ISCLEAR',
        'isblocked':'ISBLOCKED',
        'nexttobeeper':'NEXTTOBEEPER',
        'notnexttobeeper':'NOTNEXTTOBEEPER',
        'facing':'FACING',
        'notfacing':'NOTFACING',
        'anybeepers':'ANYBEEPERS',
        'nobeepers':'NOBEEPERS',
        'front':'FRONT',
        'left':'LEFT',
        'right':'RIGHT',
        'north':'NORTH',
        'south':'SOUTH',
        'east':'EAST',
        'west':'WEST',
        'move':'MOVE',
        'turnleft':'TURNLEFT',
        'pickbeeper':'PICKBEEPER',
        'putbeeper':'PUTBEEPER',
        'end':'END',
        'if': 'IF',
        'else':'ELSE',
        'while': 'WHILE',
    }

    tokens = [
        'LBRACKET',
        'RBRACKET',
        'LPAREN',
        'RPAREN',
        'IDENTIFIER'
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
      r'[a-zA-Z_][a-zA-Z_0-9]*'
      global reserved
      token.type = reserved.get(token.value,'IDENTIFIER')    # Check for reserved words
      return token

    def t_NUMBER(self, t):
      r'\d+'
      t.value = int(t.value)
      return t

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

    def get_tokens(self,data):
      self.lexer.input(data)
      token_values = []
      while True:
        token = self.lexer.token()
        if not token:
          break
        token_values.append(token.value)
      return token_values

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
    print ('VERIFICAR TIENE A {} EN LA MIRA'.format(next_token))
    return expected_token == next_token

global counter
counter = 0

def exigir(expected_token):
    global all_tokens
    next_token = all_tokens.pop()

    global counter
    counter = counter + 1
    print (counter, all_tokens)
    print ('')
    return expected_token == next_token

def mostrarError():
    raise Exception('Unexpected token ;)  -- mamamlon')




#------TERMINADO------
#<program> ::= "class" "program" "{" <functions> <main function> "}"
def program():
  if ( exigir("class") ):
    if ( exigir("program") ):
      if ( exigir("{") ):
        functions()
        main_function()
        if ( not exigir("}") ):
          mostrarError()
      else:
          mostrarError()
    else:
        mostrarError()
  else:
      mostrarError()


#------TERMINADO------
#<functions> ::= <function> <functions prima> | lambda
def functions():
  if (verificar("void")):
    function()
    functions_prima()



#------TERMINADO------
#<functions prima> ::= <function> <functions prima> | lambda
def functions_prima():
  if (verificar("void")):
    function()
    functions_prima()



#------TERMINADO------
def main_function():
  if (exigir ("program") ):
    if (exigir ("(") ):
      if (exigir (")") ):
        if (exigir ("{")):
          body()
          if (not exigir("}")):
            mostrarError()
        else:
           mostrarError()
      else:
         mostrarError()
    else:
       mostrarError()
  else:
     mostrarError()


#------TERMINADO------
#<function> ::= "void" <name function> "("  ")" "{" <body> "}"
def function():
  if (exigir("void")):
    name_function()
    if (exigir("(")):
      if (exigir(")")):
        print ('EXIJO BRACKETS EN FUNCTION')
        if (exigir("{")):
          body()
          if (not exigir("}")):
            mostrarError()
        else:
           mostrarError()
      else:
         mostrarError()
    else:
       mostrarError()
  else:
     mostrarError()


#------TERMINADO------
#<body> ::= <expression> <body prima>
def body():
  print ('expresssion llamada en body normalito')
  expression()
  body_prima()


#------TERMINADO------
#<body prima> ::= <expression> <body prima> | lambda
def body_prima():
  print ('entra a body prima ')
  if ( verificar("if") or verificar( "while" ) or verificar( "iterate" ) or verificar('move') or verificar("turnLeft") or verificar("pickBeeper") or verificar("putBeeper") or verificar("end")):
    expression()
    body_prima()
  #else lambda


#------TERMINADO------
#<expression> ::= <call function> | <if expression> | <while expression> | <iterate expression>
def expression():
  if ( verificar("if") ):
    if_expression()
  elif ( verificar( "while" ) ):
    while_expression()
  elif ( verificar( "iterate" ) ):
    iterate_expression()
  else:
    call_function()



#------TERMINADO------
#verificar que no es palabra reservada
# <call function> ::= <name function> "(" ")"
def call_function():
  name_function()
  print ('exigiendo parentesis en call function')
  if (exigir("(")):
    if (not exigir(")")):
      mostrarError()
  else:
    mostrarError()
  print ('CALL FUNCTION, SE CHINGO PARENTESIS')


#------TERMINADO------
#<name function> ::= <official function> | <customer function>
def name_function():
  if (verificar('move') or verificar("turnLeft") or verificar("pickBeeper") or verificar("putBeeper") or verificar("end")):
    official_function()
  else:
    customer_function()

def customer_function():
  print ('no tenemos CUSTOMER FUNCTION lol')

#------TERMINADO------
#<if expression> ::= "if" "(" <condition> ")" "{" <body>  "}" <else>
def if_expression():
  if (exigir("if")):
    if (exigir("(")):
      condition()
      if (exigir(")")):
        if (exigir("{")):
          body()
          if (exigir("}")):
            else_expression()
          else:
             mostrarError()
        else:
           mostrarError()
      else:
         mostrarError()
    else:
       mostrarError()
  else:
     mostrarError()


#------TERMINADO------
#<else> ::= "else" "{" <body> "}"  | lambda
def else_expression():
  if (verificar("else")):
    if (exigir("else")):
      if (exigir("{")):
        body()
        if (not exigir("}")):
            mostrarError()
      else:
        mostrarError()
    else:
      mostrarError()
  #else Lambda


#------TERMINADO------
#<while> ::= "while" "(" <condition> ")" "{" <body> "}"
def while_expression():
  if (exigir("while")):
    if (exigir("(")):
      condition()
      if (exigir(")")):
        if (exigir("{")):
          body()
          if (not exigir("}")):
            mostrarError()
        else:
           mostrarError()
      else:
         mostrarError()
    else:
       mostrarError()
  else:
     mostrarError()


#------TERMINADO------
#<iterate expression> ::= "iterate" "(" <number> ")" "{" <body> "}"
def iterate_expression():
  if (exigir("iterate")):
    if (exigir("(")):
      number()
      if (exigir(")")):
        if (exigir("{")):
          body()
          if (not exigir("}")):
            mostrarError()
        else:
           mostrarError()
      else:
         mostrarError()
    else:
       mostrarError()
  else:
     mostrarError()



#------TERMINADO------
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
    mostrarError()


#------TERMINADO------
#<official function> ::= "move" | "turnLeft" | "pickBeeper" | "putBeeper" | "end"
def official_function():
  print ('official FUNCTIOOOOOOOOOOON')
  if (verificar("move")):
    print('POP DE MOVEEEEEEEEEEEEEEEEEEEEEE')
    exigir("move")
  elif (verificar("turnLeft")):
    exigir("turnLeft")
  elif (verificar("pickBeeper")):
    exigir("pickBeeper")
  elif (verificar("putBeeper")):
    exigir("putBeeper")
  elif (verificar("end")):
    exigir("end")
  else:
    mostrarError()



karel_program = open('karel.txt').read()
lexer = OurLexer()
lexer.build()


#lexer.test(karel_program)



all_tokens = lexer.get_tokens(karel_program)
all_tokens.reverse()
#print (all_tokens)

all_tokens2 = all_tokens




program()




#------SIN TERMINAR------
#aquí vamos a comparar con todas las palabras reservadas (no todos los tokens, solo las palabras reservadas).
#<customer function> ::= palabra de mas de 2 caracteres y menos de 11
#def customer_function(){

#}

#------SIN TERMINAR------
#<number> ::= numero natural del 1 al 100


