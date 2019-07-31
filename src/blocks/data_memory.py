import numpy as np


__WORD_MASK__ = 0b1111


class DataMemory:
  """This class simulates the processor memory with 2^32 byte addressable cells of size 8 bits"""
  def __init__(self, size=2 ** 16):
    self.read_data = 0
    self.mem = np.zeros(size, dtype='uint8')
    self.address = 0
    self.write_data = 0

  def run(self, address: int, write_data: int, mem_write: bool,
          mem_read: bool, hw: bool) -> None:
    """ Run the read/write process in the memory
    :param address: int
      Read/Write address
    :param write_data: int
      data to be written to the memory
    :param mem_write: bool
      memWrite control signal
    :param mem_read: bool
      memRead control signal
    :param hw: bool
      loadHw control signal
    :return: None
    """
    # Clear output
    self.read_data = 0
    self.write_data = 0
    # Read from memory
    if mem_read:
      self.address = address
      if hw:
        self.read_data = self.mem[address] << 8 + self.mem[address + 1]
      else:
        self.read_data = (self.mem[address] << 24) \
                         + (self.mem[address + 1] << 16) + \
                         (self.mem[address + 2] << 8) + self.mem[address + 3]
    # Write to memory
    if mem_write:
      self.address = address
      self.write_data = write_data
      if hw:
        self.mem[address] = (write_data >> 8) & __WORD_MASK__
        self.mem[address + 1] = write_data & __WORD_MASK__
      else:
        self.mem[address + 3] = write_data & __WORD_MASK__
        self.mem[address + 2] = (write_data >> 8) & __WORD_MASK__
        self.mem[address + 1] = (write_data >> 16) & __WORD_MASK__
        self.mem[address] = (write_data >> 24) & __WORD_MASK__
