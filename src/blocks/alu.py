from data.instruction_table import funct_to_ascii


class ALU:
  def __init__(self):
    self.result = 0
    self.zero = 0

  def execute(self, funct: int, alu_op: str, op1: int, op2: int) -> None:
    control = alu_op
    if alu_op == 'arith':
      control = funct_to_ascii[funct][0]
    if control in ('add', 'addi', 'lw', 'lh', 'sw', 'sh'):
      self.result = op1 + op2
    elif control in ('sub', 'beq'):
      self.result = op1 - op2
    elif control == 'sll':
      self.result = op1 << op2
    elif control == 'slr':
      self.result = op1 >> op2
    elif control == 'or':
      self.result = op1 | op2
    elif control == 'and':
      self.result = op1 & op2
    self.zero = self.result == 0