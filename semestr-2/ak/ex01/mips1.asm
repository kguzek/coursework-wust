.data
	input_first: .asciiz "Input first operand: "
	input_second: .asciiz "Input second operand: "
	input_operator: .asciiz "Input operator (0+, 1-, 2/, 3*): "
	invalid_operator: .asciiz "Invalid operator"
	input_loop: .asciiz "\nCalculate again? (0/1): "
	divide_by_zero: .asciiz "Cannot divide by 0"
.text
main:
	# first operand
	li $v0, 4
	la $a0, input_first
	syscall
	li $v0, 5
	syscall
	move $t0, $v0
	# operator
	li $v0, 4
	la $a0, input_operator
	syscall
	li $v0, 5
	syscall
	move $t2, $v0
	# second operand
	li $v0, 4
	la $a0, input_second
	syscall
	li $v0, 5
	syscall
	move $t1, $v0
	# switch
	beq $t2, 0, addition
	beq $t2, 1, subtraction
	beq $t2, 2, division
	beq $t2, 3, multiplication
	j error_operator
addition:
	add $t3, $t0, $t1
	j end
subtraction:
	sub $t3, $t0, $t1
	j end
division:
	beq $t1, 0, error_division
	div $t0, $t1
	mflo $t3
	j end
multiplication:
	mul $t3, $t0, $t1
	j end
error_division:
	li $v0, 4
	la $a0, divide_by_zero
	syscall
	j ask_loop
error_operator:
	li $v0, 4
	la $a0, invalid_operator
	syscall
	j ask_loop
end:
	li $v0, 1
	move $a0, $t3
	syscall
ask_loop:
	li $v0, 4
	la $a0, input_loop
	syscall
	li $v0, 5
	syscall
	beq $v0, 1, main
