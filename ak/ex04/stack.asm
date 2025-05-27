.data
	prompt_input: .asciiz "Input number of strings... "

.text
main:
	li $v0, 4
	la $a0, prompt_input
	syscall
	li $v0, 5
	syscall
	move $t0, $v0
	
