dane <- read.csv2("~/Documents/coding/coursework-wust/rpis/lab2/mieszkania.csv")

# a)
# H0: Cena za m2 ma rozkład normalny
# H1: Cena za m2 nie ma rozkładu normalnego
cena_m2 <- dane$Cena / dane$Metraz
shapiro.test(cena_m2)

# Odrzucamy na poziomie istotności 0,1% (p<0,001): Mamy bardzo mocne dowody przeciwko H0

# b)
# H0: Metraż mieszkań ma rozkład normalny
# H1: Metraż mieszkań nie ma rozkładu normalnego
shapiro.test(dane$Metraz)

# Odrzucamy na poziomie istotności 0,1% (p<0,001): Mamy bardzo mocne dowody przeciwko H0
