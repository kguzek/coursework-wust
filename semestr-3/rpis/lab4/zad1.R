a <- runif(5000, 0, 1)
b <- rnorm(3000, 100, 15)

par(mfrow = c(1,2))
hist(a,freq=FALSE)
lines(density(a))
hist(b,freq=FALSE)
lines(density(b))
