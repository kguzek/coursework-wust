# 2.
# a)
path <- "~/Documents/coding/coursework-wust/rpis/lab2/waga1.csv"
# dane <- read.table(path, header=TRUE, sep=";")
dane <- read.csv2(path)
# b)
head(dane, 5)
# c)
str(dane)
# d)
mean(dane$Wzrost)
mean(dane$Waga_przed)
# e)
dane$BMI <- dane$Waga_przed / ((dane$Wzrost / 100) ^ 2)
# e2)
# dane[dane$plec == 1 & dane$BMI > 25, ]
subset(dane, plec == 1 & BMI > 25)
# f)
#dane[dane$plec == 0, ]
subset(plec == 0)
# g)
sum(dane$Wzrost > 175)
