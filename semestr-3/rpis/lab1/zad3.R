(a <- seq(300, 0, by = -3))
(b <- c("one", "two", "three", "four", 5))
(c <- c("one", "two", "three", "four", "5"))
(d <- rep(c(3, 1, 6), 4))
# (e <- c(rep(3, 4), rep(1, 4), rep(6, 4)))
(e <- rep(c(3, 1, 6), each = 4))
(f <- c(5, 1, 4, 7))

vectors <- list(a, b, c, d, e, f)

for (i in seq_along(vectors)) {
  v <- vectors[[i]]
  print(paste("długość", i, ":", length(v)))
  print(paste("typ", i, ":", typeof(v)))
  print(paste("min.", i, ":", min(v)))
  print(paste("maks.", i, ":", max(v)))
  if (typeof(v) != "character") {
    print(paste("suma", i, ":", sum(v)))
  }
  cat("\n")
}

(sort(b))
(sort(e))
(d + f)
(sum(d * e))
(a[35])
(a[67:85])

iloczyn_wektorowy <- function(a, b) {
  if (length(a) != length(b)) {
    stop("Wektory muszą mieć tę samą długość")
  }
  if (length(a) > 3) {
    #stop("Iloczyn wektorowy nie jest zdefiniowany dla wektorów o długości powyżej 3.")
  }
  result <- numeric(length(a))
  for (i in seq_along(a)) {
    result[i] <- a[i] * b[i]
  }
  return(result)
}

(iloczyn_wektorowy(d, e))

(a_lt_100 <- a[a < 100])
(length(a_lt_100))
