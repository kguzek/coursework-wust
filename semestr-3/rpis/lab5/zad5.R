path <- "~/Documents/coding/coursework-wust/rpis/lab2/waga1.csv"
dane <- read.csv2(path)

wzrost_kobiety <- dane$Wzrost[dane$plec == 1]

ci_5 <- t.test(wzrost_kobiety, conf.level = 0.98)
cat(
  "Przedział ufności (98%): [", round(ci_5$conf.int[1], 2), ",",
  round(ci_5$conf.int[2], 2), "]\n"
)
cat("Średnia z próby:", round(ci_5$estimate, 2), "cm\n")

cat("\n*** WNIOSEK ***\n")
cat("Z 98% pewnością średni wzrost studentek w populacji\n")
cat(
  "mieści się w przedziale [", round(ci_5$conf.int[1], 2), ",",
  round(ci_5$conf.int[2], 2), "] cm.\n"
)
