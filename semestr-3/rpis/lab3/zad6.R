n <- 180
p <- 1/6

# i)
dbinom(27, n, p)
# ii)
1 - pbinom(32 - 1, n, p)
# iii)
pbinom(29 - 1, n, p)
# iv)
pbinom(33, n, p) - pbinom(25 - 1, n, p)