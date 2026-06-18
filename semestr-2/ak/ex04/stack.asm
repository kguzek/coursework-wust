.data
	prompt_input: .asciiz "Input number of strings (1-10): "
	newline: .asciiz "\n"
	buffer: .space 100

.text
main:
	li $v0, 4
	la $a0, prompt_input
	syscall
	li $v0, 5
	syscall
	move $t0, $v0
	move $s0, $sp
	li $t1, 0
	la $s1, buffer
loop:
	bge $t1, $t0, after_input

	li $v0, 8
	move $a0, $s1
	li $a1, 100
	syscall
	move  $s2, $s1

parse_loop:
	lb $t2, 0($s2)
	beq $t2, $zero, end_parse
	li $t3, 32 # 32 == ' '
	beq $t2, $t3, skip_ws
	li $t3, 10 # 10 == '\n'
	beq $t2, $t3, skip_ws
	li $t3, 9 # 9 == '\t'
	beq $t2, $t3, skip_ws
	move  $s3, $s2

word_loop:
	addi  $s2, $s2, 1
	lb $t2, 0($s2)
	beq   $t2, $zero, word_end
	li $t3, 32
	beq   $t2, $t3, word_end
	li $t3, 10
	beq   $t2, $t3, word_end
	li $t3, 9
	beq   $t2, $t3, word_end
	j word_loop

word_end:
	sub   $t4, $s2, $s3
	addi  $t5, $t4, 1	
	subu  $sp, $sp, $t5

	move  $t6, $sp
	move  $t7, $s3

copy_chars:
	beq $t4, $zero, copy_null
	lb $t2, 0($t7)
	sb $t2, 0($t6)
	addi $t4, $t4, -1
	addi $t7, $t7, 1
	addi $t6, $t6, 1
	j copy_chars

copy_null:
	sb $zero, 0($t6)
	j skip_ws

skip_ws:
	addi  $s2, $s2, 1
	j parse_loop

end_parse:
	addi  $t1, $t1, 1
	j loop

after_input:
print_loop:
	beq $sp, $s0, end

	move $a0, $sp
	li $v0, 4
	syscall

	li $v0, 4
	la $a0, newline
	syscall

	move $t7, $sp
	li $t9, 0

end_loop:
	lb $t2, 0($t7)
	beq  $t2, $zero, end_done
	addi $t9, $t9, 1
	addi $t7, $t7, 1
	j  end_loop

end_done:
	addi  $t9, $t9, 1
	addu  $sp, $sp, $t9 
	j  print_loop

end:
