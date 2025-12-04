dane <- read.csv("waga1.csv")

wzrost_mezczyzni <- dane$wzrost[dane$plec == 0]
n_mezczyzni <- length(wzrost_mezczyzni)
n_wysokich <- sum(wzrost_mezczyzni > 180)
p_wysokich <- n_wysokich / n_mezczyzni

cat("Liczba mężczyzn:", n_mezczyzni, "\n")
cat("Liczba mężczyzn > 180cm:", n_wysokich, "\n")
cat("Proporcja w próbie:", round(p_wysokich, 4), "\n\n")

cat("H0: p = 0.25 (25% studentów (mężczyzn) jest wyższych niż 180 cm)\n")
cat("H1: p ≠ 0.25 (proporcja różni się od 25%)\n\n")

test_6 <- prop.test(n_wysokich, n_mezczyzni, p = 0.25, correct = FALSE)
print(test_6)

cat("\n*** WNIOSEK ***\n")
cat("p =", round(test_6$p.value, 4), "\n")
if (test_6$p.value < 0.05) {
  cat("Skoro p < 0.05, odrzucamy H0 na poziomie istotności 5%.\n")
  cat("Mamy dowody, że proporcja mężczyzn wyższych niż 180 cm różni się od 25%.\n")
  cat("Rzeczywista proporcja w próbie wynosi:", round(p_wysokich * 100, 2), "%.\n")
} else {
  cat("Skoro p > 0.05, nie odrzucamy H0 na poziomie istotności 5%.\n")
  cat("Nie mamy dowodów, że proporcja mężczyzn wyższych niż 180 cm różni się od 25%.\n")
}
