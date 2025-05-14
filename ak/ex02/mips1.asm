.data
	input_operation: .asciiz "Input operation (0 decode, 1 encode): "
	input_source: .asciiz "Input the source text: "
	input_offset: .asciiz "Input the shift offset: "
	invalid_operation: .asciiz "Invalid operation"
	
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
	j end
encode:
	j end
error_operator:
	li $v0, 4
	la $a0, invalid_operation
	syscall
	j end
end:
