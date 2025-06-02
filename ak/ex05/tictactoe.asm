.data
	input_rounds: .asciiz "Input number of rounds: "
	error_rounds: .asciiz "Invalid number of rounds (must be 1-5)\n"
	victory_player: .asciiz "Player wins!"
	victory_computer: .asciiz "Computer wins!"
	victory_nobody: .asciiz "Nobody wins (draw)!"
	round: .asciiz "Round "
	of: .asciiz " of "
	newline: .asciiz "\n"
	input_move: .asciiz "Input move (1-9): "
	error_move_invalid: .asciiz "Invalid move (not 1-9)\n"
	error_move_taken: .asciiz "Invalid move (that cell is taken)\n"
	bot_chosen_move: .asciiz "Bot chose move: "
	result: .asciiz "Result: "
	dash: .asciiz "-"
	victory_states:
		# horizontal
		.word 0x00015 # 0b000000000000010101
		.word 0x00540 # 0b000000010101000000
		.word 0x15000 # 0b010101000000000000
		# vertical
		.word 0x01041 # 0b000001000001000001
		.word 0x04104 # 0b000100000100000100
		.word 0x10410 # 0b010000010000010000
		# diagonal
		.word 0x10101 # 0b010000000100000001
		.word 0x01110 # 0b000001000100010000
	bot_mask:
		.word 0x2AAAA # 0b101010101010101010
	# grid
	sym_X:      .asciiz "X"
	sym_O:      .asciiz "O"
	sym_space:  .asciiz " "
	pipe_sep:   .asciiz " | "
	row_sep:    .asciiz "-----------\n"
.text
main:
	li $v0, 4
	la $a0, input_rounds
	syscall
	li $v0, 5
	syscall
	move $t0, $v0
	blt $t0, 1, invalid_rounds
	bgt $t0, 5, invalid_rounds
	move $t1, $zero # current round
	move $t9, $zero # player win count
	j start_round
invalid_rounds:
	li $v0, 4
	la $a0, error_rounds
	syscall
	j main
invalid_move:
	li $v0, 4
	la $a0, error_move_invalid
	syscall
	j game_loop
invalid_move_taken:
	li $v0, 4
	la $a0, error_move_taken
	syscall
	j game_loop
start_round:
	add $t1, $t1, 1
	bgtu $t1, $t0, end
	move $t2, $zero # game state
	jal draw_grid
game_loop:
	li $v0, 4
	la $a0, round
	syscall
	li $v0, 1
	move $a0, $t1
	syscall
	li $v0, 4
	la $a0, of
	syscall
	li $v0, 1
	move $a0, $t0
	syscall
	li $v0, 4
	la $a0, newline
	syscall
	# round logic
	li $v0, 4
	la $a0, input_move
	syscall
	li $v0, 5
	syscall
	move $t3, $v0
	blt $t3, 1, invalid_move
	bgt $t3, 9, invalid_move
validate_move:
	# setup game state arithmetic
	subi $t4, $t3, 1
	mul $t4, $t4, 2
	# check for taken moves (each bit pair represents one cell)
	li $t5, 3
	sllv $t5, $t5, $t4
	and $t5, $t2, $t5
	srlv $t5, $t5, $t4
	bnez $t5, invalid_move_taken
	# store valid move after checking
	li $t5, 1
	sllv $t5, $t5, $t4
	or $t2, $t5, $t2
	jal draw_grid
	# start checking if player won
	move $t4, $zero
	la $t5, victory_states
victory_check:
	lw $t6, 0($t5)
	and $t7, $t6, $t2 # TODO: branch if bot won as well
	beq $t6, $t7, win_player
	addi $t5, $t5, 4
	addi $t4, $t4, 1
	blt $t4, 8, victory_check
	j check_stalemate
check_stalemate:
	lw $t6, bot_mask
	and $t5, $t2, $t6
	srl $t7, $t6, 1
	and $t8, $t2, $t7
	sll $t8, $t8, 1
	or $t5, $t5, $t8
	beq $t5, $t6, round_stalemate
	j bot_move
bot_move:
	# strategy: play the next available move
	# e.g. player plays cell 4 -> bot plays cell 5
	# if cell 5 is taken then play cell 6, etc.
	add $t3, $t3, 1
	bgt $t3, 9, bot_move_reset
	j validate_move_bot
bot_move_reset:
	li $t3, 1
validate_move_bot:
	# setup game state arithmetic
	subi $t4, $t3, 1
	mul $t4, $t4, 2
	# check for taken moves (each bit pair represents one cell)
	li $t5, 3
	sllv $t5, $t5, $t4
	and $t5, $t2, $t5
	srlv $t5, $t5, $t4
	bnez $t5, bot_move
	# store valid move after checking
	li $t5, 2
	sllv $t5, $t5, $t4
	or $t2, $t5, $t2
	# announce bot move
	li $v0, 4
	la $a0, bot_chosen_move
	syscall
	li $v0, 1
	move $a0, $t3
	syscall
	li $v0, 4
	la $a0, newline
	syscall
	jal draw_grid
	move $t4, $zero
	la $t5, victory_states
victory_check_bot:
	lw $t6, 0($t5)
	sll $t6, $t6, 1 # shift left one bit for bot offset
	and $t7, $t6, $t2
	beq $t6, $t7, win_bot
	addi $t5, $t5, 4
	addi $t4, $t4, 1
	blt $t4, 8, victory_check_bot
	j game_loop
win_player:
	la $a0, victory_player
	add $t9, $t9, 1
	j post_round
win_bot:
	la $a0, victory_computer
	srl $t8, $t9, 3
	add $t8, $t8, 1
	sll $t8, $t8, 3
	li $t7, 7 # 0b111
	and $t9, $t9, $t7
	or $t9, $t9, $t8
	j post_round
round_stalemate:
	la $a0, victory_nobody
	j post_round
post_round:
	li $v0, 4
	syscall
	la $a0, newline
	syscall
	j start_round
draw_grid:
	li $t5, 0            # cell index (0 to 8)
	li $t6, 0            # bit shift offset
	li $t7, 9            # total cells

draw_loop:
	srlv $t8, $t2, $t6   # shift game state right by bit offset
	andi $t8, $t8, 0x3   # isolate 2 bits

	li $v0, 4
	la $a0, sym_space
	beq $t8, 0, print_symbol
	la $a0, sym_X
	beq $t8, 1, print_symbol
	la $a0, sym_O

print_symbol:
	syscall

	remu $v1, $t5, 3
	blt $v1, 2, print_pipe

	li $v0, 4
	la $a0, newline
	syscall

	divu $v1, $t5, 3
	beq $v1, 2, skip_separator

	li $v0, 4
	la $a0, row_sep
	syscall

skip_separator:
	j next_cell

print_pipe:
	li $v0, 4
	la $a0, pipe_sep
	syscall

next_cell:
	addiu $t5, $t5, 1
	addiu $t6, $t6, 2
	blt $t5, $t7, draw_loop

	jr $ra
end:
	li $v0, 4 
	la $a0, result
	syscall
	
	li $v0, 1
	li $t7, 7 # 0b111
	and $a0, $t9, $t7
	syscall
	li $v0, 4
	la $a0, dash
	syscall
	li $v0, 1
	srl $a0, $t9, 3
	syscall
	li $v0 ,4
	la $a0, newline
	syscall