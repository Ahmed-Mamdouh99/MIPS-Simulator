ascii_to_bin = {
  # symbol: instruction type, opcode, funct
  'add': ('R', 0x00, 0x20),
  'sub': ('R', 0x00, 0x22),
  'and': ('R', 0x00, 0x24),
  'or': ('R', 0x00, 0x25),

  'addi': ('I', 0x08, 0x00),
  'lw': ('I', 0x23, 0x00),
  'lh': ('I', 0x21, 0x00),
  'sw': ('I', 0x2B, 0x00),
  'sh': ('I', 0x29, 0x00),

  'sll': ('R', 0x00, 0x00),
  'srl': ('R', 0x00, 0x02),

  'j': ('J', 0x02, 0x00),
  'beq': ('I', 0x04, 0x00),

  'nop': ('I', 0x05, 0x00),

  # 'addiu':  ('I', 0x09, 0x00),
  # 'addu':   ('R', 0x00, 0x21),
  # 'andi':   ('I', 0x0C, 0x00),
  # 'blez':   ('I', 0x06, 0x00),
  # 'bne':    ('I', 0x05, 0x00),
  # 'bgtz':   ('I', 0x07, 0x00),
  # 'div':    ('R', 0x00, 0x1A),
  # 'divu':   ('R', 0x00, 0x1B),
  # 'jal':    ('J', 0x03, 0x00),
  # 'jr':     ('R', 0x00, 0x08),
  # 'lb':     ('I', 0x20, 0x00),
  # 'lbu':    ('I', 0x24, 0x00),
  # 'lhu':    ('I', 0x25, 0x00),
  # 'lui':    ('I', 0x0F, 0x00),
  # 'mfhi':   ('R', 0x00, 0x10),
  # 'mthi':   ('R', 0x00, 0x11),
  # 'mflo':   ('R', 0x00, 0x12),
  # 'mtlo':   ('R', 0x00, 0x13),
  # 'mfc0':   ('R', 0x10, 0x00),
  # 'mult':   ('R', 0x00, 0x18),
  # 'multu':  ('R', 0x00, 0x19),
  # 'nor':    ('R', 0x00, 0x27),
  # 'xor':    ('R', 0x00, 0x26),
  # 'ori':    ('I', 0x0D, 0x00),
  # 'sb':     ('I', 0x28, 0x00),
  # 'sh':     ('I', 0x29, 0x00),
  # 'slt':    ('R', 0x00, 0x2A),
  # 'slti':   ('I', 0x0A, 0x00),
  # 'sltiu':  ('I', 0x0B, 0x00),
  # 'sltu':   ('R', 0x00, 0x2B),
  # 'sra':    ('R', 0x00, 0x03),
  # 'subu':   ('R', 0x00, 0x23),
}

op_to_ascii = dict()
for key, val in ascii_to_bin.items():
  op_to_ascii[val[1]] = (key, val[0], val[2])
op_to_ascii[0] = ('arith', op_to_ascii[0][1], None)


funct_to_ascii = dict()
for key, val in ascii_to_bin.items():
  funct_to_ascii[val[2]] = (key, val[0], val[1])
funct_to_ascii[0] = ('sll', ascii_to_bin['sll'][0], ascii_to_bin['sll'][1])