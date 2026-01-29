dane <- read.csv("~/Documents/coding/coursework-wust/rpis/lab7/mieszkania.csv")

# a) Test normalności dla ceny za m2
# H0: Cena za m2 ma rozkład normalny
# H1: Cena za m2 nie ma rozkładu normalnego
shapiro.test(dane$cena_m2)

# b) Test normalności dla metrażu
# H0: Metraż mieszkań ma rozkład normalny
# H1: Metraż mieszkań nie ma rozkładu normalnego
shapiro.test(dane$metraz)
