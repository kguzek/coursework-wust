path <- "~/Documents/coding/coursework-wust/rpis/lab2/waga1.csv"
dane <- read.csv2(path)

ci_3 <- t.test(dane$Wzrost, conf.level = 0.90)
cat(
  "Przedział ufności (90%): [", round(ci_3$conf.int[1], 2), ",",
  round(ci_3$conf.int[2], 2), "]\n"
)
cat("Średnia z próby:", round(ci_3$estimate, 2), "cm\n")

cat("\n*** WNIOSEK ***\n")
cat("Z 90% pewnością średni wzrost wszystkich studentów (obu płci)\n")
cat(
  "mieści się w przedziale [", round(ci_3$conf.int[1], 2), ",",
  round(ci_3$conf.int[2], 2), "] cm.\n"
)
