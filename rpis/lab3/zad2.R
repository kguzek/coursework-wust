lambda <- 6

# i)
dpois(5, lambda)
# ii)
1 - ppois(4 - 1, lambda)
# iii)
ppois(5, lambda) - ppois(3 - 1, lambda)
# iv)
samochody <- 0:30
dane <- dpois(samochody, lambda)
plot(samochody, dane)
