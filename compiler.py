from ast import keyword
import sys
sys.path.insert(0, "../..")

keywords = (
  'FLOAT', 'INT', 'BOOLEAN', 'PRINT', 'AND', 'OR', 'TRUE', 'FALSE'
)

tokens = keywords + (
  'FNUMBER', 'INUMBER', 'NAME'
)

literals = ['+', '-', '*', '/', '^', ';', '=', '(', ')']

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
  '''program : declarations statements
             | '''
  root = Node("PROG")
  if len(p) > 1:
    root.children += p[1] + p[2]
  p[0] = root

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
  '''statements : statement ";" statements
                | '''
  if len(p) > 1:
    p[0] = p[1] + p[3]
  else:
    p[0] = []

def p_statement_assign(p):
  'statement : NAME "=" number_expression'
  parent = Node("=")
  parent.children.append(Node('id', p[1]))
  parent.children.append(p[3])
  p[0] = [parent]

def p_statement_print(p):
  'statement : PRINT NAME'
  p[0] = [Node('print', p[2])]

def p_number_expression(p):
  '''number_expression : "(" number_expression ")"
                       | number_expression "+" number_expression 
                       | number_expression "-" number_expression 
                       | number_expression "*" number_expression 
                       | number_expression "/" number_expression 
                       | number_expression "^" number_expression
                       | number_value'''
  if len(p) > 2:
    if p[2] in ['+', '-', '*', '/', '^']:
      parent = Node(p[2])
      parent.children.append(p[1])
      parent.children.append(p[3])
      p[0] = parent
    else:
      p[0] = p[2]
  else:
    p[0] = p[1]

def p_number_value_id(p):
  'number_value : NAME'
  p[0] = Node('id', p[1])

def p_number_value_float(p):
  'number_value : FNUMBER'
  p[0] = Node('fnum', p[1])           

def p_number_value_int(p):
  'number_value : INUMBER'
  p[0] = Node('inum', p[1])

def p_boolean_expression(p):
  '''boolean_expression : "(" boolean_expression ")"
                        | boolean_expression AND boolean_expression
                        | boolean_expression OR boolean_expression
                        | boolean_value'''
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
    type = ''
  else:
    type = 'id'
  p[0] = Node(type, p[1])

def p_error(p):
  if p:
    print("Syntax error at '%s'" % p.value)
  else:
    print("Syntax error at EOF")

# Build the yacc
import ply.yacc as yacc
parser = yacc.yacc()

f = open("input.txt", "r")

tree = yacc.parse(f.read())
# print(tree.token + ': ' + str(tree.val))
# print(tree.children[0].token + ': ' + str(tree.children[0].val))
# print(tree.children[0].children[1].token + ': ' + str(tree.children[0].children[1].val))
print(tree)

f.close()
  