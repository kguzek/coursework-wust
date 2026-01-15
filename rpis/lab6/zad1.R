d <- read.csv2("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# a)
# H0: p1 = p2 (Prawdopodobieństwo ukończenia studiów nie zależy od płci)
# H1: p1 != p2 (Prawdopodobieństwo ukończenia studiów zależy od płci)

sukcesy <- c(220, 165)
proby <- c(520, 480)

# ii)
res_prop <- prop.test(sukcesy, proby, correct = FALSE)
print(res_prop)

# i)
z_stat_a <- sqrt(res_prop$statistic)
p_val_a <- res_prop$p.value
cat("Statystyka Z:", z_stat_a, "p-value:", p_val_a)

# p-value: 0.01000722
# Odrzucamy na poziomie istotności 5% (0,01<p<0,05): Mamy dowody przeciwko H0

# b)
# H0: Rozkład wykształcenia jest niezależny od płci
# H1: Rozkład wykształcenia jest zależny od płci

tablica <- matrix(c(300, 220, 315, 165), nrow = 2, byrow = TRUE)
rownames(tablica) <- c("Kobieta", "Mezczyzna")
colnames(tablica) <- c("0", "1")
print(tablica)

# c)
# H0: Wykształcenie nie zależy od płci (zmienne są niezależne)
# H1: Wykształcenie zależy od płci (zmienne są zależne)

# i)
res_chi <- chisq.test(tablica, correct = FALSE)
print(res_chi)

# p-value: 0.01001
# Odrzucamy na poziomie istotności 5% (0,01<p<0,05): Mamy dowody przeciwko H0

# ii)
res_fish <- fisher.test(tablica)
print(res_fish)

# p-value: 0.01118
# Odrzucamy na poziomie istotności 5% (0,01<p<0,05): Mamy dowody przeciwko H0

# d)
# H0: mu1 = mu2 (Średni wzrost nie zależy od płci)
# H1: mu1 != mu2 (Średni wzrost zależy od płci)

n1 <- 520
sr1 <- 166
war1 <- 100
n2 <- 480
sr2 <- 174
war2 <- 121

z_stat_d <- (sr1 - sr2) / sqrt(war1 / n1 + war2 / n2)
p_val_d <- 2 * (1 - pnorm(abs(z_stat_d)))
cat("Statystyka Z:", z_stat_d, "p-value:", p_val_d)

# p-value < 0.001.
# Odrzucamy na poziomie istotności 0,1% (p<0,001): Mamy bardzo mocne dowody przeciwko H0
