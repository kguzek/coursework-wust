n <- 6
p <- 0.5

# i)
dbinom(5, n, p)
# ii)
1 - pbinom(3 - 1, n, p)
# iii)
pbinom(4, n, p) - pbinom(2 - 1, n, p)
# iv)
reszki <- 0:6
dane <- dbinom(reszki, n, p)
plot(reszki, dane, type="h")
