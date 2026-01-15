d <- read.csv2("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: 80% studentów przybywa na wadze
# H1: odsetek przybierających na wadze jest inny niż 80%

d$przybral <- ifelse(d$Waga_po > d$Waga_przed, 1, 0)
prop.test(sum(d$przybral), nrow(d), p = 0.8)

# p-value: 0.05303
# Nie odrzucamy na poziomie istotności 5% (p>0,05): Nie mamy dowodów przeciwko H0
