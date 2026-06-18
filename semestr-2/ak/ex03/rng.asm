.data
	newline: .asciiz "\n"
.text
main:
	move $t0, $zero
	move $t1, $zero
	li $t4, 62
	j generate
remainder_numeric:
	add $t2, $t2, 48
	j remainder_after
remainder_upper:
	add $t2, $t2, 55
	j remainder_after
remainder_lower:
	add $t2, $t2, 61
	j remainder_after
generate:
	# break condition
	bge $t1, 1000, end
	li $v0, 42
	move $a1, $t4
	syscall
	move $t2, $a0
	blt $t2, 10, remainder_numeric
	blt $t2, 36, remainder_upper
	j remainder_lower
remainder_after:
	# print character
	li $v0, 11
	move $a0, $t2
	syscall
	add $t0, $t0, 1
	blt $t0, 10, generate
	move $t0, $zero
	add $t1, $t1, 100
	# print newline every 10 characters
	li $v0, 4
	la $a0, newline
	syscall
	# loop
	j generate
end:
