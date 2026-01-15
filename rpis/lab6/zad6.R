d <- read.csv2("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: mężczyźni średnio przytyli się o 4kg
# H1: mężczyźni średnio przytyli się o inną wartość niż  4kg

dm <- d[d$plec == 0, ]
t.test(dm$Waga_przed, dm$Waga_po, mu = 4)

# p-value: 0.00245
# Odrzucamy na poziomie istotności 1% (0,001<p<0,01): Mamy mocne dowody przeciwko H0
