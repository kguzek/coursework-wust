.data
	input_operation: .asciiz "Input operation (0 decode, 1 encode): "
	input_source: .asciiz "Input the source text: "
	input_offset: .asciiz "Input the shift offset: "
	invalid_operation: .asciiz "Invalid operation: "
	invalid_input_a: .asciiz "Invalid character ('"
	invalid_input_b: .asciiz "') at position "
	invalid_input_c: .asciiz ": not an uppercase character A-Z\n"

	newline: .asciiz "\n"
	
	source_text: .space 17
	source_size: .word 16
.text
main:
	# prompt for operator
	li $v0, 4
	la $a0, input_operation
	syscall
	li $v0, 5
	syscall
	move $t0, $v0
	# prompt for shift offset
	li $v0, 4
	la $a0, input_offset
	syscall
	li $v0, 5
	syscall
	move $t1, $v0
	# prompt for input value
	li $v0, 4
	la $a0, input_source
	syscall
	li $v0, 8
	la $a0, source_text
	lw $a1, source_size
	syscall
	# apply operation
	beq $t0, 0, decode
	beq $t0, 1, encode
	j error_operator
decode:
	sub $t1, $zero, $t1
	j shift
encode:
	j shift
shift:
	li $t3, 0
	lw $t4, source_size
	loop:
		beq $t3, $t4, loop_end

		lb $t5, source_text($t3)
		# break if at end of string
		beq $t5, 10, loop_end
		beq $t5, '\0', loop_end_print_newline
		# comment this line if you want to disallow whitespaces
		beq $t5, ' ', continue
		bgtu $t5, 'z', error_input
		bltu $t5, 'A', error_input
		bgtu $t5, 'Z', convert_lowercase
		j converted
		convert_lowercase: 
			bltu $t5, 'a', error_input
			sub $t5, $t5, 32
		converted:
		add $t5, $t5, $t1
		bgtu $t5, 'Z', overflow_upper
		bltu $t5, 'A', overflow_lower
		j mut
		overflow_upper:
			sub $t5, $t5, 26
			j mut
		overflow_lower:
			add $t5, $t5, 26
			j mut
		mut:
			# mutate the input text
			sb $t5, source_text($t3)
		continue:
		add $t3, $t3, 1
		j loop
	loop_end_print_newline:
	li $v0, 4
	la $a0, newline
	syscall
	loop_end:
	li $v0, 4
	la $a0, source_text
	syscall
	j end
error_operator:
	li $v0, 4
	la $a0, invalid_operation
	syscall
	li $v0, 1
	move $a0, $t0
	syscall
	li $v0, 4
	la $a0, newline
	syscall
	j end
error_input:
	li $v0, 4
	la $a0, invalid_input_a
	syscall
	li $v0, 11
	move $a0, $t5
	syscall
	li $v0, 4
	la $a0, invalid_input_b
	syscall
	li $v0, 1
	move $a0, $t3
	syscall
	li $v0, 4
	la $a0, invalid_input_c
	syscall
	j end
end:
