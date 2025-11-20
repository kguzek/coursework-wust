par(mfrow = c(1,2))

rbinom_uniform <- function(N, size, prob) {
  U <- matrix(runif(N * size), nrow = N)
  rowSums(U < prob)
}

i <- rbinom_uniform(100, 10, 0.3)
hist(i, freq = FALSE)

rgeom_uniform <- function(N, prob) {
  out <- numeric(N)
  for (n in 1:N) {
    k <- 0
    while (TRUE) {
      u <- runif(1)
      if (u < prob) break
      k <- k + 1
    }
    out[n] <- k
  }
  out
}

ii <- rgeom_uniform(50, 0.4)
hist(ii, freq = FALSE)
