import io
import math
import sys
from data.instruction_table import ascii_to_bin as instruction_table
from data.register_table import register_table


__INSTR_MASK__ = '{:06b}{:05b}{:05b}{:05b}{:05b}{:06b}'
def d2b(A: int, w: int=5) -> int:
  if A < 0:
    res = (- A ^ ((1 << w) - 1)) + 1
    res = '{:b}'.format(res)
    print('{} | {} | {} | {}'.format(A, w, res, len(res)))
    return res
  else:
    padding = '0'*(w - 1 - int(math.log(A, 2)))
    res = '{}{:b}'.format(padding, A)
    print('{} | {} | {} | {}'.format(A, w, res, len(res)))
    return res


def asm_to_bin(instr: str, instr_count: int, labels: dict) -> (int, [str]):
  # Initialize outputs
  instr_out = []
  # Sanitizing input
  instr = instr.strip()
  cmd = instr.split(' ')[0]
  cmd_info = instruction_table[cmd]
  if cmd in ('beq', 'j'):
    # Creating the branch/jump instruction
    label = instr.split(' ')[-1]
    label_bin = labels[label] - (instr_count+2)
    if cmd == 'beq':
      # Get register
      registers = [register_table[x] for x in instr[instr.index(' '):].replace(' ','').split(',')[:-1]]
      assert len(registers) == 2, 'R-type instruction {} should have 2 registers'.format(cmd)
      bin_instr = '{:06b}{:05b}{:05b}{}'.format(cmd_info[1], registers[0], registers[1], d2b(label_bin, 16))
      instr_out.append(bin_instr)
      instr_count += 1
    else:
      bin_instr = '{:06b}{:05b}{:05b}{}'.format(cmd_info[1], 0, 0, d2b(label_bin, 16))
      instr_out.append(bin_instr)
      instr_count += 1
  elif cmd in ('sll', 'srl'):
    # Assembling with a shift instrucion
    # Getting the registers from the instructions
    registers = instr[instr.index(' '):].replace(' ','').split(',')[:-1]
    shamt = instr.split(' ')[1].replace(' ','').split(',')[-1]
    assert len(registers) == 2, 'R-type instruction {} should have 2 registers'.format(cmd)
    # Creating binary instruction
    bin_cmd = __INSTR_MASK__.format( cmd_info[1], 0, \
      register_table[registers[1]], 0, register_table[registers[0]],\
        d2b(shamt) , cmd_info[2]\
    )
    # Adding the command to the output list
    instr_out.append(bin_cmd)
    instr_count += 1
  elif cmd_info[0] == 'R':
    # R type command
    # Getting the registers from the instructions
    registers = instr[instr.index(' '):].replace(' ','').split(',')
    assert len(registers) == 3, 'R-type instruction {} should have 3 registers'.format(cmd)
    # Creating binary instruction
    bin_cmd = __INSTR_MASK__.format( cmd_info[1], \
      register_table[registers[2]], register_table[registers[1]], \
      register_table[registers[0]], 0, cmd_info[2]\
    )
    # Adding the command to the output list
    instr_out.append(bin_cmd)
    instr_count += 1
  elif cmd_info[0] == 'I':
    # Create I-type instruction
    # Getting the registers from the instructions
    registers = instr[instr.index(' '):].replace(' ','').split(',')[:-1]
    assert len(registers) == 2, 'I-type instruction {} should have 2 registers'.format(cmd)
    imm = int(instr[instr.index(' '):].replace(' ','').split(',')[-1])
    bin_cmd = '{:06b}{:05b}{:05b}{}'.format(cmd_info[1], \
      register_table[registers[1]], register_table[registers[0]], d2b(imm, 16))
    instr_out.append(bin_cmd)
  instr_out[-1] += '  # {}'.format(instr)
  return instr_count, instr_out


def assemble(input_stream: io.TextIOWrapper, 
             output_stream: io.TextIOWrapper) -> None:
  # Initializing label dictionary
  labels = dict()
  # Initializing instruction number
  instr_count = 0
  # Initializing binary instruction
  asm = []
  # First pass to detect labels
  for line in input_stream.readlines():
    # Sanitize the line
    line = line.split('#')[0].strip()
    # Skip empty lines
    if len(line) == 0:
      continue
    # Checking for labels
    line = line.split(':')
    if len(line) == 1:
          instr_count += 1
    elif len(line) == 2:
      labels[line[0]] = instr_count-1
      if len(line[1]) > 0:
            instr_count += 1
  # Resetting instruction count
  instr_count = 0
  # Second pass to assemble the code
  input_stream.seek(0, 0)
  for line in input_stream.readlines():
    # Sanitize the line
    line = line.split('#')[0].strip()
    # Skip empty lines
    if len(line) == 0:
      continue
    # Checking for labels
    line = line.split(':')
    # Check if there is no label
    if len(line) == 1:
      instr_count, asm = asm_to_bin(line[0], instr_count, labels)
    # Check if a label exists
    elif len(line) == 2:
      # Check if the line has an instruction
      if len(line[1]) > 0:
        instr_count, asm = asm_to_bin(line[1], instr_count, labels)
      else:
        continue
    # Writing to output stream
    for bin_instr in asm:
      output_stream.write(bin_instr+'\n')


if __name__ == '__main__':
  input_name = 'input.asm'
  output_name = 'output'
  # Check if an input file name is supplied
  if '-i' in sys.argv:
    input_name = sys.argv[sys.argv.index('-i')+1]
  # Check if an output file name is supplied
  if '-o' in sys.argv:
    output_name = sys.argv[sys.argv.index('-o')+1]
  # Read input file
  input_stream = open(input_name, 'r')
  # Read output file
  output_stream = open(output_name, 'w')
  assemble(input_stream, output_stream)

int(23).bit_length
