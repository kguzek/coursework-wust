a <- c(1, 4, 6, 13, -10, 8)
b <- seq(1, 101, 2)
c <- c(rep(4, 3), rep(7, 3), rep(9, 3))
d <- c("czy", "to", "jest", "wektor", NA)
e <- c("czy", "to", "jest", "wektor", "NA")
f <- c(rep(c(4, 7, 9), 6))

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

print(sort(d))
print(sort(e))
print(a + f)
print(a * f)
print(a + c)
print(a + 10)
print(b[26])
print(f[6:10])
b2 <- b[b > 50]
print(b2)
print(length(b2))
