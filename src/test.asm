addi $t7, $t0, 1
add $t0, $0, $0          # Initialize loop counter
add $t1, $0, $0          # Initialize positive accumulator
add $t2, $0, $0          # Initialize negative accumulator
addi $t3, $0, 1          # Initialize rl-shift accumulator
addi $t4, $0, 1          # Initialize ll-shift accumulator
# Saving all initial working register content to memory
  sw $t1, 0($t0)
  sw $t1, 4($t0)
  sw $t1, 8($t0)
  sw $t1, 12($t0)
loop_begin:              # Begin loop
  beq $t0, $t7, exit     # Exiting the loop if the counter reaches 1
  
  add $t5, $0, $0        # Initialize memory address

  # Loading values from memory
  lw $t1, 0($t5)
  lw $t1, 4($t5)
  lw $t1, 8($t5)
  lw $t1, 12($t5)
  
  addi $t0, $t0, 1       # Incrementing the counter
  add $t1, $t1, $t0      # Adding the counter to the positive accum
  sub $t2, $t2, $t0      # Subbing the counter from the negative accum
  srl $t3, $t3, 1        # Shifting right by 1
  sll $t4, $t4, 1        # Shifting left by 1

  # Saving all working register content to memory
  sw $t1, 0($t5)
  sw $t1, 4($t5)
  sw $t1, 8($t5)
  sw $t1, 12($t5)
  # Adding nop
  nop
  j loop_begin           # Looping

exit:
  # Saving half words
  sh $t1, 0($t0)
  sh $t1, 2($t0)
  sh $t1, 4($t0)
  sh $t1, 6($t0)

  # Loading half words
  lh $t1, 0($t0)
  lh $t1, 2($t0)
  lh $t1, 4($t0)
  lh $t1, 6($t0)

  and $t5, $t1, $t2     # And operation
  or $t6, $t1, $t2      # Or operation
