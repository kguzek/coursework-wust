n <- 200
u <- runif(n)
result <- 2 * sqrt(u)
hist(result)

max_x <- 2

f <- function(x) {
  ifelse(x >= 0 & x <= max_x, x, 0)
}

g <- function(x) {
  ifelse(x >= 0 & x <= max_x, 1/2, 0)
}

c <- max_x / g(max_x)

b_i <- function() {
  while (TRUE) {
    y <- runif(1, 0, 2)
    u <- runif(1)
    
    if (u < f(y) / (c * g(y))) {
      return(y)
    }
  }
}

n <- 200
x <- numeric(n)
for (i in 1:n) {
  x[i] <- b_i()
}

hist(x, breaks=20)