import sys
sys.path.insert(0, "../..")

keywords = (
  'FLOAT', 'INT', 'BOOLEAN', 'PRINT', 'AND', 'OR', 'TRUE', 'FALSE', 'IF'
)

tokens = keywords + (
  'FNUMBER', 'INUMBER', 'NAME', 'EQUALS', 'NOT_EQUALS', 'GREATER', 'LESS', 'GREAT_EQUALS', 'LESS_EQUALS'
)

literals = ['+', '-', '*', '/', '^', ';', '=', '(', ')', '{', '}']

# Tokens
def t_NAME(t):
  r'[a-zA-Z_][a-zA-Z0-9_]*'
  if t.value.upper() in keywords:
    t.type = t.value.upper()
  return t

def t_FNUMBER(t):
  r'\d+\.\d+'
  t.value = float(t.value)
  return t

def t_INUMBER(t):
  r'\d+'
  t.value = int(t.value)
  return t

t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_GREATER = r'>'
t_LESS = r'<'
t_GREAT_EQUALS = r'>='
t_LESS_EQUALS = r'<='

t_ignore = " \t"

def t_newline(t):
  r'\n+'
  t.lexer.lineno += t.value.count("\n")

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

from Node import Node

# Symbol table
names = { }

def p_program(p):
  '''program : blocks'''
  root = Node("PROG")
  root.children += p[1]
  p[0] = root

def p_blocks(p):
  '''blocks : block blocks
            | '''
  if len(p) > 1:
    p[0] = p[1] + p[2]
  else:
    p[0] = []

def p_block(p):
  '''block : declarations statements'''
  p[0] = p[1] + p[2]

def p_declarations(p):
  '''declarations : declaration ";" declarations
                  | '''
  if len(p) > 1:
    p[0] = p[1] + p[3]
  else:
    p[0] = []

def p_declaration(p):
  '''declaration : FLOAT NAME
                 | INT NAME
                 | BOOLEAN NAME'''
  dcl_type = ''
  if p[1] == 'float':
    dcl_type = 'floatdcl'
  elif p[1] == 'int':
    dcl_type = 'intdcl'
  elif p[1] == 'boolean':
    dcl_type = 'booldcl'
  p[0] = [Node(dcl_type, p[2])]

def p_declaration_assign(p):
  '''declaration : FLOAT NAME "=" number_expression
                 | INT NAME "=" number_expression
                 | BOOLEAN NAME "=" boolean_expression'''
  parent = Node("=")
  parent.children.append(Node('id', p[2]))
  parent.children.append(p[4])
  p[0] = [parent]

def p_statements(p):
  '''statements : statement statements
                | '''
  if len(p) > 1:
    p[0] = p[1] + p[2]
  else:
    p[0] = []

def p_statement_if(p):
  'statement : IF "(" boolean_expression ")" "{" blocks "}"'
  parent = Node("if")
  parent.children.append(p[3])
  child = Node("block")
  child.children += p[6]
  parent.children.append(child)
  p[0] = [parent]

def p_statement_assign(p):
  '''statement : NAME "=" number_expression ";"
               | NAME "=" boolean_expression ";"'''
  parent = Node("=")
  parent.children.append(Node('id', p[1]))
  parent.children.append(p[3])
  p[0] = [parent]

def p_statement_print(p):
  'statement : PRINT "(" NAME ")" ";"'
  p[0] = [Node('print', p[3])]

def p_number_expression(p):
  '''number_expression : "(" number_expression ")"
                       | number_expression "+" number_expression 
                       | number_expression "-" number_expression 
                       | number_expression "*" number_expression 
                       | number_expression "/" number_expression 
                       | number_expression "^" number_expression
                       | NAME
                       | float_value
                       | int_value'''
  if len(p) > 2:
    if p[2] in ['+', '-', '*', '/', '^']:
      parent = Node(p[2])
      parent.children.append(p[1])
      parent.children.append(p[3])
      p[0] = parent
    else:
      p[0] = p[2]
  else:
    if type(p[1]) == str:
      p[0] = Node("id", p[1])
    else:
      p[0] = p[1]

def p_float_value(p):
  '''float_value : FNUMBER'''
  p[0] = Node('float', p[1])

def p_int_value(p):
  '''int_value : INUMBER'''
  p[0] = Node('int', p[1])

def p_boolean_expression(p):
  '''boolean_expression : "(" boolean_expression ")"
                        | boolean_expression AND boolean_expression
                        | boolean_expression OR boolean_expression
                        | boolean_value
                        | comparison'''
  if len(p) > 2:
    if p[2] in ['and', 'or']:
      parent = Node(p[2])
      parent.children.append(p[1])
      parent.children.append(p[3])
      p[0] = parent
    else:
      p[0] = p[2]
  else:
    p[0] = p[1]
  
def p_boolean_value(p):
  '''boolean_value : NAME
                   | TRUE
                   | FALSE'''
  type = ''
  if p[1] in ['true', 'false']:
    type = 'bool'
  else:
    type = 'id'
  p[0] = Node(type, p[1])

def p_comparison(p):
  '''comparison : number_expression EQUALS number_expression
                | number_expression NOT_EQUALS number_expression
                | number_expression GREATER number_expression
                | number_expression LESS number_expression
                | number_expression GREAT_EQUALS number_expression
                | number_expression LESS_EQUALS number_expression'''
  parent = Node(p[2])
  parent.children.append(p[1])
  parent.children.append(p[3])
  p[0] = parent
                
def p_error(p):
  if p:
    print("Syntax error at '%s'" % p.value)
  else:
    print("Syntax error at EOF")

# Semantic analysis
def type_check(root):
  print(root)

# Build the yacc
import ply.yacc as yacc
parser = yacc.yacc()

if len(sys.argv) == 2:
  f = open(sys.argv[1], "r")

  tree = yacc.parse(f.read())
  # print(tree)
  type_check(tree)

  f.close()
else:
  print('Missing arguments (./gtc.py input_path.txt)')