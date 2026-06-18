path <- "~/Documents/coding/coursework-wust/rpis/lab2/waga1.csv"
dane <- read.csv2(path)

wzrost_mezczyzni <- dane$Wzrost[dane$plec == 0]
n_mezczyzni <- length(wzrost_mezczyzni)
n_wysokich <- sum(wzrost_mezczyzni > 180)
p_wysokich <- n_wysokich / n_mezczyzni

ci_7 <- prop.test(n_wysokich, n_mezczyzni, conf.level = 0.96, correct = FALSE)
cat(
  "Przedział ufności (96%): [", round(ci_7$conf.int[1], 4), ",",
  round(ci_7$conf.int[2], 4), "]\n"
)
cat("Proporcja z próby:", round(p_wysokich, 4), "\n")

cat("\n*** WNIOSEK ***\n")
cat("Z 96% pewnością proporcja mężczyzn wyższych niż 180 cm w populacji\n")
cat(
  "mieści się w przedziale [", round(ci_7$conf.int[1] * 100, 2), "%,",
  round(ci_7$conf.int[2] * 100, 2), "%].\n"
)
if (0.25 >= ci_7$conf.int[1] && 0.25 <= ci_7$conf.int[2]) {
  cat("Zauważmy, że wartość 25% mieści się w tym przedziale,\n")
  cat("co potwierdza wynik testu z zadania 6.\n")
} else {
  cat("Wartość 25% nie mieści się w tym przedziale,\n")
  cat("co wskazuje na różnicę od zakładanej proporcji.\n")
}
