n <- 100
mean_iq <- 109
var_iq <- 225
sd_iq <- sqrt(var_iq)
n_high <- 30
p_sample <- n_high / n

# a)

p0 <- 0.35

cat("\n=== Zadanie 1.1: Test proporcji ===\n")
cat("H0: p = 0.35 (35% studentów ma IQ > 115)\n")
cat("H1: p ≠ 0.35 (proporcja różni się od 35%)\n\n")

# a) i)

z_stat <- (p_sample - p0) / sqrt(p0 * (1 - p0) / n)
p_value_z <- 2 * pnorm(-abs(z_stat))
cat("i) Test Z (ręczny):\n")
cat("   Statystyka Z =", z_stat, "\n")
cat("   Wartość p =", p_value_z, "\n")

# a) ii)

prop_test_1 <- prop.test(n_high, n, p = 0.35, correct = FALSE)
cat("\nii) prop.test:\n")
print(prop_test_1)

cat("\n*** WNIOSEK ***\n")
cat("p =", round(p_value_z, 4), "\n")
cat("Skoro p > 0.05, nie odrzucamy H0 na poziomie istotności 5%.\n")
cat("Nie mamy dowodów, że proporcja studentów z IQ > 115 różni się od 35%.\n")

# b)

alpha <- 0.01
conf_level <- 0.99

cat("\n=== Zadanie 1.2: Przedział ufności dla proporcji (99%) ===\n")

# b) i)

z_crit <- qnorm(1 - alpha / 2)
se_p <- sqrt(p_sample * (1 - p_sample) / n)
ci_lower_norm <- p_sample - z_crit * se_p
ci_upper_norm <- p_sample + z_crit * se_p
cat("i) Przybliżenie normalne:\n")
cat("   Przedział ufności: [", round(ci_lower_norm, 4), ",", round(ci_upper_norm, 4), "]\n")

# b) ii)

prop_ci <- prop.test(n_high, n, conf.level = conf_level, correct = FALSE)
cat("\nii) prop.test:\n")
cat(
  "   Przedział ufności: [", round(prop_ci$conf.int[1], 4), ",",
  round(prop_ci$conf.int[2], 4), "]\n"
)

cat("\n*** WNIOSEK ***\n")
cat("Z 99% pewnością proporcja studentów z IQ > 115 w populacji mieści się\n")
cat("w przedziale [", round(ci_lower_norm, 4), ",", round(ci_upper_norm, 4), "].\n")
cat("Zauważmy, że wartość 0.35 mieści się w tym przedziale,\n")
cat("co potwierdza wynik testu z zadania 1.1.\n")

# c)

alpha_90 <- 0.10
conf_level_90 <- 0.90

cat("\n=== Zadanie 1.3: Przedział ufności dla średniego IQ (90%, Z) ===\n")
z_crit_90 <- qnorm(1 - alpha_90 / 2)
se_mean <- sd_iq / sqrt(n)
ci_lower_z <- mean_iq - z_crit_90 * se_mean
ci_upper_z <- mean_iq + z_crit_90 * se_mean
cat(
  "Przedział ufności (rozkład normalny): [", round(ci_lower_z, 2), ",",
  round(ci_upper_z, 2), "]\n"
)

cat("\n*** WNIOSEK ***\n")
cat("Z 90% pewnością średnie IQ wszystkich studentów mieści się\n")
cat("w przedziale [", round(ci_lower_z, 2), ",", round(ci_upper_z, 2), "].\n")

# d)

cat("\n=== Zadanie 1.4: Przedział ufności dla średniego IQ (90%, t-Studenta) ===\n")
t_crit_90 <- qt(1 - alpha_90 / 2, df = n - 1)
ci_lower_t <- mean_iq - t_crit_90 * se_mean
ci_upper_t <- mean_iq + t_crit_90 * se_mean
cat(
  "Przedział ufności (rozkład Studenta): [", round(ci_lower_t, 2), ",",
  round(ci_upper_t, 2), "]\n"
)

cat("\n*** WNIOSEK ***\n")
cat(
  "Przedział oparty na rozkładzie t-Studenta: [", round(ci_lower_t, 2), ",",
  round(ci_upper_t, 2), "]\n"
)
cat("jest nieznacznie szerszy niż przedział oparty na rozkładzie normalnym,\n")
cat("co jest właściwe dla skończonej próby (n=100).\n")

# e)

mu0 <- 115

cat("\n=== Zadanie 1.5: Test hipotezy dla średniego IQ ===\n")
cat("H0: μ = 115 (średnie IQ studentów wynosi 115)\n")
cat("H1: μ ≠ 115 (średnie IQ różni się od 115)\n\n")

# e) i)

z_stat_mean <- (mean_iq - mu0) / se_mean
p_value_z_mean <- 2 * pnorm(-abs(z_stat_mean))
cat("i) Test Z:\n")
cat("   Statystyka Z =", round(z_stat_mean, 4), "\n")
cat("   Wartość p =", format(p_value_z_mean, scientific = FALSE), "\n")

# e) ii)

t_stat_mean <- (mean_iq - mu0) / se_mean
p_value_t_mean <- 2 * pt(-abs(t_stat_mean), df = n - 1)
cat("\nii) Test t-Studenta:\n")
cat("   Statystyka t =", round(t_stat_mean, 4), "\n")
cat("   Wartość p =", format(p_value_t_mean, scientific = FALSE), "\n")

cat("\n*** WNIOSEK ***\n")
cat("p < 0.001\n")
cat("Skoro p < 0.001, to:\n")
cat("* odrzucamy H0 na poziomie istotności 1%, 5% i 10%,\n")
cat("* przyjmujemy H1.\n")
cat("Mamy bardzo mocne dowody, że średnie IQ studentów różni się od 115.\n")
cat("W rzeczywistości średnie IQ (109) jest istotnie niższe niż 115.\n")
