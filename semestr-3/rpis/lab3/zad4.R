lambda <- 4

# i)
1 - pexp(0.5, lambda)
# ii)
pexp(1/3, lambda)
# iii)
pexp(4/3, lambda) - pexp(2/3, lambda)
# iv)
# 1 - pexp(t, lambda) = 0.2
# pex(t, lambda) = 1 - 0.2 = 0.8
qexp(0.8, lambda)
# v)
minuty <- seq(0, 3, by=0.01)
dane <- dexp(minuty, lambda)
plot(minuty, dane, type="l")
