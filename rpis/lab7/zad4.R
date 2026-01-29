dane <- read.csv("~/Documents/coding/coursework-wust/rpis/lab7/mieszkania.csv")

# a) Regresja liniowa ceny względem metrażu
model <- lm(cena ~ metraz, data = dane)
summary(model)

# b) Wykres rozrzutu
plot(dane$metraz, dane$cena)
abline(model)

# c) Test normalności reszt
# H0: Reszty modelu regresji mają rozkład normalny
# H1: Reszty modelu regresji nie mają rozkładu normalnego
reszty <- residuals(model)
shapiro.test(reszty)

# d) Oszacowanie ceny dla mieszkania 80m2
predict(model, newdata = data.frame(metraz = 80))
