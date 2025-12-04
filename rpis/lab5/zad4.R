dane <- read.csv("waga1.csv")

wzrost_kobiety <- dane$wzrost[dane$plec == 1]
cat("Liczba studentek:", length(wzrost_kobiety), "\n\n")

cat("H0: μ = 160 (średni wzrost studentek wynosi 160 cm)\n")
cat("H1: μ ≠ 160 (średni wzrost studentek różni się od 160 cm)\n\n")

test_4 <- t.test(wzrost_kobiety, mu = 160)
print(test_4)

cat("\n*** WNIOSEK ***\n")
cat("p =", round(test_4$p.value, 4), "\n")
if (test_4$p.value < 0.05) {
  cat("Skoro p < 0.05, odrzucamy H0 na poziomie istotności 5%.\n")
  cat("Mamy dowody, że średni wzrost studentek różni się od 160 cm.\n")
  if (test_4$estimate < 160) {
    cat("Średni wzrost studentek (", round(test_4$estimate, 2), " cm) jest istotnie niższy niż 160 cm.\n")
  } else {
    cat("Średni wzrost studentek (", round(test_4$estimate, 2), " cm) jest istotnie wyższy niż 160 cm.\n")
  }
} else {
  cat("Skoro p > 0.05, nie odrzucamy H0 na poziomie istotności 5%.\n")
  cat("Nie mamy dowodów, że średni wzrost studentek różni się od 160 cm.\n")
}
