d <- read.csv2("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: mężczyźni średnio przytyli się o 4kg
# H1: mężczyźni średnio przytyli się o inną wartość niż  4kg

dm <- d[d$plec == 0, ]
da <- dm$Waga_po - dm$Waga_przed
t.test(da, mu = 4)


# p-value: 0.004053
# Odrzucamy na poziomie istotności 5% (0,01<p<0,05): Mamy dowody przeciwko H0
