d <- read.csv2("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: proporcja kobiet i mężczyzn ważących >70kg jest rowna
# H1: proporcje te się różnią

d$wiecej70 <- ifelse(d$Waga_po > 70, 1, 0)
tab2 <- table(d$plec, d$wiecej70)
prop.test(tab2[, 2], rowSums(tab2), correct = FALSE)

# p-value: 0.01801
# Odrzucamy na poziomie istotności 5% (0,01<p<0,05): Mamy dowody przeciwko H0
