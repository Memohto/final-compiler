class Node:
  def __init__(self, token = '', val = ''):
    self.token = token
    self.val = val
    self.children = []

  def __str__(self, level = 0):
    ret = "\t"*level+(self.token + ': ' + str(self.val))+"\n"
    for child in self.children:
      ret += child.__str__(level+1)
    return ret