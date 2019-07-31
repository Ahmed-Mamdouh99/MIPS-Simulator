import numpy as np


class RegisterFile:
  def __init__(self):
    self.registers = np.zeros(32, dtype='int32')
    self.read_data_1 = None
    self.read_data_2 = None

  def write_back(self, r1: int, r2: int, dst_flag: bool, res1: int, res2: int,
                 res_flag: bool, write_flag: bool) -> None:
    """ Write back result to a register
    :param r1: int
        rt register data
    :param r2: int
        rd register data
    :param dst_flag: bool
        regDst signal from control
    :param res1: int
        result from alu
    :param res2:
    result from data memory
    :param res_flag:
        memToReg signal from control
    :param write_flag: bool
        regWrite signal from control
    :return: None
    """
    dst = r1
    if dst_flag:
      dst = r2
    res = res1
    if res_flag:
      res = res2
    if write_flag:
      if dst == 0:
        raise RuntimeError('Cannot change the value of register $0')
      self.registers[dst] = res

  def read(self, rs: int, rt: int) -> None:
    """ Read data from register file
    :param rs: int
      rs register number
    :param rt: int
      rt register number
    :return: None
    """
    self.read_data_1 = self.registers[rs]
    self.read_data_2 = self.registers[rt]
