from mips import Processor
import sys
from assembler import assemble


if __name__ == '__main__':
  # Check if an assembly flag was supplied
  if '-a' in sys.argv:
    # Assembling job
    # Detect flags
    input_file_name = 'input.asm'
    output_file_name = 'input.b'
    if '-i' in sys.argv:
      input_file_name = sys.argv[sys.argv.index('-i')+1]
    if '-o' in sys.argv:
      output_file_name = sys.argv[sys.argv.index('-o')+1]
    input_file = open(input_file_name, 'r')
    output_file = open(output_file_name, 'w')
    # Run assembly function
    assemble(input_file, output_file)
  else:
    # Run MIPS simulation
    cpu = Processor(cli=True)
    input_file_name = 'input.b'
    output_file_name = 'sim_output.txt'
    # Check for flags
    if '-i' in sys.argv:
      input_file_name = sys.argv[sys.argv.index('-i')+1]
    if '-o' in sys.argv:
      output_file_name = sys.argv[sys.argv.index('-o')+1]
    input_file = open(input_file_name, 'r')
    output_file = open(output_file_name, 'w')
    # Set IO streams for the simulation
    cpu.load_instructions(input_file)
    cpu.output_stream = output_file
    # Running simulation
    while not cpu.done:
      cpu.run_instruction()
