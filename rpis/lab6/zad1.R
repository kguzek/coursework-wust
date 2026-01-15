d <- read.csv("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: prawdopodobieństwo ukończenia studiów nie zależy od płci
# H1: prawdopodobieństwo ukończenia studiów zależy od płci

n1 <- 520
x1 <- 220
n2 <- 480
x2 <- 165

p1 <- x1 / n1
p2 <- x2 / n2
p <- (x1 + x2) / (n1 + n2)

z <- (p1 - p2) / sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
pval <- 2 * (1 - pnorm(abs(z)))
pval

prop.test(c(x1, x2), c(n1, n2), correct = FALSE)

tab <- matrix(c(n1 - x1, x1, n2 - x2, x2), 2, 2)
tab

chisq.test(tab, correct = FALSE)
fisher.test(tab)

# H0: sredni wzrost nie zalezy od plci
# H1: sredni wzrost zalezy od plci

m1 <- 166
v1 <- 100
m2 <- 174
v2 <- 121

z <- (m1 - m2) / sqrt(v1 / n1 + v2 / n2)
pval <- 2 * (1 - pnorm(abs(z)))
pval

# p < 0.001
# Odrzucamy H0 na poziomie istotnosci 0.1%.
# Mamy bardzo mocne dowody ze średni wzrost zależy od płci
