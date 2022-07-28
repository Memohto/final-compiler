from mimetypes import init


class CodeGenerator:
  def __init__(self, root):
    self.root = root
    self.instructions = []
    self.var_num = 1
    self.block_num = 1

  def generate_code(self):
    for child in self.root.children:
      self.var_num = 1
      self.generate_node_code(child)
  
  def generate_node_code(self, current):
    ret = ''
    if current.type in ['float', 'int', 'boolean', 'id']:
      ret = str(current.val)
    elif current.type in ['floatdcl', 'intdcl', 'booldcl']:
      if current.val != '':
        self.instructions.append(current.type + ' ' + current.val)
      else:
        self.instructions.append(current.type + ' ' + current.children[0].children[0].val)
        self.generate_node_code(current.children[0])
    elif current.type == 'int2float':
        right = self.generate_node_code(current.children[0])
        ret = self.next_var()
        self.instructions.append(ret + ' = ' + current.type + ' ' + right)
    elif current.type == 'print':
        self.instructions.append('print ' + current.val)
    elif current.type == '=':
      right = self.generate_node_code(current.children[1])
      self.instructions.append(current.children[0].val + ' = ' + right) 
    elif current.type in ['+', '-', '*', '/', '^', '==', '!=', '>', '<', '>=', '<=', 'and', 'or']:
      left = self.generate_node_code(current.children[0])
      right = self.generate_node_code(current.children[1])
      ret = self.next_var()
      self.instructions.append(ret + ' = ' + left + ' ' + current.type + ' ' + right)
    elif current.type == 'if':
      condition = self.generate_node_code(current.children[0])
      if_block = self.next_block()
      continue_block = self.next_block()
      self.instructions.append('if '+ condition + ' goto ' + if_block)
      self.instructions.append('goto '+continue_block)
      self.instructions.append(if_block)
      for child in current.children[1].children:
        self.generate_node_code(child)
      self.instructions.append(continue_block)
    return ret

  def next_var(self):
    ret = 'r' + str(self.var_num)
    self.var_num += 1
    return ret

  def next_block(self):
    ret = 'L' + str(self.block_num)
    self.block_num += 1
    return ret