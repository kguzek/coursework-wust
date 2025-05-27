.data
	prompt_input: .asciiz "Input number of strings... "
	input_buffer: .space 199
	input_size: .byte 200
.text
main:
	li $v0, 4
	la $a0, prompt_input
	syscall
	li $v0, 5
	syscall
	move $t0, $v0
loop:
	beqz $t0, loop_end
	li $v0, 8
	la $a0, input_buffer
	la $a1, input_size
	syscall
	sub $t0, $t0, 1
	j loop
loop_end:
