d <- read.csv("/home/konrad/Documents/coding/coursework-wust/rpis/lab2/waga1.csv")

# H0: mężczyźni są średnio o 5cm wyżsi niż kobiety
# H1: różnica wzrostu jest inna niż 5cm

dk <- d[d$plec == 1, ]
dm <- d[d$plec == 0, ]
t.test(dm$wzrost, dk$wzrost, mu = 5)
