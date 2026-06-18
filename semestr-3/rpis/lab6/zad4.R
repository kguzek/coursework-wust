d <- read.csv2("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: mężczyźni są średnio o 5cm wyżsi niż kobiety
# H1: różnica wzrostu jest inna niż 5cm

dk <- d[d$plec == 1, ]
dm <- d[d$plec == 0, ]
t.test(dm$Wzrost, dk$Wzrost, mu = 5)

# p-vaue: 0.003025
# Odrzucamy na poziomie istotności 1% (0,001<p<0,01): Mamy mocne dowody przeciwko H0
