import io
import os
import sys
import numpy as np
from blocks.register_file import RegisterFile
from blocks.control import Control
from blocks.alu import ALU
from blocks.data_memory import DataMemory


def b2d(n, w=5):
  value = 0
  if n[0] == '0':
    return int(n, 2)
  else:
    return  - ((int(n[1:], 2) - 1) ^ ((1 << w - 1) - 1 ))


class Instruction:
  """This class is a wrapper of the deconstructed instruction"""
  def __init__(self, opcode: int = 0, rd: int = 0, rt: int = 0,
               rs: int = 0, shamt: int = 0, funct: int = 0,
               sign_extend: int = 0) -> None:
    self.opcode = opcode
    self.rd = rd
    self.rt = rt
    self.rs = rs
    self.shamt = shamt
    self.funct = funct
    self.sign_extend = sign_extend
  
  def __str__(self) -> str:
    return '{:06b} {:05b} {:05b} {:05b} {:05b} {:06b}'.format(self.opcode,\
        self.rd, self.rt, self.sign_extend)


class Processor:
  """ This class simulates the mips processor, it contains a high level view of how the processor works"""
  def __init__(self, memory_size: int = 2**16, cli: bool = False) -> None:
    # debugging variables
    self.done = False
    self.cli = cli
    self._output_stream = sys.stdout
    # Initializing clock
    self.clk = 0
    # Initializing memory
    self.memory = [0 for _ in range(memory_size)]
    # Initializing program counter
    self.pc = 0
    # Initializing instruction memory
    self.instruction_memory = []
    # Initializing raw instruction string
    self.raw_instr = ''
    # Initializing instruction parts
    self.inst = Instruction()
    # Initializing cpu blocks
    self.reg_file = RegisterFile()
    self.control = Control()
    self.alu = ALU()
    self.memory = DataMemory(memory_size)
  
  @property
  def output_stream(self) -> io.TextIOWrapper:
    return self._output_stream
  
  @output_stream.setter
  def output_stream(self, output_stream: io.TextIOWrapper) -> None:
    assert isinstance(output_stream, io.TextIOWrapper), \
        'output_stream property has to be of type io.TextIOWrapper'
    self._output_stream = output_stream
  
  def write(self, line: str) -> None:
    """ prints a string to the output stream assigned to the class instance
    :param: line: str
      line to be printed
    :return: None
    """
    self.output_stream.write(line)
    self.output_stream.write('\n')

  def load_instructions(self, in_stream: io.TextIOWrapper = sys.stdin) -> None:
    """ Loading instructions from an input stream
    :param in_stream: io.TextIOWrapper
      input steam
    :return: None
    """
    assert isinstance(in_stream, io.TextIOWrapper), \
      'Parameter type error: in_stream {}'.format(type(in_stream))
    self.instruction_memory.clear()
    for line in in_stream.readlines():
      # Sanitizing input
      line = line.split('#')[0].strip().replace(' ', '')
      if len(line) != 32:
        continue
      self.instruction_memory.append(line)

  def fetch(self) -> None:
    """f etching the instruction from the instructions memory
    :return: None
    """
    self.raw_instr = self.instruction_memory[self.pc // 4]

  def decode(self) -> None:
    """ Decoding the instruction after fetching
    :return: None
    """
    # Asserting the instruction data type
    assert isinstance(self.raw_instr, str), 'instruction has to be a string'
    # Decoding the instruction
    opcode = int(self.raw_instr[:6], 2)
    rs = int(self.raw_instr[6:11], 2)
    rt = int(self.raw_instr[11:16], 2)
    rd = int(self.raw_instr[16:21], 2)
    shamt = b2d(self.raw_instr[21:26])
    funct = int(self.raw_instr[26:], 2)
    sign_extend = b2d(self.raw_instr[16:], 16)
    self.inst = Instruction(opcode, rd, rt, rs, shamt, funct, sign_extend)

  def update_control(self) -> None:
    """ Updating control signals by passing the opcode to the control unit
    :return: None
    """
    self.control.opcode = self.inst.opcode

  def read_registers(self) -> None:
    """ Reading registers from the register file
    :return: None
    """
    self.reg_file.read(self.inst.rs, self.inst.rt)

  def execute(self) -> None:
    """ Executing the instruction in the ALU
    :return: None
    """
    op1 = self.reg_file.read_data_1
    op2 = self.reg_file.read_data_2
    if self.control.alu_src:
      op2 = self.inst.sign_extend
    self.alu.execute(self.inst.funct, self.control.alu_op, op1, op2)

  def access_memory(self) -> None:
    """ Accessing memory using the results from the ALU, registers and control signals
    :return: None
    """
    self.memory.run(self.alu.result, self.reg_file.read_data_2,
                    self.control.mem_write, self.control.mem_read,
                    self.control.hw)

  def write_back(self) -> None:
    """ Writing the result back to the registers
    :return: None
    """
    self.reg_file.write_back(self.inst.rt, self.inst.rd, self.control.reg_dst,
                             self.alu.result, self.memory.read_data,
                             self.control.mem_to_reg, self.control.reg_write)

  def print_changes(self) -> None:
    """Print the details of the instruction execution
    :return: None
    """
    if self.cli:
      sep = lambda: self.write('-'*30)
      make_str = lambda x, n: ''.join(str(x)[i] if i < len(str(x))\
         else ' ' for i in range(n))
      print_row = lambda a, b: self.write('| {}| {}|'.format(make_str(a, 15), make_str(b, 10)))
      self.write('Instruction number {} | {}'.format(self.pc//4,\
          self.raw_instr))
      sep()
      print_row('Register Number', 'Data')
      for i in range(len(self.reg_file.registers)):
        print_row(i, self.reg_file.registers[i])
      sep()
      sep()
      self.write('Control signals')

      sep()
      for key, value in self.control.__dict__.items():
        print_row(key, value)
      sep()
      sep()
      self.write('Memory')
      sep()
      print_row('Address', self.memory.address)
      print_row('Read Data', self.memory.read_data)
      print_row('Write Data', self.memory.write_data)
      sep()
      sep()
      self.write('PC: {}'.format(self.pc))
      sep()
      sep()
      sep()

  def fix_pc(self) -> None:
    """ Fixing the program counter's place by checking for the jump and branch control signals and then adding 4
    :return: None
    """
    self.pc += 4
    if (self.control.branch and self.alu.zero) or self.control.jump:
      self.pc += (self.inst.sign_extend << 2)
  
  def check_done(self) -> None:
    """ Check if the program counter reached the end of the instruction memory
    :return: None
    """
    if self.pc // 4 >= len(self.instruction_memory):
      self.done = True

  def run_instruction(self) -> None:
    """ Simulating of an instruction running
    :return: None
    """
    self.fetch()           # Fetching instruction
    self.decode()          # Decoding instruction
    self.update_control()  # Updating control
    self.read_registers()  # Accessing register file
    self.execute()         # Executing the instruction in the alu
    self.access_memory()   # Accessing memory
    self.write_back()      # Write back
    self.print_changes()   # Printing details of the instruction execution
    self.fix_pc()          # Fix program counter
    self.check_done()      # Checking if the program counter is out of range


if __name__ == '__main__':
  cli = '-v' in sys.argv
  cpu = Processor(cli=cli)
  with open(sys.argv[1], 'r') as instruction_file:
    cpu.load_instructions(instruction_file)
    while True:
      cpu.run_instruction()
      os.system('pause')
      if cpu.done:
        print('Done executing!')
        break
  print(cpu.pc)
