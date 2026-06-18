.data
	a: .word 5
	b: .word 6
	c: .word 4
	d: .word 3
.text
main:
	lw $t0, a
	lw $t1, b
	lw $t2, c
	lw $t3, d
	add $t4, $t0, $t1
	sub $t5, $t2, $t3
	sub $t6, $t4, $t5
	li $v0, 1
	add $a0, $zero, $t6
	syscall
