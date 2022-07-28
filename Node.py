import copy

class Node:
  def __init__(self, type = '', val = '', data_type = ''):
    self.type = type
    self.val = val
    self.data_type = data_type
    self.children = []

  def type_check(self, symbol_table):
    for child in self.children:
      child.type_check(symbol_table)
    if self.type == 'id':
      if self.val in symbol_table:
        self.data_type = symbol_table[self.val]
      else:
        self.error(self.val + "not declared")
    elif self.type in ['float', 'int', 'boolean']:
      self.data_type = self.type
    elif self.type in ['+', '-', '*', '/', '^']:
      self.data_type = self.consistent(self.children[0], self.children[1])
    elif self.type in ['==', '!=', '>', '<', '>=', '<=']:
      self.data_type = self.comparison(self.children[0], self.children[1])
    elif self.type == '=':
      self.data_type = self.convert(self.children[1], self.children[0].data_type)

  def comparison(self, node_1, node_2):
    if node_1.data_type == 'boolean' or node_2.data_type == 'boolean':
      self.error("Parsing error: Can only compare numbers")
    return 'boolean'

  def generalize(self, type_1, type_2):
    type = ""
    if type_1 == 'float'  or type_2 == 'float':
      type = 'float'
    else:
      type = 'int'
    return type

  def consistent(self, node_1, node_2):
    type = self.generalize(node_1.data_type, node_2.data_type)
    self.convert(node_1, type)
    self.convert(node_2, type)
    return type

  def convert(self, node, type):
    if node.data_type == 'int' and type == 'float':
      temp_node = copy.deepcopy(node)
      node.type = "int2float"
      node.val = ""
      node.data_type = "float"
      node.children = [temp_node]
      return 'float'
    elif node.data_type == 'float' and type == 'int':
      self.error("Parsing error")
    elif node.data_type == 'boolean' and type == 'int':
      self.error("Parsing error")
    elif node.data_type == 'boolean' and type == 'float':
      self.error("Parsing error: Cannot convert " + node.data_type + " to " + type)
    return type
  
  def error(self, message):
    print(message)
    exit()

  def __str__(self, level = 0):
    ret = "   " * level+(self.type + ' : ' + str(self.val)) + ' ' + (self.data_type)+"\n"
    for child in self.children:
      ret += child.__str__(level+1)
    return ret