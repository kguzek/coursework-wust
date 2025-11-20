wartosci <- 0:3
prawdopodobienstwa <- c(0.15, 0.25, 0.5, 0.1)
wyniki <- sample(wartosci, size=1000, replace=TRUE, prob=prawdopodobienstwa)
par(mfrow = c(1,1))
hist(wyniki, breaks=seq(-0.5, 3.5), freq=FALSE)
