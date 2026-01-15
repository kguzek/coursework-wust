d <- read.csv("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: mężczyźni średnio przytyli się o 4kg
# H1: mężczyźni średnio przytyli się o inną wartość niż  4kg

dm <- d[d$plec == 0, ]
t.test(dm$przed, dm$po, paired = TRUE, mu = 4)
