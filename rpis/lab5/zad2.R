path <- "~/Documents/coding/coursework-wust/rpis/lab2/waga1.csv"
dane <- read.csv2(path)

dane

str(dane)
head(dane)

test_2 <- t.test(dane$Wzrost, mu = 170)
print(test_2)

cat("\n*** WNIOSEK ***\n")
cat("p =", round(test_2$p.value, 4), "\n")
if (test_2$p.value < 0.05) {
  cat("Skoro p < 0.05, odrzucamy H0 na poziomie istotności 5%.\n")
  cat("Mamy dowody, że średni wzrost studentów różni się od 170 cm.\n")
  if (test_2$estimate < 170) {
    cat("Średni wzrost (", round(test_2$estimate, 2), " cm) jest istotnie niższy niż 170 cm.\n")
  } else {
    cat("Średni wzrost (", round(test_2$estimate, 2), " cm) jest istotnie wyższy niż 170 cm.\n")
  }
} else {
  cat("Skoro p > 0.05, nie odrzucamy H0 na poziomie istotności 5%.\n")
  cat("Nie mamy dowodów, że średni wzrost studentów różni się od 170 cm.\n")
}
