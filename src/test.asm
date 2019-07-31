addi $t1, $v0, 3
add $t0, $0, $0          # Initialize loop counter
add $v0, $0, $0          # Initializing accumulating counter
loop_begin:
  addi $t0, $t0, 1       # incrementing the counter
  add $v0, $v0, $t0      # Adding the counter to the accumulating counter
  beq $t0, $t1, exit       # Exiting the loop if the counter reaches 3 
  j loop_begin           # Looping
exit: