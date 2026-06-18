a <- 4
b <- 12

# i)
punif(7, a, b)
# ii)
punif(11, a, b) - punif(5, a, b)
# iii)
1 - punif(10, a, b)
# iv)
# 1 - punif(x, a, b) = 0.6
# punif(x, a, b) = 1 - 0.6 = 0.4
qunif(0.4, a, b)
