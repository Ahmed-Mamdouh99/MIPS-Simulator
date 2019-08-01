from data.instruction_table import op_to_ascii


class Control:
  def __init__(self):
    self.hw = False
    self.jump = False
    self.reg_dst = False
    self.branch = False
    self.mem_read = False
    self.mem_to_reg = False
    self.alu_op = None
    self.mem_write = False
    self.alu_src = False
    self.reg_write = False

  def reset(self) -> None:
    self.jump = False
    self.reg_dst = False
    self.branch = False
    self.mem_read = False
    self.mem_to_reg = False
    self.alu_op = None
    self.mem_write = False
    self.alu_src = False
    self.reg_write = False

  @property
  def opcode(self) -> int:
    return self._opcode

  @opcode.setter
  def opcode(self, opcode: int) -> None:
    self.reset()
    op_info = op_to_ascii[opcode]
    op = op_info[0]
    if op in ('sll', 'srl'):
      # trigger shift signals
      self.reg_write = True
      self.shamt = True
    elif op == 'arith':
      # trigger r-type signals
      self.reg_dst = True
      self.reg_write = True
    elif op == 'addi':
      # trigger i-type signals
      self.reg_write = True
      self.alu_src = True
    elif op in ('lw', 'lh'):
      # trigger memory access signals
      if op == 'lh':
        self.hw = True
      self.mem_read = True
      self.mem_to_reg = True
      self.reg_write = True
      self.alu_src = True
    elif op in ('sw', 'sh'):
      # trigger memory access signals
      if op == 'sh':
        self.hw = True
      self.mem_write = True
      self.alu_src = True
    elif op == 'beq':
      # trigger branch signals
      self.branch = True
    elif op == 'j':
      # trigger jump signals
      self.jump = True
    self.alu_op = op
