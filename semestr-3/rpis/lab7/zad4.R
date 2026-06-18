dane <- read.csv2("~/Documents/coding/coursework-wust/rpis/lab2/mieszkania.csv")

# a)
model <- lm(Cena ~ Metraz, data = dane)
summary(model)

# b)
plot(dane$Metraz, dane$Cena)
abline(model)

# c)
# H0: Reszty modelu regresji mają rozkład normalny
# H1: Reszty modelu regresji nie mają rozkładu normalnego
reszty <- residuals(model)
shapiro.test(reszty)

# Odrzucamy na poziomie istotności 0,1% (p<0,001): Mamy bardzo mocne dowody przeciwko H0

# d)
predict(model, newdata = data.frame(Metraz = 80))
