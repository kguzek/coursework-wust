mu <- 170
variance <- 144
sigma <- sqrt(variance)

# i)
1 - pnorm(180, mu, sigma)
# ii)
pnorm(165, mu, sigma)
# iii)
pnorm(190, mu, sigma) - pnorm(155, mu, sigma)
# iv)
# P(X > k) = 10%
# 1 - P(X > k) = 10%
# 1 - pnorm(k, mu, sigma) = 0.1
# pnorm(k, mu, sigma) = 0.9
qnorm(0.9, mu, sigma)
1 - pnorm(185.3786, mu, sigma)
